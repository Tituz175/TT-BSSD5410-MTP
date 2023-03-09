"""
    my_gui.py: This a python file that manipulate image color
    base on the color value of two pixels on the image.
    this two pixel color values are selected by clicking on
    the image.
    This python file uses the tkinter, pillow and colorsys module.
    The tkinter module for the creation of the gui and loading of image.
    The pillow and colorsys for the image color manipulation.
"""

# import necessary modules and functions
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import colorsys
from SortFunctions import mergesort
from SearchFunctions import binarySearch_sub
from PixelFunctions import storePixels, compare_pixels_merge_sort, \
    pixels_to_points, grayscale


# my gui class
class MYGUI:

    # gui constructor
    def __init__(self, master):
        self.currentColor = ""
        self.master = master
        self.master.title("Pixel Color Manipulator")
        self.picked_colors = []
        self.imagePath = ""
        self.canvas = ""
        self.image = ""
        self.width = ""
        self.height = ""
        self.photo = ""
        self.start_button = ""
        self.functionalityLoaded = False
        self.selectedColor = 0

        # displaying my welcome message and open button
        self.welcomeMessage = Label(self.master, text="Welcome to pixel color manipulator", font=("Arial", 16))
        self.openImage = Button(self.master, text="Open file", command=self.open_image)
        self.welcomeMessage.grid(row=0, column=0, columnspan=3)
        self.openImage.grid(row=1, column=0, columnspan=3)

    # function to load other part of the application
    def load_functionality(self):
        self.currentColor = Label(self.master, text="Pixel Color: ")
        self.currentColor.grid(row=3, column=0)

        self.start_button = Button(self.master, text="Start",
                                   command=lambda: self.im_highlight(self.image,
                                                                     self.picked_colors[0],
                                                                     self.picked_colors[1]))
        self.start_button.grid(row=3, column=2)
        self.functionalityLoaded = True

    # end def load_functionality(self):

    # function to load image from the user device
    def open_image(self):
        if self.functionalityLoaded:
            Canvas.delete(self.canvas)
        self.imagePath = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                    filetypes=(
                                                        ("png files", "*.PNG"), ("png files", "*.PNG"),
                                                        ("all files", "*.*")))
        self.image = Image.open(self.imagePath)
        self.photo = ImageTk.PhotoImage(self.image)
        self.width, self.height = self.image.size
        self.canvas = Canvas(self.master, width=self.width, height=self.height)
        self.canvas.grid(row=2, column=0, columnspan=3)
        self.canvas.create_image(0, 0, anchor=NW, image=self.photo)
        self.canvas.bind("<Button-1>", self.get_pixel_color)
        if not self.functionalityLoaded:
            self.load_functionality()

    # end def open_image(self):

    # this function gets the color from the image via mouse click event
    def get_pixel_color(self, event):
        # Get x, y coordinates of click event
        xMouse, yMouse = event.x, event.y
        # Get RGB value of pixel at clicked location
        pixel = self.image.getpixel((xMouse, yMouse))
        if self.picked_colors.__len__() < 2:
            # store the color to my color list
            self.picked_colors.append(pixel)
        red, green, blue = pixel
        print(self.picked_colors)
        # Update currentColor label with pixel color
        self.currentColor.config(text=f"Pixel Color: ({red}, {green}, {blue})")

    # end def get_pixel_color(self, event):

    # this is the function that perform the manipulations to the loaded image
    def im_highlight(self, image, tuple_start, tuple_stop):
        pixels, yiq_pixels = storePixels(image)
        yiq_pixels = mergesort(yiq_pixels, compare_pixels_merge_sort)
        target_start = (tuple_start[0] / 255, tuple_start[1] / 255, tuple_start[2] / 255)
        target_stop = (tuple_stop[0] / 255, tuple_stop[1] / 255, tuple_stop[2] / 255)
        print(target_start, tuple_stop)
        yiq_target_start = colorsys.rgb_to_yiq(target_start[0], target_start[1], target_start[2])
        yiq_target_stop = colorsys.rgb_to_yiq(target_stop[0], target_stop[1], target_stop[2])
        print(yiq_target_start[0])
        print(yiq_target_stop[0])
        sub_index_start = binarySearch_sub([b[0][0] for b in yiq_pixels], 0, len(yiq_pixels) - 1,
                                           yiq_target_start[0])
        sub_index_stop = binarySearch_sub([b[0][0] for b in yiq_pixels], 0, len(yiq_pixels) - 1,
                                          yiq_target_stop[0])
        print("target start at: ", sub_index_start)
        grayscale(image, pixels)
        pixels_to_points(image, yiq_pixels[sub_index_start:sub_index_stop])
        image.save("output.jpg", "JPEG")
        image.show()
        self.picked_colors = []

    # end def im_highlight(self, image, tuple_start, tuple_stop):

# end class MYGUI:
