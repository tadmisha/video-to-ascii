import argparse
import pathlib
import cv2
import numpy
from time import sleep

#! Making image to ascii for now, proceed to video when finished

ascii_darkness = {0.0: ' ', 0.0762: '`', 0.0851: '.', 0.0881: '-', 0.1271: "'", 0.1458: ':', 0.1624: '_', 0.1926: ',', 0.227: '^', 0.2515: '=', 0.268: ';', 0.2972: '>', 0.3033: '<', 0.3061: '+', 0.3252: '!', 0.3356: 'r', 0.3406: 'c', 0.3479: '*', 0.358: '/', 0.3816: 'z', 0.3837: '?', 0.3896: 's', 0.3977: 'L', 0.3998: 'T', 0.41: 'v', 0.4194: ')', 0.4244: 'J', 0.4278: '7', 0.4298: '(', 0.4391: '|', 0.4418: 'F', 0.4439: 'i', 0.4549: '{', 0.459: 'C', 0.4618: '}', 0.4656: 'f', 0.4686: 'I', 0.4732: '3', 0.4796: '1', 0.481: 't', 0.4856: 'l', 0.492: 'u', 0.4935: '[', 0.4972: 'n', 0.5042: 'e', 0.5071: 'o', 0.5112: 'Z', 0.5151: '5', 0.519: 'Y', 0.522: 'x', 0.5238: 'j', 0.5259: 'y', 0.54: 'a', 0.5459: ']', 0.5533: '2', 0.5553: 'E', 0.5603: 'S', 0.6131: 'w', 0.62: 'q', 0.6212: 'k', 0.6245: 'P', 0.6267: 'h', 0.6326: '9', 0.6463: 'd', 0.6475: '4', 0.6527: 'V', 0.659: 'p', 0.6703: 'O', 0.6741: 'G', 0.6795: 'b', 0.6812: 'U', 0.6867: 'A', 0.6884: 'K', 0.7261: 'X', 0.7368: 'H', 0.7413: 'm', 0.746: '8', 0.7554: 'R', 0.761: 'D', 0.7671: '#', 0.7688: '$', 0.7808: 'B', 0.7933: 'g', 0.7991: '0', 0.8151: 'M', 0.8229: 'N', 0.827: 'W', 0.8551: 'Q', 0.8794: '%', 0.9008: '&', 1: '@'}
darknesses = list(ascii_darkness.keys())

#& Checking if file exists & format is right
def check_path(path: str, is_video: bool) -> bool:
    extensions = [".mp4", ".mov", ".webm", ".mpg", ".ogg", ".avi", ".flv"] if is_video else \
                 [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".svg"]

    if not any([path.endswith(ext) for ext in extensions]):
        return False

    if not pathlib.Path(path).exists():
        return False
    
    return True


#& Image to rayscale
def to_grayscale(img: numpy.ndarray) -> numpy.ndarray:
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray_img


#& Function that turns an image to ascii art
def image_to_ascii(img: numpy.ndarray, new_width: int = 100) -> str:
    gray_img = to_grayscale(img)

    new_height = int(new_width*len(gray_img)/1.5//len(gray_img[0]))
    if new_height == 0: new_height = 1 # ? In extreme thin ratios cases

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

#& Function that converts video to ascii frame by frame
def video_to_ascii(cap: cv2.VideoCapture, new_width: int = 100):
    frames_ascii = []
    frames_len = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print()

    frame_idx = -1
    while cap.isOpened():
        frame_idx+=1
        ret, frame = cap.read()
        if not ret:
            break
        frames_ascii.append(image_to_ascii(frame, new_width))
        print(f"Progress - {frame_idx/frames_len*100:.2f}%\n")
        print(f"Frame N{frame_idx}/{frames_len} converted")
        print("\033[F"*3, end='')
    
    return frames_ascii


#& Creates a directory for converted to ascii image/video to be saved in and returns the path to it
def makedir_for_saving_ascii(path: str, is_video: bool) -> str:
    base_folder = "ascii_" + ("videos" if is_video else "images")

    folder_name = pathlib.Path(path).stem 
    if pathlib.Path(f"{base_folder}/{folder_name}").exists():
        i = 1
        folder_name=f"{folder_name}{i}"
        while pathlib.Path(f"{base_folder}/{folder_name}").exists():
            folder_name=f"{folder_name[:-(len(str(i-1)))]}{i}"
            i+=1

    pathlib.Path(f"{base_folder}/{folder_name}").mkdir()

    return f"{base_folder}/{folder_name}"


#& Main function
def main(is_video: bool, is_image: bool, path: str, width: int, save: bool, play: bool):
    if not (is_image ^ is_video): # ! If nor --image nor --video were specified or both were
        print("Choose either --video or --image to be converted.")
        return

    if not (save or play): # ! If nor --save nor --play were specified
        print("Warning: neither --save nor --play specified. Output will be discarded.")
        if input("Do you want to continue? Type anything if not: "):
            return

    if not check_path(path, is_video): # ! Checking if can open a file
        print("Couldn't open the file")
        return False
    
    if is_image: # ! Converting if input is an image
        img = cv2.imread(path)
        if img is None:
            print("Cannot convert a corrupt file.")
            return

        frames_ascii = [image_to_ascii(img, width)]
        frame_delay = 0
    
    if is_video: # ! Converting if input is a video
        cap = cv2.VideoCapture(path)

        fps = cap.get(cv2.CAP_PROP_FPS)

        if fps == 0: # ? If some weird metadata issue when fps = 0
            fps = 30

        frame_delay = 1/fps

        if not cap.isOpened():
            print("Couldn't open the file")
            return False

        frames_ascii = video_to_ascii(cap, width)
    
    if save: # ! Saving
        savepath = makedir_for_saving_ascii(path, is_video)

        if is_video: # ? Saving fps if video
            with open(f"{savepath}/fps.txt", 'w') as file:
                file.write(str(fps))

        # ? Saving all the frames
        for idx in range(len(frames_ascii)):
            with open(f"{savepath}/frame{idx}.txt", 'w') as file:
                file.write(frames_ascii[idx])
    
    if play: # ! Playing
        for frame_ascii in frames_ascii:
            print('\n'*100)
            print(frame_ascii)
            sleep(frame_delay)


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(description="Convert video to ASCII art")
    parser.add_argument("--path", type=str, required=True, help="Path to the image/video file")
    parser.add_argument("--width", type=int, default=100, help="Width of ASCII output")
    parser.add_argument("--save", action="store_true", help="Save ASCII frame(s) to a folder")
    parser.add_argument("--play", action="store_true", help="Play the image/video in the terminal")
    parser.add_argument("--video", action="store_true", help="Convert a video")
    parser.add_argument("--image", action="store_true", help="Convert an image")
    args = parser.parse_args()

    main(args.video, args.image, args.path, args.width, args.save, args.play)