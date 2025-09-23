# Run in Containers (Podman/Docker)

This project ships with two containerized workflows:

* **Option A — Single container (default)**: quickest way to run the app locally.
* **Option B — Compose stack with Redis**: app + Redis backend for persistent memory.

Both options work with **Podman** or **Docker**. Commands below show Podman first; swap `podman` → `docker` if you prefer Docker.

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

## Option A — Single Container (no Redis)

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

## Option B — Compose Stack with Redis

This runs **two containers**: the app and a Redis service for the memory backend.

### 1) Compose file

Create `compose.yml` at the repo root:

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
    # (optional) add a healthcheck if you want the app to wait for Redis
    # healthcheck:
    #   test: ["CMD", "redis-cli", "ping"]
    #   interval: 5s
    #   timeout: 3s
    #   retries: 10
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

## Notes

* The container entrypoint runs: `python main.py`
* For local development with live-reload, prefer running directly on your host (venv) or consider a dev-specific image with `watchfiles`/`uvicorn` style reloader (not included here).
* When you later add CD, you can reuse the same image for a registry (GHCR, Quay, etc.).
