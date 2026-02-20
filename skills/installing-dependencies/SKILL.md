---
name: installing-dependencies
description: Use before installing dependencies, packages, or tools required for building project.
---

# Installing Dependencies

## The Golden Rule

**If the install command writes anything outside the current project directory, stop and ask the user for permission first.**

This is non-negotiable. No exceptions.

## Decision Gate

Before running any install command, ask:

```
Does this command write outside the project directory?
  YES -> Ask user for permission. Do not proceed until granted.
  NO  -> Proceed.

Is there no virtual environment / local package setup yet?
  YES -> Initialize one first, then install.
  NO  -> Install into the existing local environment.
```

## Per-Ecosystem Rules

### Python

```
# Initialize venv if not present
uv venv          # preferred
python -m venv .venv

# Install into venv
uv add <pkg>
uv pip install <pkg>
.venv/bin/pip install <pkg>
```

```
# NEVER without permission
pip install <pkg>           # writes to system Python
pip install --user <pkg>    # writes to ~/.local
```

### Node.js

```
# Install locally (default behavior)
npm install <pkg>
npm install --save-dev <pkg>
bun add <pkg>
bun add -d <pkg>
```

```
# NEVER without permission
npm install -g <pkg>        # writes to system node_modules
bun add -g <pkg>
```

### Rust

```
# Add as project dependency
cargo add <pkg>
```

```
# NEVER without permission
cargo install <pkg>         # writes to ~/.cargo/bin
```

### System / OS-level tools

```
# NEVER without permission
sudo apt install <pkg>
brew install <pkg>
pip install <pkg>           # system pip
```

System-level tools (runtimes, compilers, CLI utilities) always require explicit user permission. If a required tool is missing, inform the user and ask them to install it rather than installing it yourself.

## What "Outside the Project Directory" Means

Any path that is not under the current working project folder, including:

- `~/.local`
- `~/.cargo`
- `/usr/local`
- `/usr/lib`
- Global `node_modules`
- System Python site-packages

## Asking for Permission

State clearly:
1. What you want to install
2. Where it will be written
3. Why it is needed

Wait for explicit approval before proceeding.
