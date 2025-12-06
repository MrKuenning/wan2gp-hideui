# WAN2GP Hide UI Plugin

This is a plugin for the [WAN2GP](https://github.com/deepbeepmeep/Wan2GP) application that adds a floating menu to the user interface. This menu allows you to toggle the visibility of various UI elements, making it easier to focus on specific sections of the interface, especially on mobile devices.

![compact_example](https://github.com/user-attachments/assets/73dd5c32-4b60-48ae-8baf-db2423dc1b87)

## Features

- **Floating Menu:** A convenient, collapsible menu that floats on the bottom right of the screen.
- **UI Element Toggling:** Show or hide specific UI elements, such as:
  - Header
  - Model Selector
  - Model Info
  - Input Options
  - Text Image Options
  - Enhance Prompt
  - Resolution Options
  - Number of Frames
  - Inference Steps
  - Settings Buttons
  - Load from Video
  - Download LoRA
  - Video Info
- **Show/Hide All:** Quickly toggle the visibility of all supported UI elements.
- **Safe Hiding:** The plugin safely hides elements and collapses empty parent containers to reclaim screen space without breaking the Gradio layout.

## Installation

1.  Clone the repository or make a folder called wan2gp-hideUI in the plugins folder for wan2gp and place the `plugin.py` file into the folder.
2.  Restart the WAN2GP application.

## How to Use

Once installed, a "☰ UI" button will appear in the bottom right corner of the WAN2GP interface. Click this button to open the menu.

The menu contains a list of checkboxes corresponding to different UI elements. Uncheck a box to hide the corresponding element, and check it to show it again. The "Show/Hide All" checkbox at the top of the menu can be used to toggle all elements at once.

Click the "✕ Close" button to close the menu.

### Changing Default Visibility

The plugin comes with a mix of items that are visible and hidden by default to provide a balanced starting interface. You can customize which items are visible or hidden by default by editing the `plugin.py` file.

In the `plugin.py` file, locate the `TARGETS` list within the `inject_floating_buttons_js` function. For each element, the `default` property controls its initial state:
- `default: true` makes the item visible by default.
- `default: false` makes the item hidden by default.

For example, to make the "Header" visible by default, you would change its entry from `false` to `true`:

```python
// From (hidden by default):
{'id': 'header', 'labels': ['Header'], 'name': 'Header', 'default': false},

// To (visible by default):
{'id': 'header', 'labels': ['Header'], 'name': 'Header', 'default': true},
```

Conversely, to hide an item like the "Model Selector" by default, you would change its `default` property from `true` to `false`.

Save the file and restart the WAN2GP application for the changes to take effect.

## Configuration

The plugin can be configured by editing the `plugin.py` file. The `TARGETS` list at the top of the `inject_floating_buttons_js` function defines the UI elements that can be toggled. You can modify this list to add or remove elements, or change their default visibility.

Each entry in the `TARGETS` list is an object with the following properties:

-   `id`: A unique identifier for the element.
-   `labels`: A list of strings used to identify the element in the UI.
-   `name`: The name of the element as it appears in the floating menu.
-   `default`: The initial visibility of the element (`true` for visible, `false` for hidden).
