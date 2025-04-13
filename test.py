from tkinter import *
from tkinter import ttk
from socket import *
from tkinter.scrolledtext import ScrolledText
from HWVL import HWVL
import time as t
import sys
import base64
import threading
from cryptography.fernet import Fernet

window=Tk()
window.geometry("300x400")
window.resizable(0,0)
data=[]

def Next():
        global data
        data.append(pas.get())
        data.append(ip.get())
        data.append(port.get())
        data.append(server_client.get())
        window.destroy()
    
text1=Label(window,
            text="password:",
            font=("Arial 20"),
            )
text1.pack()

pas=Entry(window,
        font=("Arial 15"),
        show="X"
        )
pas.pack(fill=X,padx=40)

text2=Label(window,
            text="ip:",
            font=("Arial 20"),
            )
text2.pack()

ip=Entry(window,
        font=("Arial 15")
        )
ip.pack(fill=X,padx=40)

text3=Label(window,
            text="port:",
            font=("Arial 20"),
            )
text3.pack()

port=Entry(window,
        font=("Arial 15")
        )
port.pack(fill=X,padx=40)

server_client=ttk.Combobox(window,font=("Arial 10"))
server_client.config(values=["server","client"],state="readonly")
server_client.current(0)
server_client.pack(pady=20 ,fill=X,padx=40)

btn=Button(window,text="start",font="Arial 15",command=Next)
btn.pack(pady=15,fill=X,padx=40)

window.mainloop()
bool_text=False
def copy():
        global bool_text
        while bool_text:pass
        win.clipboard_clear()
        win.clipboard_append(text)  
def text_s():
        global text
        global bool_text
        while True:        
                s.send(cipher.encrypt(code1.get(1.0, END).encode()))
                text = cipher.decrypt(s.recv(1000000)).decode()
                bool_text=True
                code2.config(state="normal")
                if not text==code2.get(1.0,END):
                        code2.delete(1.0, END)
                        code2.insert(END, text)   
                code2.config(state="disabled")
                bool_text=False
                t.sleep(0.2)
def text_c():
        global text
        global bool_text
        while True:
                text = cipher.decrypt(s.recv(1000000)).decode()
                s.send(cipher.encrypt(code1.get(1.0, END).encode()))
                bool_text=True
                code2.config(state="normal")
                if not text==code2.get(1.0,END):
                        code2.delete(1.0, END)
                        code2.insert(END, text)
                code2.config(state="disabled")
                bool_text=False
                t.sleep(0.2)
                
for i in data:
        if i=="":
                sys.exit()

if len(data)!=0:
        if data[3]=="server":
                run=True
                while run:
                        mysocket=socket(AF_INET,SOCK_STREAM)
                        mysocket.bind((data[1],int(data[2])))
                        mysocket.listen(1)
                        s,addr=mysocket.accept()
                        t.sleep(1)
                        if s.recv(40).decode()==HWVL(data[0],40):
                                cipher = Fernet(base64.urlsafe_b64encode(HWVL(data[0],32).encode()))
                                s.send(b"1")
                                run=False
                        else:
                                s.send(b"0")
                                s.close()
                win=Tk()
                win.geometry("800x400")
                win.resizable(0,0)
                btn=Button(win,text="copy",command=copy)
                btn.pack(fill=X,expand=1)
                code1=ScrolledText(win,font=("Arial 15"),width=30)
                code1.pack(fill=BOTH,expand=1,side=LEFT)
                code2=ScrolledText(win,font=("Arial 15"),width=30,state="d")
                code2.pack(fill=BOTH,expand=1,side=RIGHT)
                threading.Thread(target=text_s).start()
                win.mainloop()
                sys.exit()
                
        else:
                s=socket(AF_INET,SOCK_STREAM)
                s.connect((data[1],int(data[2])))
                t.sleep(1)
                s.send(HWVL(data[0],40).encode())
                if s.recv(1).decode()=="1":
                        cipher = Fernet(base64.urlsafe_b64encode(HWVL(data[0],32).encode()))
                        win=Tk()
                        win.geometry("800x400")
                        win.resizable(0,0)
                        btn=Button(win,text="copy",command=copy)
                        btn.pack(fill=X,expand=1)
                        code1=ScrolledText(win,font=("Arial 15"),width=30)
                        code1.pack(fill=BOTH,expand=1,side=LEFT,)
                        code2=ScrolledText(win,font=("Arial 15"),width=30,state="d")
                        code2.pack(fill=BOTH,expand=1,side=RIGHT)
                        threading.Thread(target=text_c).start()
                        win.mainloop()
                        sys.exit()