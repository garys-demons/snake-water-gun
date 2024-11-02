from tkinter import *
from PIL import Image, ImageTk
import random
import tkinter.messagebox as tmsg
root=Tk()
root.geometry('750x750')
root.title("SNAKE WATER GUN")

#functions
def crand():
    l=('snake','water','gun')
    r=random.choice(l)
    return r

def snake(event):
    ch=crand()
    if ch=='snake':
        tmsg.showinfo('Result',f'snake V/S {ch}. DRAW')
    elif ch=='water':
        scoreval.set(scoreval.get()+1)
        screen.update()
        tmsg.showinfo('Result',f'snake V/S {ch}. WIN')
    else:
        scoreval.set(scoreval.get()-1)
        screen.update()
        tmsg.showinfo('Result',f'snake V/S {ch}. LOSE')

def water(event):
    ch=crand()
    if ch=='water':
        tmsg.showinfo('Result',f'water V/S {ch}. DRAW')
    elif ch=='gun':
        scoreval.set(scoreval.get()+1)
        screen.update()
        tmsg.showinfo('Result',f'water V/S {ch}. WIN')
    else:
        scoreval.set(scoreval.get()-1)
        screen.update()
        tmsg.showinfo('Result',f'water V/S {ch}. LOSE')

def gun(event):
    ch=crand()
    if ch=='gun':
        tmsg.showinfo('Result',f'gun V/S {ch}. DRAW')
    elif ch=='snake':
        scoreval.set(scoreval.get()+1)
        screen.update()
        tmsg.showinfo('Result',f'gun V/S {ch}. WIN')
    else:
        scoreval.set(scoreval.get()-1)
        screen.update()
        tmsg.showinfo('Result',f'gun V/S {ch}. LOSE')
def help(event):
    tmsg.showinfo("help","The game of snake, water and gun is a children's game and is similar to rock, paper and scissors. The basic rules are: Snake drinks water, water damages the gun and the gun kills snake. When you click on the icons of your choice (snake, water, gun), the computer will randomly pic an option as well and the results will be displayed on your screen. Your score will also be displayed on the top right corner of your screen. ")


#SCORECARD
f1= Frame(root)
Label(f1,text='Score',font=('Verdana',20,'bold')).pack(side=LEFT,anchor='nw')
scoreval=IntVar()
scoreval.set('0')
screen=Entry(f1,textvariable=scoreval,font=('Verdana',20,'bold'),width=5)
screen.pack(side=LEFT,anchor='nw')
f1.pack(fill=X)

#Creating the snake,water,gun buttons
p1=Image.open('snake.png')
rp1=p1.resize((300,300))
snakep=ImageTk.PhotoImage(rp1)

p2=Image.open('water.png')
rp2=p2.resize((300,300))
waterp=ImageTk.PhotoImage(rp2)

p3=Image.open('gun.png')
rp3=p3.resize((300,300))
gunp=ImageTk.PhotoImage(rp3)

p4=Image.open('help.png')
rp4=p4.resize((300,300))
helpp=ImageTk.PhotoImage(rp4)


f=Frame(root,bg='black',borderwidth=5,relief=SUNKEN)
b1=Button(f,text='Snake',image=snakep)
b1.grid(row=3,column=0)
b1.bind("<Button-1>",snake)
b2=Button(f,text='Water',image=waterp)
b2.grid(row=3,column=1)
b2.bind("<Button-1>",water)
b3=Button(f,text='Gun',image=gunp)
b3.grid(row=4,column=0)
b3.bind("<Button-1>",gun)
b4=Button(f,text='Help',image=helpp)
b4.grid(row=4,column=1)
b4.bind('<Button-1>',help)
f.pack()

root.mainloop()