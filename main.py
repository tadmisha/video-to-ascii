import argparse
import pathlib
import cv2
import numpy
from time import sleep

#! Making image to ascii for now, proceed to video when finished

ascii_darkness = {0: ' ', 0.0751: '`', 0.0829: '.', 0.0848: '-', 0.1227: "'", 0.1403: ':', 0.1559: '_', 0.185: ',', 0.2183: '^', 0.2417: '=', 0.2571: ';', 0.2852: '>', 0.2902: '<', 0.2919: '+', 0.3099: '!', 0.3192: 'r', 0.3232: 'c', 0.3294: '*', 0.3384: '/', 0.3609: 'z', 0.3619: '?', 0.3667: 's', 0.3737: 'L', 0.3747: 'T', 0.3838: 'v', 0.3921: ')', 0.396: 'J', 0.3984: '7', 0.3993: '(', 0.4075: '|', 0.4091: 'F', 0.4101: 'i', 0.42: '{', 0.423: 'C', 0.4247: '}', 0.4274: 'f', 0.4293: 'I', 0.4328: '3', 0.4382: '1', 0.4385: 't', 0.442: 'l', 0.4473: 'u', 0.4477: '[', 0.4503: 'n', 0.4562: 'e', 0.458: 'o', 0.461: 'Z', 0.4638: '5', 0.4667: 'Y', 0.4686: 'x', 0.4693: 'j', 0.4703: 'y', 0.4833: 'a', 0.4881: ']', 0.4944: '2', 0.4953: 'E', 0.4992: 'S', 0.5509: 'w', 0.5567: 'q', 0.5569: 'k', 0.5591: 'P', 0.5602: 'h', 0.565: '9', 0.5776: 'd', 0.5777: '4', 0.5818: 'V', 0.587: 'p', 0.5972: 'O', 0.5999: 'G', 0.6043: 'b', 0.6049: 'U', 0.6093: 'A', 0.6099: 'K', 0.6465: 'X', 0.6561: 'H', 0.6595: 'm', 0.6631: '8', 0.6714: 'R', 0.6759: 'D', 0.6809: '#', 0.6816: '$', 0.6925: 'B', 0.7039: 'g', 0.7086: '0', 0.7235: 'M', 0.7302: 'N', 0.7332: 'W', 0.7602: 'Q', 0.7834: '%', 0.8037: '&', 1: '@'}
darknesses = list(ascii_darkness.keys())

#& Checking if file exists & format is right
def check_path(path: str) -> bool:
    extensions = [".mp4", ".mov", ".webm", ".mpg", ".ogg", ".avi", ".flv"]
    if not any([path.endswith(ext) for ext in extensions]):
        return False

    if not pathlib.Path(path).exists():
        return False
    
    return True


#& Image to rayscale
def to_grayscale(img: numpy.ndarray) -> numpy.ndarray:
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray_img


#& Function that turns an image to ASCII art
def image_to_ascii(img: numpy.ndarray, new_width: int = 100) -> str:
    gray_img = to_grayscale(img)
    new_height = int(new_width*len(gray_img)/1.5//len(gray_img[0]))
    resized_gray_img = cv2.resize(gray_img, (new_width, new_height))
    
    ascii_str = ""
    for row in range(new_height):
        for col in range(new_width):
            darkness = resized_gray_img[row][col]/255
            for i in range(len(ascii_darkness)-1):
                if darknesses[i]<=darkness<=darknesses[i+1]:
                    ascii_str += ascii_darkness[darknesses[i+1]]
                    break
        ascii_str+='\n'

    return ascii_str


#& Main function
def main(path: str, width: int, save: bool, play: bool):
    if not (save or play):
        print("Warning: neither --save nor --play specified. Output will be discarded.")
        if input("Do you want to continue? Type anything if not: "):
            return

    if not check_path(path):
        print("Couldn't open the file")
        return False
    
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1/fps

    if not cap.isOpened():
        print("Couldn't open the file")
        return False

    frames_ascii = []

    frame_idx = -1
    while cap.isOpened():
        frame_idx+=1
        ret, frame = cap.read()
        if not ret:
            break
        frames_ascii.append(image_to_ascii(frame, width))
        print(f"Frame N{frame_idx} converted")
    
    if save:
        folder_name = path.split('.')[0]
        if pathlib.Path(f"ascii_videos/{folder_name}").exists():
            i = 1
            folder_name=f"{folder_name}{i}"
            while pathlib.Path(f"ascii_videos/{folder_name}").exists():
                folder_name=f"{folder_name[:-(len(str(i-1)))]}{i}"
                i+=1
        pathlib.Path(f"ascii_videos/{folder_name}").mkdir()

        for idx in range(len(frames_ascii)):
            with open(f"ascii_videos/{folder_name}/frame{idx}", 'w') as file:
                file.write(frames_ascii[idx])
    
    if play:
        for frame_ascii in frames_ascii:
            print('\n'*100)
            print(frame_ascii)
            sleep(frame_delay)


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(description="Convert video to ASCII art")
    parser.add_argument("--path", type=str, required=True, help="Path to the video file")
    parser.add_argument("--width", type=int, default=100, help="Width of ASCII output")
    parser.add_argument("--save", action="store_true", help="Save ASCII frames to a folder")
    parser.add_argument("--play", action="store_true", help="Play the video in the terminal")
    args = parser.parse_args()

    main(args.path, args.width, args.save, args.play)