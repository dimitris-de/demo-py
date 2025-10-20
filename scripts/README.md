# Utility Scripts

This directory contains utility scripts for project maintenance and CI/CD automation.

## Available Scripts

### `check_changelog.sh`

Validates that `CHANGELOG.md` is properly maintained and updated.

**Purpose:**
- Ensures CHANGELOG.md exists
- Verifies it's updated when source code changes (in merge requests)
- Validates proper format with required `[Unreleased]` section

**Usage:**

```bash
# Run manually
./scripts/check_changelog.sh

# In GitLab CI (automatic)
# Runs on merge request and main branch pipelines
```

**Features:**
- ✅ Colored output for better readability
- ✅ Detailed error messages with actionable suggestions
- ✅ Smart detection of source code changes
- ✅ Skips check for documentation-only changes
- ✅ GitLab CI environment variable support

**Exit Codes:**
- `0` - All checks passed
- `1` - Validation failed

**Environment Variables (GitLab CI):**
- `CI_PIPELINE_SOURCE` - Type of pipeline (merge_request_event, etc.)
- `CI_MERGE_REQUEST_TARGET_BRANCH_NAME` - Target branch for merge requests

**Example Output:**

```
================================================
  CHANGELOG.MD VALIDATION
================================================

🔍 Checking if CHANGELOG.md exists...
✅ CHANGELOG.md exists

🔍 Checking if CHANGELOG.md was updated...
✅ CHANGELOG.md was updated

🔍 Validating CHANGELOG.md format...
✅ CHANGELOG.md format is valid

================================================
✅ All changelog validations passed!
================================================
```

## Adding New Scripts

When adding new utility scripts to this directory:

1. **Make it executable:**
   ```bash
   chmod +x scripts/your_script.sh
   ```

2. **Add shebang at the top:**
   ```bash
   #!/bin/bash
   ```

3. **Add documentation header:**
   ```bash
   #
   # Script Name
   #
   # Description of what the script does
   #
   # Usage:
   #   ./scripts/your_script.sh [args]
   #
   # Exit Codes:
   #   0 - Success
   #   1 - Failure
   ```

4. **Use `set -e` for safety:**
   ```bash
   set -e  # Exit on any error
   ```

5. **Add colored output functions:**
   ```bash
   RED='\033[0;31m'
   GREEN='\033[0;32m'
   NC='\033[0m'
   
   print_success() {
       echo -e "${GREEN}✅ $1${NC}"
   }
   ```

6. **Document it here** in this README

7. **Update `.gitlab-ci.yml`** if it should run in CI

## Script Guidelines

### Best Practices

- ✅ Use meaningful variable names
- ✅ Add comments for complex logic
- ✅ Provide helpful error messages
- ✅ Return appropriate exit codes
- ✅ Handle edge cases gracefully
- ✅ Make output clear and actionable
- ✅ Test locally before committing

### Error Handling

Always handle errors gracefully:

```bash
# Check if file exists
if [ ! -f "somefile.txt" ]; then
    print_error "File not found!"
    echo "Please create somefile.txt first."
    exit 1
fi

# Check if command succeeded
if ! some_command; then
    print_error "Command failed!"
    exit 1
fi
```

### GitLab CI Integration

To use a script in GitLab CI:

```yaml
job_name:
  stage: your_stage
  image: alpine:latest
  before_script:
    - apk add --no-cache bash git  # Install dependencies
  script:
    - ./scripts/your_script.sh
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
```

## Maintenance

These scripts should be:
- Reviewed during code reviews
- Tested when modified
- Kept simple and focused
- Well-documented
- Version controlled

## Testing Scripts Locally

Before committing script changes:

```bash
# Make it executable
chmod +x scripts/your_script.sh

# Test it
./scripts/your_script.sh

# Test error cases
# (modify conditions to trigger errors)

# Check exit code
echo $?  # Should be 0 for success, non-zero for failure
```

## Resources

- [Bash Best Practices](https://bertvv.github.io/cheat-sheets/Bash.html)
- [Shell Check](https://www.shellcheck.net/) - Online shell script analyzer
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
