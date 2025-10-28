# Continuous Integration (CI)

This document describes the CI/CD setup for the LLM Assistant project.

---

## Overview

The project uses **GitHub Actions** for continuous integration, automatically running tests, linting, and type checks on every push and pull request across multiple operating systems and Python versions.

**CI Badge Status:**
![CI](https://github.com/Deim0s13/llm-assistant/actions/workflows/ci.yml/badge.svg)

---

## Workflow Configuration

### File Location
`.github/workflows/ci.yml`

### Trigger Events
- **Push** to branches: `main`, `dev`, `feature/*`, `hotfix/*`
- **Pull Request** to: `main`, `dev`
- **Manual Dispatch** via GitHub Actions UI

---

## CI Jobs

### 1. Test Matrix (Host-Based)

Runs on multiple OS and Python version combinations to ensure cross-platform compatibility.

**Matrix Configuration:**
- **Operating Systems:**
  - `ubuntu-latest` (Debian-based Linux)
  - `macos-latest` (macOS on Apple Silicon or Intel)
  - `windows-latest` (Windows Server)
  
- **Python Versions:**
  - 3.10
  - 3.11

**Total Combinations:** 6 (3 OS × 2 Python versions)

#### Steps

1. **Checkout code** - Clone the repository
2. **Set up Python** - Install specified Python version with pip caching
3. **Install dependencies** - Install runtime and dev dependencies
4. **Lint with Ruff** - Check code style and common issues
5. **Format check with Ruff** - Verify code formatting
6. **Type check with mypy** - Static type analysis
7. **Type check with Pyright** - Additional type checking
8. **Run tests with pytest** - Execute test suite
9. **Upload test results** - Archive test artifacts

#### Current Status

🚧 **Linting and type checking are currently non-blocking** (set to `continue-on-error: true`)

This pragmatic approach allows CI to pass while the codebase is being cleaned up:
- 44 Ruff linting errors remaining
- 1 mypy error (library-related)
- 38/40 tests passing

**Roadmap:**
- Once linting is clean, set `continue-on-error: false` for strict enforcement
- All tests should pass across all platforms

---

### 2. Container Build & Test (Linux Only)

Validates that the application builds and runs correctly in a containerized environment.

**Platform:** `ubuntu-latest` only

#### Steps

1. **Checkout code** - Clone the repository
2. **Set up Docker Buildx** - Enable multi-platform builds
3. **Build container image** - Build using the `Containerfile`
4. **Test container starts** - Verify the container runs successfully
5. **Upload container logs** - Archive logs for debugging

#### Build Optimizations

- **Layer caching** via GitHub Actions cache
- **Cache strategy:** `type=gha,mode=max`
- Significantly reduces build time on subsequent runs

---

### 3. CI Success (Summary Job)

A required status check that aggregates results from all other jobs.

**Purpose:**
- Enables branch protection rules
- Single check to verify all CI passes
- Fails if any dependent job fails

---

## Branch Protection

### Recommended Settings

For `main` and `dev` branches:

1. **Require status checks to pass:**
   - ✅ CI Success
   
2. **Require branches to be up to date:**
   - ✅ Enabled

3. **Status checks per platform:**
   - Test (ubuntu-latest, Python 3.10)
   - Test (ubuntu-latest, Python 3.11)
   - Test (macos-latest, Python 3.10)
   - Test (macos-latest, Python 3.11)
   - Test (windows-latest, Python 3.10)
   - Test (windows-latest, Python 3.11)
   - Container Build & Test (Linux)

---

## Platform-Specific Notes

### Linux (Ubuntu)

- **Standard runner:** `ubuntu-latest` (Debian-based)
- **Note:** GitHub Actions does not provide `rhel-latest` as a standard runner
- **For RHEL testing:** Consider self-hosted runners or container-based testing

### macOS

- Runs on Apple Silicon (M1/M2) or Intel hardware
- PyTorch with MPS (Metal Performance Shaders) support
- Slower than Linux due to fewer available runners

### Windows

- Runs on Windows Server
- Path separators handled automatically by GitHub Actions
- PowerShell and cmd.exe both supported

---

## Dependency Caching

The workflow uses GitHub Actions cache to speed up builds:

```yaml
cache: 'pip'
cache-dependency-path: |
  requirements.txt
  requirements-dev.txt
```

**Benefits:**
- Faster subsequent runs (pip packages cached)
- Reduces network bandwidth
- Consistent dependency resolution

**Cache invalidation:**
- Automatic when `requirements*.txt` files change
- Manual invalidation via GitHub Actions UI if needed

---

## Artifacts

### Test Results

**Path:** `.pytest_cache`, `debug.log`  
**Retention:** 7 days  
**Access:** Via GitHub Actions UI → Artifacts

### Container Logs

**Retention:** 7 days  
**Access:** Via GitHub Actions UI → Artifacts

---

## Running CI Locally

### Prerequisites

```bash
# Install dependencies
pip install -r requirements-dev.txt
```

### Run the same checks locally

```bash
# Lint
ruff check .

# Format check
ruff format --check .

# Type check
mypy .
pyright

# Tests
pytest -v

# Container build (requires Docker/Podman)
docker build -t llm-assistant:local -f Containerfile .
docker run --rm -p 7860:7860 llm-assistant:local
```

### Pre-commit hooks (optional)

Install pre-commit to run checks automatically:

```bash
pip install pre-commit
pre-commit install
```

---

## Troubleshooting

### CI Fails on Specific Platform

1. Check the specific job logs in GitHub Actions
2. Look for platform-specific errors (paths, dependencies)
3. Test locally on that platform if available
4. Use artifacts to download logs for debugging

### Caching Issues

If dependency resolution seems stale:

1. Go to Actions → Caches
2. Delete the relevant cache
3. Re-run the workflow

### Container Build Failures

1. Check the Containerfile for syntax issues
2. Verify base image is accessible
3. Review container logs artifact
4. Test build locally with Docker/Podman

---

## Future Enhancements

### Short Term

- [ ] Fix remaining 44 Ruff linting errors
- [ ] Enable strict linting enforcement (`continue-on-error: false`)
- [ ] Fix 2 failing tests in test isolation
- [ ] Add code coverage reporting
- [ ] Add coverage thresholds

### Medium Term

- [ ] Add security scanning (Dependabot, Snyk)
- [ ] Publish container images to GHCR/DockerHub
- [ ] Add performance benchmarking
- [ ] Matrix test with more Python versions (3.12, 3.13)

### Long Term

- [ ] Add self-hosted runners for RHEL testing
- [ ] Implement deployment automation (CD)
- [ ] Add smoke tests for production deployments
- [ ] Integration with monitoring/observability

---

## Related Documentation

- [SETUP.md](./SETUP.md) - Local development setup
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Contribution guidelines
- [CONTAINER.md](./CONTAINER.md) - Container usage guide
- [README.md](../README.md) - Project overview

---

## Questions?

For CI-related issues or questions, please:
1. Check existing GitHub Actions runs
2. Review this documentation
3. Open an issue with the `ci` label

