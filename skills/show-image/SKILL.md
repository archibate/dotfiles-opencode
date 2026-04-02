---
name: show-image
description: Show images in terminal using the Kitty image protocol. TRIGGER when show/view images in terminal, display plot results, or after saving any plot or image file to disk.
disable-model-invocation: true
---

# Showing Image in Kitty Terminal

You are a CLI assistant running in **terminal**, potentially over SSH connections. You have **no access to X display**.

This skill provides a handy `scripts/show_image.py` tool to display image in user Kitty terminal thanks to the **Kitty image protocol**.

### CLI Usage

```bash
scripts/show_image.py /path/to/image.png
```

## Use Case

Use this skill when:
1. User ask to view image in their terminal.
2. Assistant want to show user some image.

### Example

Assistant: I've executed a plot script, plot result saved to `/path/to/image.png`.

User: please show me that image.

Assistant: Use show-image skill -> Run `scripts/show_image.py /path/to/image.png` -> Image appear in user terminal.

## How It Works

The user is using the Kitty terminal, which has a support for the **Kitty image protocol** - allowing to display high resolution images directly in terminal. This works even over SSH remote connections.

When `scripts/show_image.py` is called with an image, it automatically creates a new Kitty pane (if not created yet), running a show-image server, to constantly listen to all `scripts/show_image.py` calls, and display the images being passed as arguments.

The created Kitty pane for image display will be reused for future `scripts/show_image.py` invocations.

New invocations to `scripts/show_image.py` will stacks up in the image pane. The user is able to scroll up to see previous shown images.

Images shown previously are not updated automatically, rerun `scripts/show_image.py` when image updated.

Assume user have installed and using Kitty with remote control enabled. If they didn't, the script will fail with a clear error message reported.

### Why Split Pane?

You are a CLI assistant running in a TUI tool like Claude Code, which have rich TUI interface. If we show image directly in your running pane, the Claude Code TUI you live in would be severely interfered. Creating a new pane only for display prevents TUI being screwed up.

## Constrains

- Always use the `scripts/show_image.py` wrapper for showing image
- Do not use `kitty +kitten icat image.png` or `display image.png`
- Do not use this skill for showing non-image files
- Do not stack more than 3 images at once
