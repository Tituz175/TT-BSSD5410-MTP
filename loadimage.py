from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog

root = Tk()
root.title("Hello World")

root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                           filetypes=(
                                           ("png files", "*.PNG"), ("png files", "*.PNG"), ("all files", "*.*")))

my_label = Label(root, text=root.filename).pack()

my_image = ImageTk.PhotoImage(Image.open(root.filename))
my_image_label = Label(image=my_image)
my_image_label.pack()

root.mainloop()
