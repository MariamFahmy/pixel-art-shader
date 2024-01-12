"""
Protype program that automatically shades pixel art
Algorithm adapted from the paper "Automatic Sprite Shading" at https://www.sbgames.org/papers/sbgames09/computing/full/cp10_09.pdf

Code author: Mariam Fahmy F. A. Ahmed
"""
import numpy
import cv2

# open image in color
original = cv2.imread(filename)
final = cv2.imread(filename) # make a copy of the original to perform the shading on

"""Stores visual representation of progress so far so we can see what
the code is doing"""
ysection = cv2.imread(filename)
xsection = cv2.imread(filename)
intersection = cv2.imread(filename) # showing both segments in same image

"""black pixels are assumed to be outline pixels
 white pixels are assumed to be background pixels"""
def isWithinOutline(pixel):
    # if at least one of the B, G, R values is not 0, pixel is not black
    not_black = pixel[0] != 0 or pixel[1] != 0 or pixel[2] or 0
    # if at least one of the B, G, R values is not 255, pixel is not white
    not_white = pixel[0] != 255 or pixel[1] != 255 or pixel[2] != 255
    return not_black and not_white

# change color of pixel to [B, G, R]
def changeColor(pixel, B, G, R):
    pixel[0] = B
    pixel[1] = G
    pixel[2] = R

"""
-----Perform Highlight Spot Approximation------
As described in the paper "Automatic Sprite Shading" at https://www.sbgames.org/papers/sbgames09/computing/full/cp10_09.pdf
the highlight spot is the spot with the highest exposure to the light source 
"""

# light_position is the position of the light source as [row, col] pair
# row and col are in range [0.0, 1.0]
# [0.0, 0.0] means light source is at top-left corner of coordinate system
light_position = [0.25, 0.7] # light source is at position 25% of height of image and 70% width of image

height = original.shape[0] # height of image
width = original.shape[1] # width of image

"""
------Classify pixels into 3 classes (weights)------
As described in the paper "Automatic Sprite Shading" at https://www.sbgames.org/papers/sbgames09/computing/full/cp10_09.pdf
Weight 0: pixels that belong to neither x nor y segments
Weight 1: pixels that belong to only one segment
Weight 2: pixels that are highlight spots (at intersection of x and y segments)
"""
# used to store the shading weight (0, 1 or 2) of each pixel
weight = numpy.zeros(shape=(height, width, 1), dtype=numpy.float32)

# for each row of the image, holds [start column, end column] of pixels that are inside sprite
# (i.e. for each row that has pixels inside the sprite, holds row index and first pixel that is not a background
# or outline pixel and last pixel that is not a background or outline pixel)
# this is used to separate pixels inside sprite from background/outline pixels
sprite = []

# sectioning on the x-direction
for row in range(height):
    col = 0
    # skip_row is flag to skip a row that only contains irrelevant background pixels
    skip_row = True
    while col < width:
        # if current pixel is not background or outline, keep going till
        # a background pixel or outline pixel is reached
        if isWithinOutline(original[row, col]):
            # both start and end pixels are inside the art
            # a start of a line segment along a row is found
            # color it blue to show it
            start = col
            changeColor(ysection[row, col], 0, 255, 128)
            # row contains pixels inside sprite, not just background pixels, so don't skip later
            skip_row = False
            break
        col += 1
    # now find end pixel
    while col < width:
        if not isWithinOutline(original[row, col]):
            end = col - 1  # previous column is the end
            sprite.append([row, start, end])
            changeColor(ysection[row, col - 1], 255, 255, 0)
            break
        col += 1
    # calculate center pixel for this row
    # using centre pixel = start + light_position * (end - start)
    if not skip_row:
        center = int(start + light_position[1] * (end - start))
        changeColor(ysection[row, center], 0, 0, 255)
        changeColor(intersection[row, center], 0, 0, 255)
        weight[row, center] = 1


# sectioning on the y-direction
for col in range(width):
    row = 0
    # skip_row is flag to skip a row that only contains irrelevant background pixels
    skip_col = True
    while row < height:
        # if current pixel is not background or outline, keep going till
        # a background pixel or outline pixel is reached
        if (isWithinOutline(original[row, col])):
            # both start and end pixels are inside the art
            # a start of a line segment along a row is found
            # color it blue to show it
            start = row
            changeColor(xsection[start, col], 0, 255, 128)
            # row contains pixels inside sprite, not just background pixels, so don't skip later
            skip_col = False
            break
        row += 1
    # now find end pixel
    while row < height:
        if not isWithinOutline(original[row, col]):
            end = row - 1 # previous row is the end
            changeColor(xsection[end, col], 255, 255, 0)
            break
        row += 1
    # calculate center pixel for this column
    # using centre pixel = start + light_position * (end - start)
    if not skip_col:
        center = int(start + light_position[0] * (end - start))
        changeColor(xsection[center, col], 0, 0, 255)
        changeColor(intersection[center, col], 0, 0, 255)
        # if [center, col] is also part of the x-direction segment, it's a highlight spot
        if weight[center, col] == 1:
            weight[center, col] = 2
            highlight_spot = [center, col]
        else:  # [center, col] belongs to this segment only
            weight[center, col] = 1

"""-----Get Shading Distribution-----"""
"""
Calculate the average shading distribution by blurring the weights matrix, step is adapted from "Automatic Sprite Shading"
"""
shading_distribution = numpy.zeros(shape=(height, width, 1), dtype=float)
shading_distribution = cv2.boxFilter(src=weight, dst=shading_distribution, ddepth=-1, ksize=(121, 121), normalize=True, borderType=cv2.BORDER_ISOLATED)
max_shade = 0
shading_distribution = cv2.boxFilter(src=shading_distribution, dst=shading_distribution, ddepth=-1, ksize=(99, 99), normalize=True, borderType=cv2.BORDER_ISOLATED)

for row in range(height):
    for col in range(width):
        if shading_distribution[row, col] > max_shade:
            max_shade = shading_distribution[row, col]

# normalize shading distribution to take values in range [0, 1.0]
for row in range(height):
    for col in range(width):
        shading_distribution[row, col] = shading_distribution[row, col] / (max_shade + 0.00000001)

"""---------Assign shades to pixels-------"""
# convert sprite to HSI model to facilitate shading
hsi_art = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)
# loop over every pixel inside sprite
for r in range(len(sprite)):
    for col in range(sprite[r][1], sprite[r][2] + 1): # from start to end of pixels INSIDE sprite
        row = sprite[r][0]
        base_intensity = hsi_art[row, col][2]
        if shading_distribution[row, col] <= 0.3:
            hsi_art[row, col][2] = base_intensity * 0.8
        elif shading_distribution[row, col] <= 0.4:
            hsi_art[row, col][2] = base_intensity * 0.85
        elif shading_distribution[row, col] <= 0.5:
            hsi_art[row, col][2] = base_intensity * 0.9
        elif shading_distribution[row, col] <= 0.6:
            hsi_art[row, col][2] = base_intensity * 0.95
        elif shading_distribution[row, col] <= 0.7:
            hsi_art[row, col][2] = base_intensity * 1
        elif shading_distribution[row, col] <= 0.8:
            hsi_art[row, col][2] = min(255, base_intensity * 1.05)
        elif shading_distribution[row, col] <= 0.9:
            hsi_art[row, col][2] = 255
        else:
            hsi_art[row, col][1] = 0
            hsi_art[row, col][2] = 255

unpixelated = cv2.cvtColor(hsi_art, cv2.COLOR_HSV2BGR) # shaded art so far in RGB but not in pixel-art style

"""
--------Pixelate the art so the final result has pixel-art style---------
Code credit: https://stackoverflow.com/questions/55508615/how-to-pixelate-image-using-opencv-in-python, HansHirse
"""
"""Start of StackOverFlow code:"""
# Get input size
height, width = unpixelated.shape[:2]
# Desired "pixelated" size
w, h = (16, 16)
# Resize input to "pixelated" size
temp = cv2.resize(unpixelated, (w, h), interpolation=cv2.INTER_LINEAR)
# Initialize output image
final = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
"""End of StackOverFlow code"""

"""Save result as new image"""
cv2.imwrite(filename[:filename.index('.')] + "_shaded.png", final)

"""Display results"""
# display original and visual representation of progress by the code
# --->>>> to see how the code works, uncomment the commented imshow calls
cv2.imshow('Original art', original)
#cv2.imshow('y-direction segmentation', ysection)
#cv2.imshow('x-direction segmentation', xsection)
#cv2.imshow('intersection', intersection)
#cv2.imshow('Shading distribution', shading_distribution)
#cv2.imshow('Unpixelated', unpixelated)
cv2.imshow('Final', final)
cv2.waitKey()
