#!/bin/bash
#
# Changelog Update Script
#
# Helps developers add entries to CHANGELOG.md interactively
#
# Usage:
#   ./scripts/update_changelog.sh
#   ./scripts/update_changelog.sh --category added --message "New feature X"
#
# Exit Codes:
#   0 - Success
#   1 - Failure

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo -e "${CYAN}📝 $1${NC}"
}

print_prompt() {
    echo -e "${CYAN}$1${NC}"
}

# Function to get category name by number (Bash 3.2 compatible)
get_category_name() {
    case "$1" in
        1) echo "Added" ;;
        2) echo "Changed" ;;
        3) echo "Deprecated" ;;
        4) echo "Removed" ;;
        5) echo "Fixed" ;;
        6) echo "Security" ;;
        *) echo "" ;;
    esac
}

# Function to get category description by number (Bash 3.2 compatible)
get_category_desc() {
    case "$1" in
        1) echo "New features" ;;
        2) echo "Changes in existing functionality" ;;
        3) echo "Soon-to-be removed features" ;;
        4) echo "Removed features" ;;
        5) echo "Bug fixes" ;;
        6) echo "Vulnerability fixes" ;;
        *) echo "" ;;
    esac
}

# Function to normalize category name (convert to title case)
normalize_category() {
    local cat=$(echo "$1" | tr '[:upper:]' '[:lower:]')
    case "$cat" in
        added) echo "Added" ;;
        changed) echo "Changed" ;;
        deprecated) echo "Deprecated" ;;
        removed) echo "Removed" ;;
        fixed) echo "Fixed" ;;
        security) echo "Security" ;;
        *) echo "" ;;
    esac
}

# Function to check if CHANGELOG.md exists
check_changelog_exists() {
    if [ ! -f "CHANGELOG.md" ]; then
        print_error "CHANGELOG.md not found!"
        echo ""
        echo "Please create a CHANGELOG.md file first."
        return 1
    fi
    return 0
}

# Function to display category menu
show_category_menu() {
    echo ""
    print_header "Select a category:"
    echo ""
    for key in 1 2 3 4 5 6; do
        local cat_name=$(get_category_name "$key")
        local cat_desc=$(get_category_desc "$key")
        echo "  $key) $cat_name - $cat_desc"
    done
    echo ""
}

# Function to get user input
get_user_input() {
    local prompt="$1"
    local default="$2"
    local result

    if [ -n "$default" ]; then
        read -p "$prompt [$default]: " result
        result="${result:-$default}"
    else
        read -p "$prompt: " result
    fi

    echo "$result"
}

# Function to get category interactively
get_category_interactive() {
    show_category_menu

    local choice
    while true; do
        print_prompt "Enter choice (1-6): "
        read choice

        if [[ "$choice" =~ ^[1-6]$ ]]; then
            get_category_name "$choice"
            return 0
        else
            print_error "Invalid choice. Please enter 1-6."
        fi
    done
}

# Function to get message interactively
get_message_interactive() {
    echo ""
    print_header "Enter your changelog entry:"
    print_info "Tip: Be clear and concise. Include issue numbers if applicable (e.g., #123)"
    echo ""

    local message
    print_prompt "Entry: "
    read message

    if [ -z "$message" ]; then
        print_error "Message cannot be empty!"
        return 1
    fi

    echo "$message"
}

# Function to find the [Unreleased] section in CHANGELOG.md
find_unreleased_line() {
    grep -n "## \[Unreleased\]" CHANGELOG.md | cut -d: -f1 | head -1
}

# Function to find or create category section under [Unreleased]
find_category_section() {
    local category="$1"
    local unreleased_line=$(find_unreleased_line)

    if [ -z "$unreleased_line" ]; then
        print_error "[Unreleased] section not found in CHANGELOG.md!"
        return 1
    fi

    # Look for the category heading after [Unreleased]
    local category_line=$(awk -v start="$unreleased_line" -v cat="### $category" '
        NR > start && /^### / {
            if ($0 ~ cat) {
                print NR
                exit
            }
        }
    ' CHANGELOG.md)

    echo "$category_line"
}

# Function to add entry to CHANGELOG.md
add_to_changelog() {
    local category="$1"
    local message="$2"
    local temp_file="CHANGELOG.md.tmp"

    # Find [Unreleased] line
    local unreleased_line=$(find_unreleased_line)
    if [ -z "$unreleased_line" ]; then
        print_error "[Unreleased] section not found!"
        return 1
    fi

    # Find category section
    local category_line=$(find_category_section "$category")

    # Create backup
    cp CHANGELOG.md "${temp_file}.backup"

    if [ -z "$category_line" ]; then
        # Category doesn't exist, add it after [Unreleased]
        print_info "Creating new ### $category section..."

        # Find the first line after [Unreleased] that's not empty
        local insert_line=$((unreleased_line + 1))

        awk -v line="$insert_line" -v cat="$category" -v msg="$message" '
            NR == line {
                print ""
                print "### " cat
                print ""
                print "- " msg
                print ""
            }
            { print }
        ' CHANGELOG.md > "$temp_file"
    else
        # Category exists, add entry after the category heading
        print_info "Adding entry to existing ### $category section..."

        # Find the first line after category heading
        local insert_line=$((category_line + 1))

        # Skip empty lines after category heading
        while IFS= read -r line; do
            if [ -z "$line" ]; then
                insert_line=$((insert_line + 1))
            else
                break
            fi
        done < <(tail -n +"$insert_line" CHANGELOG.md)

        awk -v line="$insert_line" -v msg="$message" '
            NR == line {
                print "- " msg
            }
            { print }
        ' CHANGELOG.md > "$temp_file"
    fi

    # Replace original file
    mv "$temp_file" CHANGELOG.md
    rm -f "${temp_file}.backup"

    return 0
}

# Function to show preview of what will be added
show_preview() {
    local category="$1"
    local message="$2"

    echo ""
    print_header "Preview of changelog entry:"
    echo ""
    echo "  ### $category"
    echo ""
    echo "  - $message"
    echo ""
}

# Function to confirm action
confirm_action() {
    local prompt="$1"
    local response

    print_prompt "$prompt (y/N): "
    read response

    [[ "$response" =~ ^[Yy]$ ]]
}

# Parse command line arguments
parse_args() {
    CATEGORY=""
    MESSAGE=""

    while [[ $# -gt 0 ]]; do
        case $1 in
            --category|-c)
                CATEGORY="$2"
                shift 2
                ;;
            --message|-m)
                MESSAGE="$2"
                shift 2
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# Show help message
show_help() {
    cat << EOF
Usage: ./scripts/update_changelog.sh [OPTIONS]

Interactively add entries to CHANGELOG.md under the [Unreleased] section.

OPTIONS:
    -c, --category CATEGORY   Category: added, changed, deprecated, removed, fixed, security
    -m, --message MESSAGE     Changelog entry message
    -h, --help                Show this help message

EXAMPLES:
    # Interactive mode (recommended)
    ./scripts/update_changelog.sh

    # Non-interactive mode
    ./scripts/update_changelog.sh --category added --message "New feature X"
    ./scripts/update_changelog.sh -c fixed -m "Bug fix for issue #123"

CATEGORIES:
    added       - New features
    changed     - Changes in existing functionality
    deprecated  - Soon-to-be removed features
    removed     - Removed features
    fixed       - Bug fixes
    security    - Vulnerability fixes

EOF
}

# Validate category name
validate_category() {
    local cat="$1"
    local cat_lower=$(echo "$cat" | tr '[:upper:]' '[:lower:]')

    case "$cat_lower" in
        added|changed|deprecated|removed|fixed|security)
            # Use normalize_category to get proper capitalization
            normalize_category "$cat_lower"
            return 0
            ;;
        *)
            print_error "Invalid category: $cat"
            echo "Valid categories: added, changed, deprecated, removed, fixed, security"
            return 1
            ;;
    esac
}

# Main execution
main() {
    echo ""
    echo "================================================"
    echo "  CHANGELOG UPDATE HELPER"
    echo "================================================"
    echo ""

    # Check if CHANGELOG.md exists
    check_changelog_exists || exit 1

    # Parse command line arguments
    parse_args "$@"

    # Get category
    if [ -n "$CATEGORY" ]; then
        CATEGORY=$(validate_category "$CATEGORY") || exit 1
    else
        CATEGORY=$(get_category_interactive)
    fi

    # Get message
    if [ -z "$MESSAGE" ]; then
        MESSAGE=$(get_message_interactive) || exit 1
    fi

    # Show preview
    show_preview "$CATEGORY" "$MESSAGE"

    # Confirm
    if ! confirm_action "Add this entry to CHANGELOG.md?"; then
        print_warning "Cancelled by user"
        exit 0
    fi

    # Add to changelog
    if add_to_changelog "$CATEGORY" "$MESSAGE"; then
        echo ""
        print_success "Entry added to CHANGELOG.md!"
        echo ""
        print_info "Don't forget to commit your changes:"
        echo "  git add CHANGELOG.md"
        echo "  git commit -m \"Update CHANGELOG.md: $MESSAGE\""
        echo ""
    else
        print_error "Failed to add entry to CHANGELOG.md"
        exit 1
    fi
}

# Run main function
main "$@"
