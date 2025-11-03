# Run in Containers (Podman/Docker)

This project ships with containerized workflows for local development and production deployment.

**Available Options:**
* **Option A — Published images from GHCR**: Pull pre-built images (recommended for users)
* **Option B — Build locally**: Build from source (for development)
* **Option C — Compose stack with Redis**: App + Redis backend for persistent memory

Both Podman and Docker are supported. Commands below show both; use whichever you prefer.

---

## Option A — Using Published Images from GHCR (Recommended)

Pre-built container images are automatically published to GitHub Container Registry on every release.

### 1) Pull the latest image

```bash
# Pull latest stable release
docker pull ghcr.io/deim0s13/llm-assistant:latest
# or with podman
podman pull ghcr.io/deim0s13/llm-assistant:latest

# Or pull a specific version
docker pull ghcr.io/deim0s13/llm-assistant:0.5.1
```

### 2) Run the container

```bash
docker run --rm -p 7860:7860 \
  -e MEMORY__ENABLED=true \
  -e MEMORY__BACKEND=in_memory \
  ghcr.io/deim0s13/llm-assistant:latest

# Or with podman
podman run --rm -p 7860:7860 \
  -e MEMORY__ENABLED=true \
  -e MEMORY__BACKEND=in_memory \
  ghcr.io/deim0s13/llm-assistant:latest
```

### 3) Open the UI

Visit: [http://localhost:7860](http://localhost:7860)

### Available Tags

| Tag Pattern | Description | Example |
|-------------|-------------|---------|
| `latest` | Latest stable release from main branch | `ghcr.io/deim0s13/llm-assistant:latest` |
| `X.Y.Z` | Specific semantic version | `ghcr.io/deim0s13/llm-assistant:0.5.1` |
| `X.Y` | Latest patch in minor version | `ghcr.io/deim0s13/llm-assistant:0.5` |
| `X` | Latest minor in major version | `ghcr.io/deim0s13/llm-assistant:0` |
| `main-<sha>` | Specific commit from main | `ghcr.io/deim0s13/llm-assistant:main-abc1234` |

**Platform Support:**
- `linux/amd64` (Intel/AMD)
- `linux/arm64` (Apple Silicon, ARM servers)

Docker/Podman automatically pulls the correct architecture for your system.

---

## Option B — Build Locally from Source

For development or customization, build the image locally.

---

## Prerequisites

* Podman ≥ 4.x (or Docker ≥ 24.x)
* Python not required on host (everything runs inside the container)
* Open port **7860** on your host

Optional: create a `.env` at the repo root to centralize overrides:

```env
# .env (optional)
MEMORY__ENABLED=true
MEMORY__BACKEND=none        # or "redis"
MEMORY__REDIS_URL=redis://redis:6379/0
SAFETY__SENSITIVITY_LEVEL=moderate
```

> The app reads environment variables first, then falls back to `config/settings.json`.

---

## Build Instructions (Option B)

### 1) Build the image

```bash
podman build -t llm-assistant:dev -f Containerfile .
# docker build -t llm-assistant:dev -f Containerfile .
```

### 2) Run the container

```bash
podman run --rm -p 7860:7860 \
  --env-file .env \
  -e MEMORY__ENABLED=true \
  -e MEMORY__BACKEND=none \
  llm-assistant:dev
```

* The app binds to `0.0.0.0:7860` in the container, mapped to `localhost:7860` on your host.

### 3) Open the UI

* Visit: [http://localhost:7860](http://localhost:7860)

### 4) Stop the container

* Press `Ctrl+C` if running in the foreground.
* If detached: `podman ps` → `podman stop <container_id>`

---

## Option C — Compose Stack with Redis

This runs **two containers**: the app and a Redis service for the memory backend.

You can use either published images from GHCR or build locally.

### 1) Compose file

Create `compose.yml` at the repo root:

**Using published image from GHCR (recommended):**

```yaml
version: "3.9"
services:
  app:
    image: ghcr.io/deim0s13/llm-assistant:latest
    ports:
      - "7860:7860"
    environment:
      MEMORY__ENABLED: "true"
      MEMORY__BACKEND: "redis"
      MEMORY__REDIS_URL: "redis://redis:6379/0"
    depends_on:
      - redis

  redis:
    image: docker.io/library/redis:7
    command: ["redis-server", "--save", "", "--appendonly", "no"]
    # (optional) add a healthcheck if you want the app to wait for Redis
    # healthcheck:
    #   test: ["CMD", "redis-cli", "ping"]
    #   interval: 5s
    #   timeout: 3s
    #   retries: 10
```

**Or build locally:**

```yaml
version: "3.9"
services:
  app:
    build:
      context: .
      dockerfile: Containerfile
    image: llm-assistant:dev
    ports:
      - "7860:7860"
    environment:
      MEMORY__ENABLED: "true"
      MEMORY__BACKEND: "redis"
      MEMORY__REDIS_URL: "redis://redis:6379/0"
    depends_on:
      - redis

  redis:
    image: docker.io/library/redis:7
    command: ["redis-server", "--save", "", "--appendonly", "no"]
```

> Tip (Fedora/SELinux + volumes): if you later mount volumes, remember `:Z` labels, e.g. `- ./data:/data:Z`.

### 2) Bring the stack up

```bash
podman compose up --build -d
# docker compose up --build -d
```

### 3) Open the UI

* Visit: [http://localhost:7860](http://localhost:7860)

### 4) Stop & clean up

```bash
podman compose down
# docker compose down
```

If you see dependency errors on shutdown, re-run `compose down` or stop the app first, then Redis:

```bash
podman stop <app_container_id>
podman stop <redis_container_id>
podman compose down
```

---

## 🔄 Development with Volumes

If you want to live-edit code on your host and run it inside the container, mount the repo into the container:

```bash
podman run --rm -p 7860:7860 \
  -v $(pwd):/app \
  llm-assistant:dev
```

This way, any code changes you make locally are reflected immediately in the container runtime.
*(Note: this does not auto-reload the app; restart the container to pick up changes.)*

---

## 🍏 Apple Silicon Notes (M1/M2/M3)

The base image (`python:3.13-slim`) is multi-arch and supports both `amd64` (Intel/AMD) and `arm64` (Apple Silicon).
Podman/Docker will automatically pull the correct variant for your machine.

* If a dependency isn’t available on `arm64` (rare, but e.g. `bitsandbytes`), you can force x86 emulation:

```bash
podman build --platform linux/amd64 -t llm-assistant:dev -f Containerfile .
podman run --rm -p 7860:7860 --platform linux/amd64 llm-assistant:dev
```

Be aware: emulation is slower and more resource-intensive.

---

## Troubleshooting

* **Blank page in Safari**: Some Safari versions don’t render Gradio correctly. Try a Chromium-based browser (Chrome/Brave) or Firefox.
* **Port already in use**: Stop previous runs or change host port: `-p 8080:7860` → open [http://localhost:8080](http://localhost:8080)
* **Can’t reach the app**:

  * Check logs: `podman logs <container_name>`
  * Verify it’s listening: you should see `* Running on local URL: http://0.0.0.0:7860`
* **Compose shutdown errors**: Use `podman compose down` (or `docker compose down`) to remove both containers. If it complains about dependents, stop containers individually as shown above, then `down`.

---

## Quick Reference: Environment Variables

| Variable                    | Description                    | Example                           |
| --------------------------- | ------------------------------ | --------------------------------- |
| `MEMORY__ENABLED`           | Turn memory on/off             | `true` / `false`                  |
| `MEMORY__BACKEND`           | Memory backend                 | `none` / `redis`                  |
| `MEMORY__REDIS_URL`         | Redis URL (when backend=redis) | `redis://redis:6379/0`            |
| `SAFETY__SENSITIVITY_LEVEL` | Guardrail level                | `strict` / `moderate` / `relaxed` |

---

## 📦 Image Publishing (Automated)

Container images are automatically published to **GitHub Container Registry (GHCR)** via CI/CD.

### Publishing Triggers

| Event | Tags Created | Example |
|-------|-------------|---------|
| **Push to main** | `latest`, `main-<sha>` | `ghcr.io/deim0s13/llm-assistant:latest` |
| **Version tag** | `X.Y.Z`, `X.Y`, `X` | `ghcr.io/deim0s13/llm-assistant:0.5.1` |

### How It Works

1. **Tests pass** on all platforms (Linux, macOS, Windows)
2. **Container build succeeds** on Linux
3. **CI publishes** multi-arch images (amd64 + arm64) to GHCR
4. **Images tagged** automatically based on semver or branch

### Viewing Published Images

Visit: [https://github.com/Deim0s13/llm-assistant/pkgs/container/llm-assistant](https://github.com/Deim0s13/llm-assistant/pkgs/container/llm-assistant)

### Manual Publishing (Maintainers Only)

If you need to manually push an image:

```bash
# Build multi-arch image
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t ghcr.io/deim0s13/llm-assistant:custom-tag \
  --push \
  -f Containerfile .

# Login required (use GitHub PAT with packages:write)
docker login ghcr.io -u YOUR_USERNAME
```

---

## Notes

* The container entrypoint runs: `python main.py`
* For local development with live-reload, prefer running directly on your host (venv) or consider a dev-specific image with `watchfiles`/`uvicorn` style reloader (not included here).
* Published images are scanned and signed for security
* All published images support both amd64 and arm64 architectures
