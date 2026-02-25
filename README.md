# Icon Card Generator

A Python script that generates consistent, colored banner images from SVG icons. Originally created to generate thumbnails for BookStack book entries.

## Overview

This tool takes SVG icon files and generates 440×250px PNG images with:

- A solid background color
- A centered, recolored icon
- Consistent sizing and spacing

The default dimensions (440×250px) are specifically chosen for **BookStack book thumbnails**, which is what this tool was originally created for. BookStack is a simple, self-hosted wiki platform, and these dimensions provide optimal display quality for book cover images.

## Features

- **Batch processing**: Generate multiple icon cards from a single command
- **Flexible configuration**: JSON-based icon specifications
- **Customizable output**: Adjust dimensions, scale, and directories via CLI
- **Color control**: Set both icon and background colors per image
- **Simple workflow**: Just add SVG files and update the JSON config

## Requirements

- Python 3.7+
- Dependencies:
  - `cairosvg` - SVG to PNG conversion
  - `pillow` - Image manipulation
  - `cairocffi` - Required by cairosvg

## Installation

1. Clone this repository
2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate  # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Generate images with default settings (440×250px):

```bash
python generate_icon_cards.py
```

### CLI Options

```bash
python generate_icon_cards.py [OPTIONS]

Options:
  -w, --width WIDTH          Canvas width in pixels (default: 440)
  -H, --height HEIGHT        Canvas height in pixels (default: 250)
  -s, --scale SCALE          Icon scale relative to canvas, 0-1 (default: 0.75)
  -i, --input-dir PATH       Directory containing SVG files (default: script directory)
  -o, --output-dir PATH      Output directory for PNG files (default: ./generated-images)
  -c, --specs PATH           JSON file with icon specifications (default: ./icon_specs.json)
  -h, --help                 Show help message
```

### Examples

Generate with custom dimensions:

```bash
python generate_icon_cards.py -w 600 -H 400
```

Use custom directories and icon scale:

```bash
python generate_icon_cards.py -i ~/my-icons -o ~/output -s 0.6
```

Use a different config file:

```bash
python generate_icon_cards.py -c custom_icons.json
```

## Configuration

Icon specifications are defined in `icon_specs.json`:

```json
[
	{
		"file": "lock-solid-full.svg",
		"icon_color": "#ffffff",
		"background_color": "#1f2937"
	},
	{
		"file": "cloud-solid-full.svg",
		"icon_color": "#ffffff",
		"background_color": "#0ea5e9"
	}
]
```

### Configuration Fields

- **file**: SVG filename (must exist in input directory)
- **icon_color**: Hex color for the icon (e.g., `#ffffff` for white)
- **background_color**: Hex color for the canvas background

## Adding New Icons

1. Add your SVG file to the input directory (default: script directory)
2. Add an entry to `icon_specs.json`:
   ```json
   {
   	"file": "your-icon.svg",
   	"icon_color": "#ffffff",
   	"background_color": "#3b82f6"
   }
   ```
3. Run the script:
   ```bash
   python generate_icon_cards.py
   ```

Your new image will be generated at `generated-images/your-icon.png`

## Color Guidelines

For best results:

- Use contrasting colors between icon and background
- Test similar hues to avoid visual confusion
- White (`#ffffff`) icons work well with most background colors
- Consider your BookStack theme when choosing colors

## Output

Generated PNG files are saved to `generated-images/` (configurable with `-o`), with the same base name as the input SVG file.

## Use Case: BookStack Integration

This tool was designed for BookStack, a documentation/wiki platform. To use the generated images as book thumbnails in BookStack:

1. Generate your icon cards with default settings (440×250px)
2. Upload the PNG files through BookStack's book settings
3. The images will display perfectly as book cover thumbnails

The 440×250 aspect ratio provides optimal display in BookStack's book listing views while maintaining crisp quality.

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
