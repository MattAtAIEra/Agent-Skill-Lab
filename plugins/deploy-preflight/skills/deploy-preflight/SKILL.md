---
name: deploy-preflight
description: This skill should be used when the user asks to "generate a setup script", "create a deploy script", "write a deployment script", "deploy to EC2", "deploy to production", "setup production server", "write setup.sh", "create deploy.sh", or discusses deploying a project to a remote server. Ensures deployment scripts include proper environment checks and safeguards.
version: 1.0.0
---

# Production Deploy Preflight Check

Before generating or modifying any deployment script (e.g. `setup.sh`, `deploy.sh`), collect the target host's environment information and diagnose potential risks. Integrate safeguards into the script automatically.

## Procedure

### Step 1: Collect Target Environment Info

Ask the user for the following details (skip any already known):

1. **Cloud provider & instance type** — e.g. AWS EC2 t3.micro, GCP e2-micro
2. **OS version** — e.g. Amazon Linux 2023, Ubuntu 24.04
3. **Memory size** — ask the user to run `free -h` if unknown
4. **Swap status** — ask the user to run `swapon --show`
5. **Disk space** — ask the user to run `df -h /`
6. **Node.js version** — `node -v` (if applicable)
7. **Terminal multiplexer** — whether tmux or screen is installed (prevents SSH disconnect issues during long-running scripts)

Present a concise checklist and wait for the user's response before proceeding.

### Step 2: Produce Diagnostic Report

Based on collected information, produce a risk assessment table:

| Item | Value | Risk Level |
|------|-------|------------|
| RAM | <= 1 GB | **HIGH** — `pnpm install` / `next build` likely to OOM |
| RAM | 1-2 GB | **MEDIUM** — recommend adding swap |
| RAM | >= 2 GB | LOW |
| Swap | None | **HIGH** — must configure before build |
| Disk | < 5 GB free | **HIGH** — `node_modules` + `.next` may fill disk |
| tmux/screen | Not installed | **WARN** — recommended for long-running scripts |

Mark each item with the appropriate risk level. Summarize overall deployment readiness.

### Step 3: Integrate Safeguards into Script

Based on the diagnostic results, prepend the following safeguard blocks to the deployment script. Place them before all other steps.

#### Low Memory Protection (RAM <= 2 GB without swap)

```bash
# -- Check & Create Swap (low-memory environment) --
TOTAL_MEM_MB=$(free -m | awk '/^Mem:/{print $2}')
if [ "$TOTAL_MEM_MB" -lt 2048 ] && [ ! -f /swapfile ]; then
  echo "[preflight] Memory ${TOTAL_MEM_MB}MB detected, creating 2GB swap..."
  sudo fallocate -l 2G /swapfile
  sudo chmod 600 /swapfile
  sudo mkswap /swapfile
  sudo swapon /swapfile
  echo '/swapfile swap swap defaults 0 0' | sudo tee -a /etc/fstab
fi
```

#### Terminal Multiplexer Check

```bash
# -- Check for tmux/screen (prevents SSH disconnect issues) --
if ! command -v tmux &>/dev/null && ! command -v screen &>/dev/null; then
  echo "[preflight] WARNING: tmux/screen not found."
  echo "  Install: sudo dnf install -y tmux  (or sudo apt install -y tmux)"
  echo "  Then run this script inside: tmux new -s deploy"
fi
```

#### Disk Space Check

```bash
# -- Check disk space --
AVAIL_GB=$(df -BG / | awk 'NR==2{print $4}' | tr -d 'G')
if [ "$AVAIL_GB" -lt 5 ]; then
  echo "[preflight] ERROR: Only ${AVAIL_GB}GB free disk space. Need at least 5GB."
  exit 1
fi
```

#### Node.js Version Check (when applicable)

```bash
# -- Check Node.js version --
if command -v node &>/dev/null; then
  NODE_VER=$(node -v | tr -d 'v' | cut -d. -f1)
  if [ "$NODE_VER" -lt 18 ]; then
    echo "[preflight] WARNING: Node.js v${NODE_VER} detected. v18+ recommended."
  fi
else
  echo "[preflight] Node.js not found. Install it before proceeding."
  exit 1
fi
```

### Step 4: Output Final Script

Assemble the complete deployment script with safeguards at the top. Include a reminder to the user:

- Run inside a tmux session: `tmux new -s deploy`
- The script auto-detects and handles swap creation
- Review the diagnostic report before executing

## Safeguard Selection Logic

Only include safeguards relevant to the diagnosed risks:

- **RAM <= 2 GB + no swap** -> include swap creation block
- **Disk < 5 GB** -> include disk space check
- **No tmux/screen** -> include multiplexer warning
- **Node.js project** -> include Node.js version check
- **All clear** -> note that no additional safeguards are needed, proceed with standard script

## Output Format

Structure the final output as:

1. **Diagnostic Report** — risk assessment table
2. **Recommended Actions** — what to fix before deploying
3. **Generated Script** — complete script with integrated safeguards
4. **Execution Instructions** — how to run the script safely

## Scope Boundaries

This skill covers pre-deployment environment validation only. It does not handle:

- Application-level configuration (env vars, secrets)
- CI/CD pipeline setup
- Container or Kubernetes deployments
- SSL certificate provisioning

For these concerns, defer to the user or other specialized skills.
