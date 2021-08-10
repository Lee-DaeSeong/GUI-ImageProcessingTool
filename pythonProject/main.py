from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np, cv2
import datetime
import tkinter.messagebox as msgbox
import regz_socket_MP_FD
import comp
import my_carv

root = Tk()  # create root window
root.title("OpenCV Term Project")  # title of the GUI window
root.geometry("1080x680") # 1080x680 크기로 window size 설정
root.resizable(False, False)  # 창크기 고정
root.config(bg="skyblue")

#전역변수로 현재 이미지를 저장하는 check변수
#default 1.jpg
check = cv2.imread("1.jpg")
toggle = True


def show_msg():
    msgbox.showinfo("gaze coreection 실행", "실시간 화면을 불러오고 있습니다. 잠시 기다려주세요.")

def x():
    pass

filename="default"

def openfn():
    global check
    global filename
    filename = filedialog.askopenfilename(title='open')
    check = cv2.imread(filename)
    return filename


def resize_img(img, width):
    basewidth = width
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    return img


def load_img():
    global toggle
    toggle = False
    x = openfn()
    img = Image.open(x)
    original_img = resize_img(img, 280)
    main_img = resize_img(img, 700)
    global img1, img2
    img1 = ImageTk.PhotoImage(original_img)
    img2 = ImageTk.PhotoImage(main_img)
    original.config(image=img1)
    mainimg_lable.config(image=img2)

def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func


def my_comp() :
    global filename
    comp.compression(filename)


def call_Gaze():
    regz_socket_MP_FD.all(1)


def forget():
    R.pack_forget()
    G.pack_forget()
    B.pack_forget()
    rgb.pack_forget()
    bright.pack_forget()
    add_or_sub.pack_forget()
    bright_label1.pack_forget()
    bright_label2.pack_forget()
    width.pack_forget()
    height.pack_forget()
    resize_btn.pack_forget()

def color_track():
    forget()

    rgb.pack(padx=5)
    R.pack(padx=5)
    G.pack(padx=5)
    B.pack(padx=5)

    r=R.get()
    g=G.get()
    b=B.get()

    global check
    blue, green, red = cv2.split(check)
    cv2.add(blue, b, blue)  # blue 채널 밝기 증가
    cv2.add(green,g, green)  # green 채널 밝기 증가
    cv2.add(red, r, red)  # red 채널 밝기 증가

    img = cv2.merge([blue, green, red])
    check = img
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    edit=Image.fromarray(img)
    edit=resize_img(edit,700)
    global img4
    img4=ImageTk.PhotoImage(edit)
    mainimg_lable.config(image=img4)

def resize():
    forget()
    global filename
    my_carv.resize(filename)

def brightnees_track():
    forget()

    bright_label1.pack()
    bright.pack()
    bright_label2.pack()
    add_or_sub.pack()

    global check
    b = bright.get()
    c = add_or_sub.get()

    array = np.full(check.shape, (b, b, b), dtype=np.uint8)
    img = None

    if c==0:
        img=cv2.add(check,array)
    else:
        img=cv2.subtract(check,array)

    check=img
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    edit = Image.fromarray(img)
    edit = resize_img(edit, 700)
    global img3
    img3 = ImageTk.PhotoImage(edit)
    mainimg_lable.config(image=img3)

def resize_track():
    forget()
    width.pack()
    height.pack()
    resize_btn.pack()


def resize_click():
    pass


def save():
    global check
    now = datetime.datetime.now().strftime("%d_%H-%M-%S")
    cv2.imwrite(str(now)+".png", check)



# 왼쪽에 배치된 frame
left_frame = Frame(root, width=300, height=660, bg='#5680E9')
left_frame.grid(row=0, column=0, padx=10, pady=10)

#오른쪽에 배치된 frame
right_frame = Frame(root, width=730, height=660, bg='#5680E9')
right_frame.grid(row=0, column=1, padx=15, pady=10)
left_frame.grid_propagate(0)
right_frame.grid_propagate(0)


#실시간 gaze correction 버튼
gaze_button = Button(left_frame, text="실시간 gaze correction", command=combine_funcs(show_msg,call_Gaze), width=30,
                   relief=RAISED)
gaze_button.grid(row=1, column=0, padx=5, pady=10)

#GUI 실행시 작은 화면에 띄울 흰색 빈 이미지 생성
default_origin = np.full((200,280),255, np.uint8)
cv2.imwrite("origin.png", default_origin)

origin = ImageTk.PhotoImage(file="origin.png")
original = Label(left_frame, image=origin, height=230)
original.grid(row=3, column=0, padx=5, pady=5)


#GUI 실행시 큰 화면에 띄울 흰색 빈 이미지 생성
default_main = np.full((620,700),255, np.uint8)
cv2.imwrite("main.png", default_main)

mainimg = ImageTk.PhotoImage(file="main.png")
mainimg_lable = Label(right_frame, image=mainimg, height=620)
mainimg_lable.grid(row=0, column=0, padx=12, pady=17)


#버튼과 트랙바가 추가될 전체 option frame
option_frame = Frame(left_frame, width=250, height=350)
option_frame.grid(row=4, column=0, padx=5, pady=10, sticky=N + E + W + S)
option_frame.grid_propagate(0)

#버튼들이 추가될 frame
button_frame = Frame(option_frame, width=250)
button_frame.grid(row=2, column=0, pady=10, padx=5)
Button(button_frame, text="불러오기", width=9, height=4, command=load_img, bg='white').grid(row=0, column=0, padx=3, pady=3)
Button(button_frame, text="색상 변경", width=9, height=4, command=color_track, bg='white').grid(row=0, column=1, padx=3, pady=3)
Button(button_frame, text="밝기 변경", width=9, height=4,command=brightnees_track, bg='white').grid(row=0, column=2, padx=3, pady=3)

Button(button_frame, text="리사이즈", width=9, height=4, command=resize, bg='white').grid(row=1, column=0, padx=3, pady=3)
Button(button_frame, text="압축", width=9, height=4, command=my_comp, bg='white').grid(row=1, column=1, padx=3, pady=3)
Button(button_frame, text="저장", width=9, height=4, command=save, bg='white').grid(row=1, column=2, padx=3, pady=3)

#추가적인 버튼이나 트랙바가 위치할 frame
add_frame = Frame(option_frame, bg='white', width=270, height=150)
add_frame.grid(row=3, column=0, padx=5, pady=10)
add_frame.grid_propagate(0)

#색상 변경 버튼을 눌렀을 때 나타나는 3개의 트랙바와 label
R = Scale(add_frame, from_=0, to=255, orient=HORIZONTAL, length=200)
G = Scale(add_frame, from_=0, to=255, orient=HORIZONTAL, length=200)
B = Scale(add_frame, from_=0, to=255, orient=HORIZONTAL, length=200)
rgb = Label(add_frame, text="위에서부터 R G B 변경")


bright = Scale(add_frame, from_=0, to=255, orient=HORIZONTAL, length=200)
add_or_sub = Scale(add_frame, from_=0, to=1, orient=HORIZONTAL, length=200)
bright_label1 = Label(add_frame, text="변경할 밝기 값")
bright_label2 = Label(add_frame, text="0 : 밝게   1: 어둡게")

width=Scale(add_frame, from_=100, to=1000, orient=HORIZONTAL, length=200)
height=Scale(add_frame, from_=100, to=1000, orient=HORIZONTAL, length=200)
resize_btn=Button(add_frame, text="사이즈 변경", command=resize_click, bg='white')

root.mainloop()