(ChatGPT generated)

# Video to ASCII Art Converter

This Python project converts video files into ASCII art frames. It can either save the frames as text files or play the ASCII video directly in the terminal.

## Features

- Converts video frames to ASCII art using custom grayscale mapping.
- Supports common video formats (mp4, mov, webm, etc.).
- Optionally save ASCII frames to disk.
- Optionally play ASCII video in the terminal.

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
python main.py --path <video_path> [--width WIDTH] [--save] [--play]
```

- `--path`: Path to the video file (required).
- `--width`: Width of the ASCII output (default: 100).
- `--save`: Save ASCII frames as text files in `ascii_videos/<video_name>/` folder.
- `--play`: Play the ASCII video in the terminal.

If neither `--save` nor `--play` is specified, the program will warn you and discard the output.

## Example

Convert and play video at width 120:

```
python main.py --path sample.mp4 --width 120 --play
```

Convert and save frames without playing:

```
python main.py --path sample.mp4 --save
```

## Notes

- Make sure your terminal supports monospace fonts for proper display.
- Larger widths increase resolution but require more processing time.
- The program currently supports only local video files.
