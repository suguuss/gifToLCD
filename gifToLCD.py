#------------------------------------------------------------
#   Projet  : gifToLCD.py
#   Nom     : 
#   Date    : 16.10.2019 
#------------------------------------------------------------
#   Description :   Creates a .h file with all the frames
#                   from a choosen gif
#------------------------------------------------------------


#------------------------------------------------------------
#   IMPORT
#------------------------------------------------------------
from PIL import Image
from cv2 import resize, imwrite, imread
from os import mkdir, listdir 
from natsort import natsorted
from sys import exit
from time import sleep


#------------------------------------------------------------
#   DEFINE
#------------------------------------------------------------
WIDTH = 128
HEIGHT = 64


#------------------------------------------------------------
#   ExtractImage()
#------------------------------------------------------------
#   Description : Extract all the frame from a gif
#------------------------------------------------------------
#   Input  : Gif from which frames are gonna be extracted
#   Output : Creates a folder with all the images
#------------------------------------------------------------
def ExtractImage(filename):
    print("\nExtracting the frames...")

    try:
        mkdir(OUTFILE)
        im = Image.open(filename)
        for x in range(im.n_frames):
            if x == 60:
                break
            try:
                current = im.tell()
                im.convert('RGB').save(f"{OUTFILE}/foo{x}.jpg")
                im.seek(current + 1)
            except EOFError:
                pass
        print(f"[+] {im.n_frames} frames extracted\n")

    except FileExistsError:
        print(f"File {OUTFILE} already exists")
        print("Exiting application...")
        exit()
    


#------------------------------------------------------------
#   CountFile()
#------------------------------------------------------------
#   Description : Count the number of files in a folder
#------------------------------------------------------------
#   Input  : Name of the folder that contains the files
#   Output : Number of files in the folder
#------------------------------------------------------------
def CountFile(dir):
    nb = len(listdir(dir))

    return nb

#------------------------------------------------------------
#   LastFileName()
#------------------------------------------------------------
#   Description : Return the name of the last file in a 
#                 folder
#------------------------------------------------------------
#   Input  : Name of the folder that contains the files
#   Output : Name of the last file
#------------------------------------------------------------
def LastFileName(dir):
    for img in listdir(OUTFILE):
        if str(CountFile(OUTFILE)-1) in img:
            return img

#------------------------------------------------------------
#   ResizeImg()
#------------------------------------------------------------
#   Description : Opens all the images in a folder and resize
#                 them (with distortion)
#------------------------------------------------------------
#   Input  : Desired width, desired height
#   Output : Creates the new file in a folder
#------------------------------------------------------------
def ResizeImg(width, height):
    print("Resizing all the frames...")
    for img in listdir(OUTFILE):
        im = imread(f"{OUTFILE}/{img}")
        im = resize(im, (width, height))
        imwrite(f"{OUTFILE}/{img}", im)
    print("[+] All the frames have been resized\n")

#------------------------------------------------------------
#   TranslateColor()
#------------------------------------------------------------
#   Description : Return the value of a pixel (1 or 0)
#------------------------------------------------------------
#   Input  : Color of the original pixel (only R is tested)
#   Output : 0 if white pixel, 1 if black pixel
#------------------------------------------------------------
def TranslateColor(color):
    if color[0] > 200:
        return 0
    else:
        return 1

#------------------------------------------------------------
#   CreateFile()
#------------------------------------------------------------
#   Description : Create a .h file containing a 2D Array with
#                 the values for all the frames. 
#------------------------------------------------------------
#   Input  : ---
#   Output : .h file with frame values
#------------------------------------------------------------
def CreateFile():
    print("Creating the file...")

    f = open(HEADEROUT, "w")
    f.write("code unsigned char tableau[][1024] = {\n")

    imgList = natsorted(listdir(OUTFILE))
    for img in imgList:
        im = Image.open(f"{OUTFILE}/{img}")
        pix = im.load()

        f.write("{")

        for line in range(8):
            for x in range(WIDTH):
                totValue = 0
                for y in range(int(HEIGHT/8)):
                    value = TranslateColor(pix[x, y + line*8])
                    totValue = totValue + value*2**y

                if (line == 7) and (x == (WIDTH-1)):
                    if img == LastFileName(OUTFILE):
                        end = "}};"
                    else:
                        end = "},"
                else:
                    end = ", "
                
                f.write(str(totValue) + end)
        f.write("\n")
    f.close()
    print("[+] File created succesfully")


if __name__ == "__main__":

    files = []
    for f in listdir():
        if f.endswith(".gif"):
            files.append(f)

    if len(files) == 0:
        print("No gif found in the current directory...")
        print("App will exit in 5s")
        sleep(5)
        exit()


    print("Choose a file : ")
    for x in range(len(files)):
        print(f"[{x}] {files[x]}")

    # Handle user selecting nonexistent file
    while True:
        try:
            findex = int(input("> "))
            if findex > len(files) - 1:
                print("Please select a correct file")
            else:
                break
        except ValueError:
            print("Please select a correct file")
            
    
    GIFNAME = files[findex]
    OUTFILE = GIFNAME + "_frames"
    HEADEROUT = GIFNAME.split(".")[0] + ".h"

    ExtractImage(GIFNAME)
    ResizeImg(WIDTH, HEIGHT)
    CreateFile()