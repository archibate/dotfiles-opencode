---
name: setup-fresh-project
description: |
    Use this when setting up a fresh new project.
---
# Fresh Project Setup Guide

Use this skill when you are starting to write code in a fresh project.

## Setup Steps

1. Check if already initialized with git -> not yet? run `git init`.
2. Create a `.gitignore` suitable for tech stack of choices (e.g. `__pycache__` for Python, `node_modules` for Node).
3. Create style and formatting configurations (e.g. `.stylua.toml` for Lua, `pyproject.toml` + Ruff for Python). Default to 4 spaces for tab.
4. Make sure basic tools required are available in system (e.g. `stylua`, `npm`, `uv`). If not, explicitly ask the user to install.
5. Set up LSP configurations for OpenCode.

## Language Specific

Ask user for tech stack choices. Offer default choices:

### Python

Prefer `uv` (with `venv`) and `ruff`.

#### Pyright LSP

If you are using `venv`, to prevent LSP errors about 'package not found', create `pyrightconfig.json` with content:

```json
{
    "venvPath": ".",
    "venv": ".venv"
}
```

### Typescript

Prefer `biome` and `npm` (or `bun`).

### Lua

Prefer `stylua`.

#### NeoVim Lua Projects

If the Lua project is used as a NeoVim configuration or plugin:

Create a `.luarc.json` with content:

```json
{
    "runtime.version": "LuaJIT",
    "runtime.path": [
        "lua/?.lua",
        "lua/?/init.lua"
    ],
    "diagnostics.globals": ["vim"],
    "workspace.checkThirdParty": false,
    "workspace.library": [
        "$VIMRUNTIME"
    ]
}
```

### C/C++

Prefer `clang`, `cmake` and `clang-format`.

#### Clangd LSP

Make sure to use `cmake -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON` when build (or add `set(CMAKE_EXPORT_COMPILE_COMMANDS ON)` to `CMakeLists.txt`). This will create `build/compile_commands.json`, for `clangd` to not reporting false positive errors about include header missing.

## Folder Structure

Follow industry best pratice of project folder structure most suitable the tech stack.

e.g.:
- `src/`, `tests/`, `dist/` for Python & PyTest project.
- `src/`, `include/`, `build/` for C++ & CMake project.
- `lua/` for NeoVim Lua plugin project.

A `.gitignore` and `README.md` is always required for all projects.

### Documentation

Main documentation resides in `README.md`. With a simple and clear introduction on how to use this project, including but not limited to the following perspectives:

- What is this?
- Project structure?
- How to build?
- How to test?
- How to install or deploy?
- ...

`README.md` must be presented in a clear, structured markdown format. No placeholders.

`README.md` focus on big-picture. Optionally create `.md` under `docs/` for more detailed documentation and refer them in `README.md`.

If this is to be a public project (potentially upload to github), not for personal use:
- Make sure no hard-coded user path (e.g. `/home/bate/project`) in `README.md` and other documents.
- Make sure no invalid fake link used in `README.md` and other documents (e.g. `[Screenshot](screenshot.png)` but actually no such file).
- Make sure no hard-coded user credentials (e.g. API keys, tokens, or password) in any files tracked by git.
