#client side software    

import socket
import threading
import subprocess
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import Menu    
from tkinter import ttk
from datetime import datetime
import emoji
host = socket.gethostname()
port = int(input())
 
        
class Client:

    def __init__(self, host, port):
        self.ke = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.bx = 0

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Please enter a nickname: ", parent=msg)
        self.nickname = simpledialog.askstring("Nickname1", "Please enter a nickname1: ", parent=msg)
        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        recieve_tread = threading.Thread(target=self.recieve)
        sd = threading.Thread(target=self.recive1)
        sd.start()
        recieve_tread.start()
        gui_thread.start()

    def gui_loop(self):        
        self.win = tkinter.Tk()
        self.win.configure(bg="lightGray")
        self.win.title("local CHAT")
        self.win.resizable(width=True, height=True)
        self.win.iconbitmap('ICON.ico')
        self.win.grid_columnconfigure(0, weight=1)

        # self.text_label = tkinter.Label(self.win, text="Chat: ", bg="lightgray")
        # self.text_label.config(font=("Arial", 12))
        # self.text_label.grid(padx=20, pady=5)
        
        self.menu = Menu(self.win)  
        self.new_item = Menu(self.menu)  
        self.new_item.add_command(label='Новый', command=self.__init__)  
        self.menu.add_cascade(label=f'{host} : {port}', menu=self.new_item)  
        self.win.config(menu=self.menu)  

        self.text_Area = tkinter.scrolledtext.ScrolledText(self.win, font=('Arial', 20), height=15)
        self.text_Area.grid(row=0, column=0)
        self.text_Area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Massage: ", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.grid(row=1, column=0, sticky="nsew")



        self.input_area = tkinter.Text(self.win, height=5)
        self.input_area.grid(row=2, column=0, sticky="nsew")

        massage = f'{self.nickname}'
        self.sock.send(massage.encode('utf-8'))

        self.send_button = tkinter.Button(self.win, text="send", command=self.write)
        self.send_button.config(font=('Arial', 12))
        self.send_button.grid(row=3, column=0,sticky="nsew")

        self.participantarea = tkinter.scrolledtext.ScrolledText(self.win)

        self.participantarea.config(width=20)
        self.participantarea.grid(row=0, column=1)
        self.participantarea.config(state='disabled')

        self.chat_button = tkinter.Button(self.win, text="Clean", command=self.clean)
        self.chat_button.grid(row=4, column=1)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        

        self.win.mainloop()

    def clean(self):
        self.msg_label.config(text="")
        self.participantarea.config()
        self.input_area.delete(1.0, 'end-1c')

            

    def write(self):
        massage = self.input_area.get(1.0, 'end-1c')
        self.sock.send(f'{datetime.now().strftime("%H:%M:%S")}, {self.nickname}&**&* {massage}'.encode('utf-8'))
        self.input_area.delete(1.0, 'end-1c')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def participates(self):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((host, 9098))
        name = connection.recv(1024).decode('utf-8')
        if name != '':
            self.participantarea.config(state='enabled')
            self.participantarea.insert('end', name)
            self.participantarea.yview('end')
            self.participantarea.config(state='disabled')



    def recieve(self):
        while self.running:
            try:
                massage = self.sock.recv(1024).decode('utf-8')
                spillitted = massage.split("&**&*")
                if ':(' in massage:
                    ksfds = massage.find(':(')
                    k = emoji.emojize(':frowning_face:')
                    massage = str(massage).replace(':(', str(k))

                elif ':)' in massage:
                    ksfds = massage.find(':)')
                    k = emoji.emojize(':grinning_face_with_big_eyes:')
                    massage = str(massage).replace(':)', str(k))

                elif ':|' in massage:
                    ksfds = massage.find(':|')
                    k = emoji.emojize(':neutral_face:')
                    massage = str(massage).replace(':|', str(k))

                if massage == "NICK":
                    self.sock.send(self.nickname.encode('utf-8'))


                else:
                    if self.gui_done:
                        t = massage.replace('&**&*', '')
                        self.text_Area.config(state='normal')
                        self.text_Area.insert('end', t + '\n')
                        self.text_Area.yview('end')
                        self.text_Area.config(state='disabled')

            except ConnectionAbortedError:
                break

            except:
                print("Error")
                self.sock.close()
                break


    def recive1(self):
       self.sock.send(self.nickname.encode('utf-8'))
       while self.running:

            try:
                self.massage12 = self.sock.recv(1024).decode('utf-8')
                self.splited = self.massage12.split('&**&*')

                if self.splited[1] not in self.ke:
                    self.participantarea.config(state='normal')
                    self.participantarea.insert('end', self.splited[1] + '\n')
                    self.text_Area.yview('end')
                    self.participantarea.config(state='disabled')
                    self.ke.append(self.splited[1])

                if self.gui_done:
                    t = self.massage12.replace('&**&*', '')
                    self.text_Area.config(state='normal')
                    self.text_Area.insert('end', t + '\n')
                    self.text_Area.yview('end')
                    self.text_Area.config(state='disabled')
                else:
                    pass

            except IndexError:
                pass



tread = threading.Thread(target=Client, args=(host, port))
tread.start()

#server side software
import threading



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host, port))

s.listen()

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s2.bind((host, 8080))
s2.listen()

clients = []
nicknames = []

fclients = []
fnicknames = []




def broadcast(massage):
    for client in clients:
        client.send(massage)




def handle(client):
    while True:
        try:

            # now = datetime.now().time().strftime("%H:%M:%S")  # time object
            # date = datetime.now().strftime("%Y-%m-%d")  # date object
            massage = client.recv(1024)
            # massage = f'[{date}] {now}: {massage}'
            broadcast(massage)



        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


def recieve():
    while True:
        client, address = s.accept()
        print(F"Connected with {address}, {client}")
        # client.send("NICKNAME?".encode('utf-8'))
        nickname = client.recv(1024)
        nicknames.append(nickname)
        print(f'{client} + {nickname} + {address}')
        broadcast(f"{nickname} connected with server \n".encode('utf-8'))
        # client.send("connected to server".encode('utf-8'))
        clients.append(client)
        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()



print("server is running")
recieve()