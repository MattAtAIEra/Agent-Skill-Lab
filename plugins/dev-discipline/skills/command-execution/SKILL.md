---
name: command-execution
description: This skill should be used when executing shell commands, "running terminal commands", "starting a dev server", "running build or test commands", or any Bash tool invocation. Prevents blind retries and ensures proper error analysis before reattempting.
version: 1.0.0
---

# Command Execution Discipline

When executing any shell command, follow these rules to avoid wasting resources on blind retries and creating confusion.

## Core Principle

**Execute once -> Check the result -> Analyze the cause -> Then decide next steps**

Never re-run the same command without confirming the result of the previous execution.

## Pre-Execution Checks

### 1. Confirm the Working Directory

Before running a command, verify the current working directory is correct:

- Project root vs subdirectory (e.g., `app/`, `packages/web/`)
- Does the command need to run in a specific directory? (e.g., `nuxt dev` requires the directory containing `nuxt.config.ts`)
- Use absolute paths or `--cwd` flags to avoid directory mistakes

Bad example:

```bash
# Running from project root, but nuxt.config.ts is in app/
npx nuxt dev --port 3333
```

Good example:

```bash
# Explicitly specify the correct directory
cd /project/app && npx nuxt dev --port 3333
# Or use the cwd flag
npx nuxt dev --cwd /project/app --port 3333
```

### 2. Confirm Prerequisites

- Are dependent services running? (e.g., database, other servers)
- Are environment variables set?
- Are dependencies installed? (does `node_modules` exist?)
- Is the port already in use?

## Post-Execution Checks

### 3. Check the Execution Result

After every command execution, **always** confirm the result:

- Check exit code (0 = success, non-zero = failure)
- Read stdout/stderr output
- For background processes, check log files to confirm successful startup

Correct flow for starting a background process:

```bash
# 1. Start
some-server > /tmp/server.log 2>&1 &

# 2. Wait for startup
sleep 3

# 3. Check logs to confirm success
cat /tmp/server.log

# 4. Or use a health check
curl -s -o /dev/null -w "%{http_code}" http://localhost:3333/
```

### 4. Failure Handling Flow

When a command fails, follow this order:

1. **Read the full error message** — do not just look at the last line
2. **Analyze the root cause** — wrong directory? Missing dependency? Port conflict? Permission issue?
3. **Formulate a fix** — target the root cause, do not blindly retry
4. **Retry after applying the fix** — change one thing at a time, then verify

Prohibited behaviors:

- Retrying without reading the error message
- Running the same command more than 2 consecutive times
- Adding `--force` or `sudo` to bypass errors without understanding the cause
- Starting multiple identical background processes simultaneously

## Cleanup Responsibility

### 5. Background Process Management

Before starting a background process, check if an identical process is already running:

```bash
# Check if nuxt dev is already running
ps aux | grep "nuxt dev" | grep -v grep

# If so, stop it first then restart
pkill -f "nuxt dev --port 3333"
sleep 1
```

Record the PID after starting a process, and clean up when the work is done.

## Special Scenarios

### Dev Server Startup

1. Confirm the working directory contains the framework config file
2. Confirm the port is not already in use
3. Start in background and wait
4. Check logs for "ready" or "listening"
5. Final confirmation via curl health check

### Database Operations

1. Confirm the database service is running
2. Confirm connection parameters are correct
3. Before execution, confirm the scope of impact (DROP will delete all data)
4. Check execution result, confirm no errors

### Test Execution

1. Confirm the test environment is ready (dev server, DB)
2. Run a small batch first to verify the environment is working
3. Then run the full test suite
4. On failure, analyze each case individually — do not re-run hoping it "fixes itself"

## Self-Check

Before every Bash tool invocation, answer these questions:

1. Am I in the correct directory?
2. Are all prerequisites satisfied?
3. Have I confirmed the result of the last execution?
4. If it failed, do I know why?
