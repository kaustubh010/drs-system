import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from functools import partial
import threading
import imutils
import time

# Width and height of our main screen
SET_WIDTH = 650
SET_HEIGHT = 368

stream = cv2.VideoCapture("clip.mp4")
flag = True
def play(speed):
    global flag
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    if flag:
        canvas.create_text(132,26, fill="black", font="Times 26 bold", text="Decision Pending")
    flag = not flag

def pending(decision):
    # Display decision pending image
    frame = cv2.cvtColor(cv2.imread("pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    time.sleep(1)

    # Display sponsor image
    frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    time.sleep(1)
    
    # Display out/notout image
    if decision == 'out':
        decisionImg = 'out.png'
    else:
        decisionImg = 'not_out.png'
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)

def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()

def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()

# Tkinter gui starts here
window = tkinter.Tk()
window.title("Third Umpire Decision Review Kit")
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
cv_img = cv2.cvtColor(cv2.imread("welcome.png"), cv2.COLOR_BGR2RGB)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image=photo)
canvas.pack()

# Buttons to control playback
btn = tkinter.Button(window, text="<< Previous (Fast)", width=50, command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text="<< Previous (Slow)", width=50, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text="Next (Fast) >>", width=50, command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text="Next (Slow) >>", width=50, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text="Give Out", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="Give Not Out", width=50, command=not_out)
btn.pack()

window.mainloop()