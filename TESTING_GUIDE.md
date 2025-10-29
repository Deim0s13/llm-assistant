# Manual Testing Guide for CI & GHCR Implementation

This guide walks through testing the CI workflow and GHCR publishing implementation locally before pushing to GitHub.

---

## ✅ Pre-Push Testing (Do This Now)

### Test 1: Workflow YAML Validation

Verify the workflow syntax is valid:

```bash
cd /Users/pleathen/Projects/ai-experiments/llm-assistant
source venv/bin/activate
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml')); print('✅ Workflow YAML is valid')"
```

**Expected output:** `✅ Workflow YAML is valid`

**Status:** ✅ **PASSED** (verified above)

---

### Test 2: Local Container Build

Build the container image locally to ensure the Containerfile works:

```bash
docker build -t llm-assistant:test -f Containerfile .
# or with podman
podman build -t llm-assistant:test -f Containerfile .
```

**Expected output:** `Successfully tagged ... llm-assistant:test`

**Status:** ✅ **PASSED** (verified above)

---

### Test 3: Container Startup Test

Run the container and verify it starts successfully:

```bash
# Start container
docker run -d --name llm-test -p 7861:7860 \
  -e MEMORY__ENABLED=true \
  -e MEMORY__BACKEND=in_memory \
  llm-assistant:test

# Wait for startup (15-30 seconds)
sleep 15

# Check logs
docker logs llm-test

# Should see: "Running on local URL:  http://0.0.0.0:7860"
```

**Test in browser:** http://localhost:7861

**Clean up:**
```bash
docker stop llm-test
docker rm llm-test
```

**Status:** ✅ **PASSED** (verified above)

---

### Test 4: Lint & Type Checks (Optional)

Run the same checks CI will run:

```bash
source venv/bin/activate

# Linting
ruff check .

# Format check
ruff format --check .

# Type checking
mypy .
pyright
```

**Note:** These will show errors (44 Ruff errors currently), but they're non-blocking in CI.

---

### Test 5: Run Tests

Run the test suite that CI will run:

```bash
source venv/bin/activate
pytest -v --tb=short

# Or just a quick smoke test
pytest tests/test_memory_backend.py -v
```

**Expected:** Most tests should pass (38/40 currently passing)

---

### Test 6: Multi-Architecture Build (Advanced)

Test building for multiple architectures (same as CI will do):

**Requirements:** Docker Buildx

```bash
# Create buildx builder (one-time setup)
docker buildx create --name multiarch --use

# Build for amd64 + arm64 (don't push)
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t ghcr.io/deim0s13/llm-assistant:test \
  -f Containerfile \
  .

# Clean up
docker buildx rm multiarch
```

**Expected:** Build succeeds for both architectures

**Status:** Optional (can skip - CI will test this)

---

## 🚀 Post-Push Testing (After Pushing to GitHub)

### Test 7: Verify CI Triggers

After pushing the branch:

```bash
git push origin feature/v0.5.1-containerisation
```

1. Go to: https://github.com/Deim0s13/llm-assistant/actions
2. You should see a new workflow run
3. Verify all jobs start:
   - ✅ Test (ubuntu-latest, Python 3.10)
   - ✅ Test (ubuntu-latest, Python 3.11)
   - ✅ Test (macos-latest, Python 3.10)
   - ✅ Test (macos-latest, Python 3.11)
   - ✅ Test (windows-latest, Python 3.10)
   - ✅ Test (windows-latest, Python 3.11)
   - ✅ Container Build & Test (Linux)
   - ⏭️  Publish to GHCR (should be skipped - not on main)
   - ✅ CI Success

**Expected:** 7 jobs pass, 1 job skipped (publish-container)

---

### Test 8: Verify Publishing Job is Skipped on Feature Branch

In the workflow run, check the "Publish to GHCR" job:

**Expected status:** Skipped (with message: "Only publish on push to main or version tags")

---

### Test 9: Test Publishing on Main (After Merge)

After merging the PR to main:

1. Go to: https://github.com/Deim0s13/llm-assistant/actions
2. Check the workflow run triggered by the merge
3. Verify "Publish to GHCR" job **runs** (not skipped)
4. Check the job output for published tags

**Expected tags created:**
- `ghcr.io/deim0s13/llm-assistant:latest`
- `ghcr.io/deim0s13/llm-assistant:main-<short-sha>`

---

### Test 10: Verify Published Image on GHCR

After the publish job completes:

1. Go to: https://github.com/Deim0s13/llm-assistant/packages
2. Find the `llm-assistant` package
3. Verify tags are present: `latest`, `main-<sha>`
4. Check that both architectures are listed: `linux/amd64`, `linux/arm64`

---

### Test 11: Pull and Run Published Image

Test pulling the published image:

```bash
# Pull from GHCR
docker pull ghcr.io/deim0s13/llm-assistant:latest

# Run it
docker run --rm -p 7860:7860 ghcr.io/deim0s13/llm-assistant:latest
```

**Expected:** 
- Pull completes successfully
- Container starts and shows: "Running on local URL:  http://0.0.0.0:7860"
- Visit http://localhost:7860 to verify UI works

---

### Test 12: Test Version Tag Publishing

Create and push a version tag:

```bash
# Create a test tag
git tag v0.5.1-test
git push origin v0.5.1-test
```

**Expected:**
1. CI runs
2. "Publish to GHCR" job runs
3. Multiple tags created:
   - `0.5.1-test`
   - `0.5`
   - `0`
   - `latest`

**Verify on GHCR:** https://github.com/Deim0s13/llm-assistant/packages

**Clean up test tag:**
```bash
git tag -d v0.5.1-test
git push origin :refs/tags/v0.5.1-test
```

---

## 🔍 Verification Checklist

### Pre-Push (Local Testing)
- [x] Workflow YAML is valid
- [x] Container builds successfully
- [x] Container starts and runs
- [ ] Tests pass locally
- [ ] Linting runs (errors ok, just verify it runs)

### Post-Push (GitHub Actions)
- [ ] CI triggers on push
- [ ] All 6 test jobs pass (Linux/macOS/Windows × Python 3.10/3.11)
- [ ] Container build job passes
- [ ] Publish job skipped on feature branch
- [ ] CI Success job passes

### Post-Merge to Main
- [ ] Publish job runs (not skipped)
- [ ] Image appears on GHCR
- [ ] Both architectures present (amd64 + arm64)
- [ ] `latest` tag created
- [ ] Image can be pulled
- [ ] Pulled image runs successfully

### Version Tag Testing
- [ ] CI triggers on version tag
- [ ] Publish job runs
- [ ] Semver tags created (X.Y.Z, X.Y, X)
- [ ] All tags visible on GHCR

---

## 🐛 Troubleshooting

### Issue: Container build fails locally

**Check:**
```bash
# View detailed build output
docker build --progress=plain -t llm-assistant:test -f Containerfile .
```

**Common causes:**
- Dependency version conflicts
- Network issues during pip install
- Base image not available

---

### Issue: Container starts but UI not accessible

**Check:**
```bash
# Verify container is running
docker ps | grep llm-assistant

# Check logs for errors
docker logs <container-id>

# Test the port
curl http://localhost:7860
```

---

### Issue: Publish job fails on GitHub

**Check:**
1. Workflow logs for specific error
2. `GITHUB_TOKEN` permissions (should be automatic)
3. Branch/tag conditions met
4. Package visibility settings

---

### Issue: Can't pull from GHCR

**Check:**
1. Package is set to public: https://github.com/Deim0s13/llm-assistant/packages
2. Correct image path: `ghcr.io/deim0s13/llm-assistant:latest`
3. Tag exists on GHCR

---

## 📊 Test Results Summary

### Local Pre-Push Tests
- ✅ Workflow YAML valid
- ✅ Container builds (2m 30s)
- ✅ Container runs successfully
- ✅ Gradio UI accessible on port 7860

### Ready to Push: **YES** ✅

---

## 🚀 Next Steps

1. **Review the changes:**
   ```bash
   git log --oneline -2
   git diff origin/feature/v0.5.1-containerisation
   ```

2. **Push to GitHub:**
   ```bash
   git push origin feature/v0.5.1-containerisation
   ```

3. **Create Pull Request:**
   - Go to: https://github.com/Deim0s13/llm-assistant/pulls
   - Create PR from `feature/v0.5.1-containerisation` to `main` or `dev`

4. **Monitor CI:**
   - Watch GitHub Actions run
   - Verify all checks pass
   - Publish job should be skipped (until merged to main)

5. **After Merge:**
   - Check GitHub Packages for published image
   - Test pulling and running the published image
   - Update any documentation with first release date

---

## 📝 Notes

- The container takes ~15-30 seconds to fully start (loading ML models)
- First build is slow due to dependency downloads (~5-10 min)
- Subsequent builds are faster with caching
- Multi-arch builds take longer but CI handles this automatically
- GHCR images are cached and should pull quickly (~30 sec)

---

**Questions?** See:
- [CI.md](docs/CI.md) - CI workflow documentation
- [CONTAINER.md](docs/CONTAINER.md) - Container usage guide
- [GHCR_PUBLISHING_SUMMARY.md](docs/GHCR_PUBLISHING_SUMMARY.md) - Implementation details

