"""
File: stanCodoshop.py
----------------------------------------------
Adapted from Nick Parlante
"""

import os
import sys
from math import sqrt
from simpleimage import SimpleImage


def get_pixel_dist(pixel, red, green, blue):
    """
    Returns the color distance between pixel and mean RGB value

    Input:
        pixel (Pixel): pixel with RGB values to be compared
        red (int): average red value across all images
        green (int): average green value across all images
        blue (int): average blue value across all images

    Returns:
        dist (int): color distance between red, green, and blue pixel values

    """
    red_dist = (pixel.red - red) ** 2
    green_dist = (pixel.green - green) ** 2
    blue_dist = (pixel.blue - blue) ** 2
    return sqrt(red_dist + green_dist + blue_dist)


def get_average(pixels):
    """
    Given a list of pixels, finds the average red, blue, and green values

    Input:
        pixels (List[Pixel]): list of pixels to be averaged
    Returns:
        rgb (List[int]): list of average red, green, blue values across pixels respectively

    Assumes you are returning in the order: [red, green, blue]

    """
    total = len(pixels)
    red = 0
    green = 0
    blue = 0

    for pixel in pixels:
        red += pixel.red
        green += pixel.green
        blue += pixel.blue

    return [red // total, green // total, blue // total]


def get_best_pixel(pixels):
    """
    Given a list of pixels, returns the pixel with the smallest
    distance from the average red, green, and blue values across all pixels.

    Input:
        pixels (List[Pixel]): list of pixels to be averaged and compared
    Returns:
        best (Pixel): pixel closest to RGB averages

    """
    avg = get_average(pixels)
    dist_lst = []

    for pixel in pixels:
        dist_lst.append(get_pixel_dist(pixel, avg[0], avg[1], avg[2]))

    best = pixels[0]
    min_dist = dist_lst[0]

    for i in range(len(dist_lst)):
        dist = dist_lst[i]
        if dist < min_dist:
            min_dist = dist
            best = pixels[i]
    return best


def solve(images):
    """
    Given a list of image objects, compute and display a Ghost solution image
    based on these images. There will be at least 3 images and they will all
    be the same size.

    Input:
        images (List[SimpleImage]): list of images to be processed
    """
    width = images[0].width
    height = images[0].height
    result = SimpleImage.blank(width, height)
    for w in range(width):
        for h in range(height):
            pixels = []
            for img in images:
                pixels.append(img.get_pixel(w, h))
            best = get_best_pixel(pixels)
            result.set_rgb(w, h, best.red, best.green, best.blue)

    print("Displaying image!")
    result.show()


def jpgs_in_dir(dir):
    """
    (provided, DO NOT MODIFY)
    Given the name of a directory, returns a list of the .jpg filenames
    within it.

    Input:
        dir (string): name of directory
    Returns:
        filenames(List[string]): names of jpg files in directory
    """
    filenames = []
    for filename in os.listdir(dir):
        if filename.endswith(".jpg"):
            filenames.append(os.path.join(dir, filename))
    return filenames


def load_images(dir):
    """
    (provided, DO NOT MODIFY)
    Given a directory name, reads all the .jpg files within it into memory and
    returns them in a list. Prints the filenames out as it goes.

    Input:
        dir (string): name of directory
    Returns:
        images (List[SimpleImages]): list of images in directory
    """
    images = []
    jpgs = jpgs_in_dir(dir)
    for filename in jpgs:
        print("Loading", filename)
        image = SimpleImage(filename)
        images.append(image)
    return images


def main():
    args = sys.argv[1:]

    # We just take 1 argument, the folder containing all the images.
    images = load_images(args[0])
    solve(images)


if __name__ == "__main__":
    main()
