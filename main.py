import pathlib
import cv2
import numpy

#! Making image to ascii for now, proceed to video when finished

ascii_darkness = {' ': 0, '`': 0.0751, '.': 0.0829, '-': 0.0848, "'": 0.1227, ':': 0.1403, '_': 0.1559, ',': 0.185, '^': 0.2183, '=': 0.2417, ';': 0.2571, '>': 0.2852, '<': 0.2902, '+': 0.2919, '!': 0.3099, 'r': 0.3192, 'c': 0.3232, '*': 0.3294, '/': 0.3384, 'z': 0.3609, '?': 0.3619, 's': 0.3667, 'L': 0.3737, 'T': 0.3747, 'v': 0.3838, ')': 0.3921, 'J': 0.396, '7': 0.3984, '(': 0.3993, '|': 0.4075, 'F': 0.4091, 'i': 0.4101, '{': 0.42, 'C': 0.423, '}': 0.4247, 'f': 0.4274, 'I': 0.4293, '3': 0.4328, '1': 0.4382, 't': 0.4385, 'l': 0.442, 'u': 0.4473, '[': 0.4477, 'n': 0.4503, 'e': 0.4562, 'o': 0.458, 'Z': 0.461, '5': 0.4638, 'Y': 0.4667, 'x': 0.4686, 'j': 0.4693, 'y': 0.4703, 'a': 0.4833, ']': 0.4881, '2': 0.4944, 'E': 0.4953, 'S': 0.4992, 'w': 0.5509, 'q': 0.5567, 'k': 0.5569, 'P': 0.5591, '6': 0.5602, 'h': 0.5602, '9': 0.565, 'd': 0.5776, '4': 0.5777, 'V': 0.5818, 'p': 0.587, 'O': 0.5972, 'G': 0.5999, 'b': 0.6043, 'U': 0.6049, 'A': 0.6093, 'K': 0.6099, 'X': 0.6465, 'H': 0.6561, 'm': 0.6595, '8': 0.6631, 'R': 0.6714, 'D': 0.6759, '#': 0.6809, '$': 0.6816, 'B': 0.6925, 'g': 0.7039, '0': 0.7086, 'M': 0.7235, 'N': 0.7302, 'W': 0.7332, 'Q': 0.7602, '%': 0.7834, '&': 0.8037, '@': 0.9999}


#& Function that splits the number n in k amount of numbers with them being int and then spreads them evenly in a list
#& Example: input: n=81, k=13 output: [7, 6, 6, 6, 7, 6, 6, 6, 6, 7, 6, 6, 6]
def split_and_spread(n: int , k: int) -> list[int]:
    base = n // k
    add = n % k

    result = [base] * k

    if not add: return result

    space = k / add
    for i in range(add):
        index = round(i*space)
        result[index] += 1
    return result


#& Checking if file exists & format is right
def check_path(path: str) -> bool:
    if not (path.endswith(".jpg") or path.endswith(".jpeg") or path.endswith(".png") or path.endswith(".webp")):
        return False
    if not pathlib.Path(path).exists():
        return False
    return True


#& Image to rayscale
def to_grayscale(img: numpy.ndarray) -> numpy.ndarray:
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray_img


#& Shrink width of image to needed
def shrink_w(gray_img: numpy.ndarray, new_w: int) -> numpy.ndarray:
    current_h = len(gray_img)
    current_w = len(gray_img[0])

    spread = split_and_spread(current_w, new_w)

    for row_i in range(current_h):
        i=0
        for s in spread:
            gray_img[row_i][i:s+1]=sum(gray_img[row_i][i:s+i])/s
        i+=1
    
    return gray_img







def main():
    new_w = 200
    
    path = "image.png"
    if not check_path(path):
        print("Couldn't open the file")
        return False
    
    img = cv2.imread(path)
    gray_img = to_grayscale(img)
    small = cv2.resize(gray_img, (0,0), fx=, fy=0.25) 
    cv2.imshow("s",small)
    cv2.waitKey(0)


    

if (__name__ == "__main__"):
    main()