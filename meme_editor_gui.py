import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageTk

screen = tk.Tk()

frame1 = tk.Frame(screen)
frame1.grid(row=0, column=1)
toolScreen = tk.Frame(screen)
toolScreen.grid(row=0, column=2)

canvas = tk.Canvas(frame1, width=500, height=500, borderwidth=1, relief="solid")
canvas.pack()
canvas.images = []


nums = 1
tags = []
main_image = None
tags_info = {}

def make_bg(img, c, x, y, w, h):
    meme_bg = Image.new("RGBA", (w, h), c)
    meme_bg.paste(img, (x, y))
    return meme_bg

def write(img, text, x, y, font=r"C:\Windows\Fonts\arial.ttf", fill="#000000", fontsize=30):
    font = ImageFont.truetype(font, fontsize)
    draw = ImageDraw.Draw(img)
    draw.text((int(x), int(y)), text, font = font, fill=fill)
    return img

def add_img(img1, img2, x, y):
    if img1.size[0] - (img1.size[0] - x) + img2.size[0] > img1.size[0]:
        imgW = img1.size[0] - (img1.size[0] - x) + img2.size[0]
    else:
        imgW = img1.size[0]
    if img1.size[1] - (img1.size[1] - y) + img2.size[1] > img1.size[1]:
        imgH = img1.size[1] - (img1.size[1] - y) + img2.size[1]
    else:
        imgH = img1.size[1]
    img = Image.new("RGBA", (imgW, imgH))
    img.paste(img1, (0, 0))
    img.paste(img2, (x, y))
    return img

def resize_img(img, x, y): 
    return img.resize((x, y))

def update_listBox():
    list_box.delete(0, tk.END)
    for i in tags:
        list_box.insert(tk.END, str(i))


def move_tag(tag, x, y):
    global tags_info
    try:
        tags_info[tag]["x"] = x
        tags_info[tag]["y"] = y
        canvas.moveto(tag, x, y)
    except: 
        tags_info["tag" + str(int(tag[-1])-1)]["x"] = x
        tags_info["tag" + str(int(tag[-1])-1)]["y"] = y
        canvas.moveto("tag" + str(int(tag[-1])-1), x, y)

def add_main_img_to_main_screen():
    global main_image
    path = filedialog.askopenfile()
    pilImage = Image.open(path.name)
    image = ImageTk.PhotoImage(pilImage)
    canvas.image = image
    canvas["width"] = image.width() 
    canvas["height"] = image.height()
    img = canvas.create_image(image.width() // 2, image.height() // 2, image=image, tag="tag0")
    if len(tags) <= 0:
        tags.append("tag0")
    main_image = pilImage
    update_listBox()
    tags_info["tag0"] = {
        "type":"img",
        "image":pilImage,
        "width":image.width(),
        "height":image.height(),
    }
    canvas.tag_bind(f"tag{str(nums)}", "<B1-Motion>", lambda e: canvas.moveto(tags[-1], e.x, e.y))
    return img

def add_text():
    global nums
    text = simpledialog.askstring(title="enter text", prompt="enter text")
    if text == None:
        return
    cText = canvas.create_text(100, 100, text=text, tag=f"tag{str(nums)}", font=("Arial", 30), fill="black")
    tags.append(f"tag{str(nums)}")
    update_listBox()
    tags_info[f"tag{str(nums)}"] = {
        "type":"text",    
        "text":text,
        "x":100,
        "y":100
    }
    canvas.tag_bind(f"tag{str(nums)}", "<B1-Motion>", lambda e: canvas.tag_bind(tags[-1], "<B1-Motion>", lambda e: move_tag(f"tag{str(nums)}", e.x, e.y))) 
    nums += 1
    return cText

def add_img_to_canvas():
    global nums
    path = filedialog.askopenfile()
    width, height = simpledialog.askstring(title="enter size", prompt="after the point is width\n before the point is height").split(".")
    pilImage = Image.open(path.name)
    pilImage = resize_img(pilImage, int(width), int(height))
    image = ImageTk.PhotoImage(pilImage)
    canvas.images.append(image)
    img = canvas.create_image(image.width() // 2, image.height() // 2, image=image, tag=f"tag{nums}")
    canvas.moveto(img, 100, 100)
    tags.append(f"tag{nums}")
    update_listBox()
    tags_info[f"tag{nums}"] = {
        "type":"normal_img",
        "image":pilImage,
        "x":100,
        "y":100,
        "width":image.width(),
        "height":image.height(),
    }
    canvas.tag_bind(f"tag{str(nums)}", "<B1-Motion>", lambda e: move_tag(f"tag{str(nums)}", e.x, e.y))
    nums += 1
    return img

def add_main_img_background():
    global main_image
    color = colorchooser.askcolor()
    color = color[1]
    x, y, w, h = simpledialog.askstring(title="pick posision and size", prompt="you need to seperate between the args with '.'\nthe background will start at 0, 0").split(".")
    pilImage = make_bg(main_image, color, int(x), int(y), int(w) + main_image.size[0], int(h) + main_image.size[1 ])
    image = ImageTk.PhotoImage(pilImage)
    canvas.image = image
    canvas["width"] = image.width() 
    canvas["height"] = image.height()
    img = canvas.create_image(image.width() // 2, image.height() // 2, image=image, tag="tag0")
    if len(tags) <= 0:
        tags.append("tag0")
    canvas.tag_bind("tag0", "<B1-Motion>", lambda e: canvas.moveto("tag0", e.x, e.y))
    main_image = pilImage
    update_listBox()
    tags_info["tag0"] = {
        "type":"img",
        "image":main_image,
        "width":image.width(),
        "height":image.height(),
    }
    return img

def save():
    image = Image.new("RGBA", (tags_info["tag0"]["width"], tags_info["tag0"]["height"]))
    image.paste(tags_info["tag0"]["image"])
    for i in tags_info:
        if tags_info[i]["type"] == "text":                
            image = write(img=image, text=list(tags_info[i].values())[1], x=list(tags_info[i].values())[2], y=list(tags_info[i].values())[3])
        elif tags_info[i]["type"] == "normal_img":
            image = add_img(img1=image, img2=list(tags_info[i].values())[1], x=list(tags_info[i].values())[2], y=list(tags_info[i].values())[3])
    image.save(simpledialog.askstring(title="pick name", prompt="name") + ".png", format="png")

change_img_button = ttk.Button(toolScreen, text="change main image", command=add_main_img_to_main_screen)
change_img_button.pack()
add_text_button = ttk.Button(toolScreen, text="add text", command=add_text)
add_text_button.pack()
add_image = ttk.Button(toolScreen, text="add img", command=add_img_to_canvas)
add_image.pack()
add_img_bg = ttk.Button(toolScreen, text="add background to main image", command=add_main_img_background)
add_img_bg.pack()
save_img = ttk.Button(toolScreen, text="save", command=save)
save_img.pack()

def list_box_move_tag(tag, e):
    global tags_info
    move_tag(tag, e.x, e.y)

list_box = tk.Listbox(screen)
list_box.grid(row=0, column=0)
list_box.bind("<Double-1>", lambda e: canvas.tag_bind(list_box.get(list_box.curselection()), "<B1-Motion>", lambda e: list_box_move_tag(list_box.get(list_box.curselection()), e)))
#canvas.tag_bind("img","<B1-Motion>", lambda e: canvas.moveto("img", e.x, e.y))
screen.mainloop()