#!/bin/bash
#
# Changelog Validation Script
#
# This script validates that CHANGELOG.md is properly maintained:
# 1. Checks if CHANGELOG.md exists
# 2. Verifies it's updated when source code changes (in MRs)
# 3. Validates required format (has [Unreleased] section)
#
# Usage:
#   ./scripts/check_changelog.sh
#
# Environment Variables (GitLab CI):
#   CI_PIPELINE_SOURCE - Type of pipeline (merge_request_event, etc.)
#   CI_MERGE_REQUEST_TARGET_BRANCH_NAME - Target branch for MR
#
# Exit Codes:
#   0 - All checks passed
#   1 - Validation failed

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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
    echo -e "${BLUE}🔍 $1${NC}"
}

# Check if CHANGELOG.md exists
check_changelog_exists() {
    print_header "Checking if CHANGELOG.md exists..."

    if [ ! -f "CHANGELOG.md" ]; then
        print_error "CHANGELOG.md not found!"
        echo ""
        echo "Please create a CHANGELOG.md file following Keep a Changelog format:"
        echo "https://keepachangelog.com/"
        return 1
    fi

    print_success "CHANGELOG.md exists"
    return 0
}

# Check if CHANGELOG.md was updated in merge requests
check_changelog_updated() {
    # Only check in merge request pipelines
    if [ "$CI_PIPELINE_SOURCE" != "merge_request_event" ]; then
        print_info "Not a merge request, skipping update check"
        return 0
    fi

    print_header "Checking if CHANGELOG.md was updated..."

    # Get target branch
    local target_branch="${CI_MERGE_REQUEST_TARGET_BRANCH_NAME:-main}"

    # Fetch target branch
    git fetch origin "$target_branch" 2>/dev/null || {
        print_warning "Could not fetch target branch, skipping update check"
        return 0
    }

    # Get list of changed files
    local changed_files
    changed_files=$(git diff --name-only "origin/$target_branch...HEAD" 2>/dev/null || echo "")

    if [ -z "$changed_files" ]; then
        print_warning "Could not determine changed files, skipping update check"
        return 0
    fi

    # Check if any source files were changed
    local source_changed
    source_changed=$(echo "$changed_files" | grep -E "^(src/|tests/|pyproject.toml)" || true)

    if [ -z "$source_changed" ]; then
        print_info "No source code changes detected, skipping changelog check"
        return 0
    fi

    # Check if CHANGELOG.md was also changed
    if ! echo "$changed_files" | grep -q "CHANGELOG.md"; then
        print_error "Source code was modified but CHANGELOG.md was not updated!"
        echo ""
        echo "📝 Please update CHANGELOG.md with your changes under the [Unreleased] section."
        echo ""
        echo "Changed source files:"
        echo "$source_changed" | sed 's/^/  - /'
        echo ""
        echo "Update CHANGELOG.md with one of these categories:"
        echo "  - Added: New features"
        echo "  - Changed: Changes to existing functionality"
        echo "  - Deprecated: Soon-to-be removed features"
        echo "  - Removed: Removed features"
        echo "  - Fixed: Bug fixes"
        echo "  - Security: Vulnerability fixes"
        return 1
    fi

    print_success "CHANGELOG.md was updated"
    return 0
}

# Validate CHANGELOG.md format
validate_changelog_format() {
    print_header "Validating CHANGELOG.md format..."

    local errors=0

    # Check for [Unreleased] section
    if ! grep -q "## \[Unreleased\]" CHANGELOG.md; then
        print_error "CHANGELOG.md missing [Unreleased] section!"
        echo ""
        echo "Your CHANGELOG.md must have an [Unreleased] section for ongoing changes."
        echo ""
        echo "Example:"
        echo "  ## [Unreleased]"
        echo ""
        echo "  ### Added"
        echo "  - New feature description"
        echo ""
        errors=$((errors + 1))
    fi

    # Check for Keep a Changelog reference (optional but recommended)
    if ! grep -q "keepachangelog.com" CHANGELOG.md; then
        print_warning "CHANGELOG.md doesn't reference Keep a Changelog format"
        echo "Consider adding: https://keepachangelog.com/"
    fi

    if [ $errors -gt 0 ]; then
        return 1
    fi

    print_success "CHANGELOG.md format is valid"
    return 0
}

# Main execution
main() {
    echo ""
    echo "================================================"
    echo "  CHANGELOG.MD VALIDATION"
    echo "================================================"
    echo ""

    local exit_code=0

    # Run all checks
    check_changelog_exists || exit_code=1
    echo ""

    if [ $exit_code -eq 0 ]; then
        check_changelog_updated || exit_code=1
        echo ""
    fi

    if [ $exit_code -eq 0 ]; then
        validate_changelog_format || exit_code=1
        echo ""
    fi

    # Final result
    if [ $exit_code -eq 0 ]; then
        echo "================================================"
        print_success "All changelog validations passed!"
        echo "================================================"
        echo ""
    else
        echo "================================================"
        print_error "Changelog validation failed!"
        echo "================================================"
        echo ""
        echo "Please fix the issues above and try again."
        echo ""
    fi

    return $exit_code
}

# Run main function
main
