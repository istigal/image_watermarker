from tkinter import *
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont

image = None
out = None
img = None
rgb = (255, 255, 255)


def browse():
    global img
    filetypes = (
        ("image files", ("*.jpg", "*.png", "*.webp", "*.bmp", "*.tiff")),
        ("All files", "*.*")
    )
    try:
        filename = filedialog.askopenfile(title="Select an image", filetypes=filetypes)
        image_path = filename.name
        img = Image.open(image_path).convert("RGBA")
        img.thumbnail((900, 900))
        show_image(img)
    except AttributeError:
        pass


def show_image(im):
    global pic, image
    canvas.delete(im)
    image = ImageTk.PhotoImage(im, master=window)
    canvas.config(width=image.width(), height=image.height())
    pic = canvas.create_image(image.width()/2, image.height()/2, image=image)
    canvas.grid(column=0, row=3, columnspan=3)
    add_wmark.grid(column=1, row=1)


def add_watermark():
    global message
    message.grid_forget()
    text.grid(column=1, row=2, pady=10)
    add_button.grid(column=2, row=2)
    color_button.grid(column=0, row=2)


def choose_color():
    global rgb
    color = colorchooser.askcolor()
    rgb = color[0]


def add_to_image():
    global out
    img_size = img.size
    blank = Image.new("RGBA", img_size, (255, 255, 255, 0))
    watermark = text.get()
    draw = ImageDraw.Draw(blank)
    fill = (rgb[0], rgb[1], rgb[2], 100)
    my_font = ImageFont.truetype("fonts/AdobeVFPrototype.ttf", 30)
    draw.text((20, img_size[1]-50), text=watermark, fill=fill, font=my_font)
    out = Image.alpha_composite(img, blank)
    show_image(out)
    text.grid_forget()
    add_button.grid_forget()
    save_button.grid(column=2, row=1)
    color_button.grid_forget()
    add_wmark.config(text="Edit Watermark")


def save():
    global message
    filetypes = (
        ("PNG file", "*.png"),
        ("WEBP file", "*.webp")
    )
    try:
        filename = filedialog.asksaveasfilename(title="Save image as", filetypes=filetypes, defaultextension=".png")
        image_path = filename
        out.save(image_path)
        message.config(text="Successfully saved.", fg="green")
    except ValueError:
        message.config(text="The image is not saved.", fg="red")
    message.grid(column=1, row=2)


window = Tk()
window.minsize(400, 150)
window.title("Watermarker")
window.config(padx=30, pady=30)

browse_btn = Button(text="Browse image", command=browse)
browse_btn.grid(column=0, row=1, pady=10)

add_wmark = Button(text="Add watermark", command=add_watermark)

save_button = Button(text="Save image", command=save)

text = Entry()

add_button = Button(text="Add", command=add_to_image)

color_button = Button(text="Choose color", command=choose_color)

canvas = Canvas()
pic = canvas.create_image(0, 0, image)

message = Label()

window.mainloop()
