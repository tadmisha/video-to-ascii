# Video & Image to ASCII Art Converter

This Python project converts **video or image files** into ASCII art frames. It can either save the frames as text files or play the ASCII output directly in the terminal.

## Features

- Converts images or video frames to ASCII art using a custom grayscale mapping.
- Supports common video formats (`.mp4`, `.mov`, `.webm`, `.avi`, etc.) and image formats (`.jpg`, `.png`, `.gif`, `.bmp`, etc.).
- Optionally save ASCII frames to disk.
- Optionally play ASCII output in the terminal.
- Handles corrupt or unsupported files gracefully.
- Automatically creates unique folders when saving ASCII outputs to prevent overwriting.

## Requirements

- Python 3.8+
- OpenCV (`cv2`)
- NumPy

Install dependencies using:

```
pip install -r requirements.txt
```

## Usage

Run the script with the following command line options:

```
python main.py --srcpath <file_path> [--dstpath <destination_path>] [--width WIDTH] [--save] [--play] [--video | --image]
```

- `--srcpath`: Path to the image or video file (**required**).
- `--dstpath`: Destination directory to save ASCII output (default: `ascii_images/` or `ascii_videos/`).
- `--width`: Width of the ASCII output (default: 100).
- `--save`: Save ASCII frames as text files in `ascii_images/<image_name>/` or `ascii_videos/<video_name>/` folder.
- `--play`: Play the ASCII output in the terminal.
- `--video`: Convert a video file.
- `--image`: Convert an image file.

**Important:** You must specify either `--video` or `--image`, but not both.

If neither `--save` nor `--play` is specified, the program will warn you and discard the output.

## Examples

Convert and play a video at width 120:

```
python main.py --srcpath sample.mp4 --width 120 --video --play
```

Convert and save an image without playing:

```
python main.py --srcpath sample.jpg --image --save
```

## Notes

- Make sure your terminal supports monospace fonts for proper display.
- Larger widths increase resolution but require more processing time.
- The program currently supports only local image/video files.
- Videos are converted frame by frame; FPS information is saved in `fps.txt` if `--save` is used.
