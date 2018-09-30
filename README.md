# png-annotator
PNG annotator tool

This is very simple (under 300 lines of python) Tk-based image annotator that I created to help me mark and save coordinates of objects in images.

I've only tested it on Linux (Ubuntu 18).

# Screenshot and example output

![Alt text](screenshot.png?raw=true "Title")

Example output (saved as .txt next to original image file)
```
191.0, 148.0, 230.0, 194.0
238.0, 119.0, 262.0, 145.0
257.0, 131.0, 286.0, 154.0
271.0, 87.0, 298.0, 119.0
311.0, 76.0, 326.0, 96.0
228.0, 189.0, 278.0, 237.0
301.0, 175.0, 338.0, 223.0
344.0, 162.0, 443.0, 286.0
488.0, 250.0, 440.0, 310.0
504.0, 177.0, 466.0, 223.0
354.0, 124.0, 376.0, 146.0
369.0, 130.0, 402.0, 165.0
430.0, 141.0, 400.0, 166.0
392.0, 93.0, 416.0, 117.0
429.0, 112.0, 405.0, 135.0
449.0, 105.0, 478.0, 138.0
499.99999999999994, 87.0, 522.0, 114.0
```

# Usage

_Note: Python version must be >= 3.6_

### Running

python your_image.png

### Interacting

* Use `+`, `-` and `0` keys to zoom in, zoom out, or reset zoom, respectively.
* Use arrow keys to move around in the image.
* Use the mouse to draw rectangles on the image.
* Press `s` to save the currently drawn rectangles.
* Use `z` to remove the most-recently-drawn rectangle.

_PS: There is no "undo" action_

# License

MIT - see LICENSE file.

# Future work

* Support proper window resizing. Right now it's hard-coded to 600x400.
* Add ability to label rectangles (i.e. labelled regions).
* Add a small status bar that would show what the label of the rectangle is that the mouse is hovering over.
