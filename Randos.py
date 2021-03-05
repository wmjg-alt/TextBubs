from tkinter import *
import random
import time
import psutil
import nltk
import math

bnum = 3
speed = 1.0
scale = 8
packed = True
count = 1
going = False
first = True
master_ls = [None for x in range(0,bnum)]


with open ("Seuss.txt", "r") as myfile:
    data = [x for x in nltk.sent_tokenize(myfile.read()) if len(x)>10 and len(x) < 500]

# Instanced TK with Titled and Properties:
wdow = Tk()
wdow.title('Blippy') 
wdow.resizable(True, True)

w, h = wdow.winfo_screenwidth()-200, wdow.winfo_screenheight()-200
wdow.geometry("%dx%d" % (w+10, h+5))

max_r = math.floor(h/5)
min_r = math.floor(h/10)

# Frames
top = Frame(wdow)
top.pack(side=TOP)
bot = Frame(wdow)
bot.pack(side=BOTTOM)

canvas = Canvas(wdow, width=w, height=h, borderwidth=5, highlightthickness=10, bg="#010966")
canvas.pack()

def speedup(ev):
    global speed
    if ev:
        speed = speed/2
def speeddn(ev):
    global speed
    if ev:
        speed = speed*2
        

# Some labels
#T1 = Label(wdow, text="Hello World")
#T1.pack()


def create_circle(x, y, r, color, canvasName): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, fill=color)


def undoes(event):
    if packed:
        T1.pack_forget()
    else:
        T1.pack()

#Pythagoras to describe the square in the circles
def pThag(r):
    return math.floor(math.sqrt(((r*2)**2)/2))

class blob:
    def __init__(self, c):
        random.seed(random.randint(-10000,10000))
        self.r = random.randint(min_r,max_r)
        self.x = random.randint(self.r, w-(self.r))
        self.y = random.randint(self.r, h-(self.r))
        self.col = "#%06x" % random.randint(0, 0xFFFFFF)

        self.blip = create_circle(self.x, self.y, self.r, self.col, canvas)
        f = "Times "+str(int(self.r/scale))+" bold"
        texx = data[c]
        #texx = ""+str(self.x)+"\n"+str(self.y) displays coords
        widdy = pThag(self.r)
        self.tx = canvas.create_text(self.x,self.y, text=texx, anchor=CENTER, justify=CENTER, font=f, width=widdy)

    def reset(self, c):
        canvas.delete(self.blip)
        canvas.delete(self.tx) #dont 'delete' if you want to leave a trail of txt
        
        self.r = random.randint(min_r,max_r)
        self.x = random.randint(self.r, w-(self.r))
        self.y = random.randint(self.r, h-(self.r))
        self.col = "#%06x" % random.randint(0x111111, 0xFFFFFF)

        self.blip = create_circle(self.x, self.y, self.r, self.col, canvas)
        f = "Times "+str(int(self.r/scale))+" bold"
        texx = data[c]
        #texx = ""+str(self.x)+"\n"+str(self.y) displays coords
        widdy = pThag(self.r)
        self.tx = canvas.create_text(self.x,self.y, text=texx, anchor=CENTER, justify=CENTER, font=f, width=widdy)


t_x =math.floor(w/2)
t_y =math.floor(h/2)
t_r =max_r
t_col ='red'
t_font ="Times "+str(int(max_r/scale))+" bold"
tit = create_circle(t_x, t_y, t_r, t_col, canvas)
titT = canvas.create_text(t_x, t_y, text=data[0], anchor=CENTER, justify=CENTER, font=t_font, width=pThag(t_r))


def go(e): 
    global master_ls, going, count, first, speed
    if going:
        going = False
    else:
        going = True
        while going:
            for x in range(0, bnum):
                global speed
                if not going:
                    break
                if first:
                    master_ls[x] = blob(count)
                else:
                    master_ls[x].reset(count)
                count+=1
                wdow.update()
                time.sleep(speed)
            if first:
                canvas.delete(tit)
                canvas.delete(titT)
                first = not first
            print("blips so far: ", count, "----", speed, bnum)
            print(psutil.virtual_memory())


# Widget Buttons
#B1 = Button(top, text="CLUTTER", fg="#00ff00", command=clutter)
B2 = Button(top, text="SpeedUP", fg="#552299", command=speedup(True))
B3 = Button(top, text="SpeedDOWN", fg="#000166", command=speeddn(True))
#B4 = Button(bot, text="GO", fg="#dc00a0", command=go(None))

#B1.pack(side=LEFT)
B2.pack(side=LEFT)
B3.pack(side=LEFT)
#B4.pack(side=RIGHT)

wdow.bind("<space>", go)
wdow.bind("<Up>", speedup)
wdow.bind("<Down>", speeddn)


try:
    print('display')
    wdow.mainloop() #event loop
except:
    print('exited')

