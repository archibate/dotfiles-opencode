---
name: neovim-guide
description: |
    Use when user mentioned neovim.
---
# NeoVim Manipulation

The user mainly use NeoVim for editing file.

You are equipped with `nvim_*` tools, which have powerful ability to manipulate NeoVim sessions and buffers.

> Powered by [nvim-mcp](https://github.com/linw1995/nvim-mcp).

## Context Retrive

When user mentioned 'this file', 'current file', 'this script', 'this function' without previous context:

**Intent:** The user might be indicating the **currently opening file in NeoVim**.

**Steps:**
- Run `nvim_get_targets` then `nvim_connect` to connect the relevant session.
- Run `nvim_list_buffers` and `nvim_cursor_position` tools to retrive NeoVim context.
- Run `nvim_read` to read NeoVim buffers.

**Fallback:**
If no NeoVim session found, ask the user for disambiguation.

## Navigate to Files

When user ask for editor navigations like 'open it in my editor', 'reveal the location of X', 'jump to the Y function':

**Intent:** The user might mean to open the mentioned location in current running NeoVim.

- Run `nvim_get_targets` then `nvim_connect` to connect the relevant session.
- Run `nvim_navigate` tools to navigate NeoVim to the user mentioned location.

**Fallback:**
If no NeoVim session found:
- Try run `test -n "$TMUX" && tmux split-window -h "nvim <file>" || echo "Not running in Tmux"`.
- If not running in Tmux, tell the file location directly in text response.

**CRITICAL:** NEVER run `nvim <file>` command directly in Bash.
