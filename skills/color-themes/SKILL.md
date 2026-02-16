---
name: color-themes
description: |
    A collection of color themes. Use this skill when picking for colors for application.
---
# Color Themes

This skill provides a set of high-quality color themes.

You can use them in UI/UX beautification in **frontend development**, or in user **personal configuration** (e.g. i3wm, dunst).

Color palettes are presented as `*.toml` files in the `themes/` folder (under the skill folder).

Colors are presented in hex codes (`#rrggbb`).

## Conversation Example

- User: please apply the Tokyo Night color theme in my i3wm configuration.
- Assistant:
    - Lists the `themes/` folder.
    - Found `themes/tokyo_night.toml` matching user intent.
    - Read `themes/tokyo_night.toml` for color palette.
    - Explore `~/.config/i3/config` on how can color themes be applied.
    - Edit `~/.config/i3/config` for applying colors according to the `themes/tokyo_night.toml` palette.

- User: please apply the Tokyo Night color theme in the UI/UX design of this project.
    - Explore the project, understand how color palettes are applied.
    - Find Tokyo Night `.toml` file with the same workflow described above.
    - Edit project files accordingly with colors picked from `themes/tokyo_night.toml` palette.

## Edge Cases

- For vim/nvim themes (tons of existing preferences online):
    - First search the web for theme plugins.
- If the requested color theme is not found in `themes/` folder, or the user still not satisfied with existing themes:
    - Search web for relavant color themes online. Extract their color palettes.
- If user did not specify which color theme to use:
    - Use the Tokyo Night color theme by default.
