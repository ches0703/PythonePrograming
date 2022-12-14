# User-defined module - Class_TextChat.py
# HomeWork 12 - 01
"""
Project : TextChat
Author: Eun-seong Choi
Date of last update: 2022 / 12 / 01
Update list:
    - v1.1 : 12 / 01
        Make Class : TextChat
            __init__, sockRecvMsg, sockSendMsg, _quit, createWidgets
        Add commit & Retouch variable name
        Make Application file : TextChat_Server, TextChat_Client 
"""
import socket           # for comunicate
import threading        # for multi-thread
from time import sleep  # for switching
# for GUI interface
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import END


LocalHost = "127.0.0.1"         # IP address : For use Local host
SocketChat_PortNumber = 24000   # Port Number : set Port 24000


class TextChat():
    def __init__(self, mode):
        # Get variavle data part
        global host_address     # global variable : Host's IP
        self.mode = mode        # Set Mode : "Server" or "Client"
        host_name = socket.gethostname()                 # Get host's name
        host_address = socket.gethostbyname(host_name)   # Get host's IP address
        print("My ({}) IP address = {}".format(self.mode, host_address))
        self.my_address = host_address
        sleep(1)

        # GUI Part
        self.win = tk.Tk()  # make window
        self.win.title("Python Socket-based TextChat ({})"
                       .format(self.mode))  # Set window's title
        self.createWidgets()

        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Make Socket, for use TCP
        # Run by mode
        if self.mode == "Server":   # Run by Server
            # Insert sever adderss(my adress) to server_address_entry
            self.server_address_entry.insert(END, self.my_address)
            # Bind socket to (Host's IP Adress, port_number)
            self.mySocket.bind((host_address, SocketChat_PortNumber))
            # Print status in GUI
            self.scrDisplay.insert(tk.INSERT, "TCP server is waiting for a client .... \n")
            self.mySocket.listen(1)     # Waiating for Connection
            # if detect connection request : accept
            self.conection, self.client_address = self.mySocket.accept()
            # Print Client Adress in Shell
            print("TCP Server is connected to client ({})\n".format(self.client_address))
            # Print Conection state & Client Adress in GUI
            self.scrDisplay.insert(tk.INSERT, "TCP server is connected to client\n")
            self.scrDisplay.insert(tk.INSERT, "TCP client IP address : {}\n".format(self.client_address[0]))
            self.client_address_entry.insert(END, self.client_address[0])
        elif self.mode == "Client":  # Run by Cliente
            self.client_address = self.my_address                   # Set client_address by my_address
            self.client_address_entry.insert(END, self.my_address)  # Print client_address(my_address) in GUI
            server_address_str = input("Server IP Addr = ")         # Get server's IP address from shell
            # Send connect request to TCP server
            self.mySocket.connect((server_address_str, SocketChat_PortNumber))  
            self.server_address = self.mySocket.getpeername()       # Get connented host(server)'s data : IP address
            print("TCP Client is connected to server ({})\n".format(self.server_address))
            # Print Conection state & Server Adress in GUI
            self.scrDisplay.insert(tk.INSERT, "TCP client is connected to server \n")
            self.scrDisplay.insert(tk.INSERT, "TCP server IP address : {}\n".format(self.server_address[0]))
            self.server_address_entry.insert(END, self.server_address[0])
            self.conection = self.mySocket

        # Start TCP/IP server in its own thread
        thread_sockRecvMsg = threading.Thread(target=self.sockRecvMsg, daemon=True)
        thread_sockRecvMsg.start()
    
    # Get Data from other host
    def sockRecvMsg(self):
        while True:
            # Recieve msg = Decode Recive data
            recvMsg = self.conection.recv(512).decode()     
            if not recvMsg:
                break
            # Print Recive msg in GUI
            self.scrDisplay.insert(tk.INSERT, ">> " + recvMsg)
        self.conection.close()

    # Send Data from other host
    def sockSendMsg(self):
        msgToPeer = str(self.scrTextInput.get(1.0, END))        # Read the msg from Input Area
        self.scrDisplay.insert(tk.INSERT, "<< " + msgToPeer)    # Print send msg in GUI
        self.conection.send(bytes(msgToPeer.encode()))          # Send the msg
        self.scrTextInput.delete(1.0, END)                      # Clear scr_msgInput scrolltext

    # Exit GUI cleanly; definition of quit()
    def _quit(self):
        self.win.quit()
        self.win.destroy()
        exit()

    # GUI Part : createWidgets()
    def createWidgets(self):
        # Add a frame in self.win
        frame = ttk.LabelFrame(self.win, text="Frame(Socket-based Text Chatting)")
        frame.grid(column=0, row=0, padx=8, pady=4)

        # Add a LabelFrame of myAddr, peerAddr, Connect Button in frame
        frame_address_connect = ttk.LabelFrame(frame, text="")
        frame_address_connect.grid(column=0, row=0, padx=40, pady=20, columnspan=2)

        # Add labels (myAddr, peerAddr) in the frame_addr_connect
        server_address_label = ttk.Label(frame_address_connect, text="Server address")
        server_address_label.grid(column=0, row=0, sticky='W')
        client_address_label = ttk.Label(frame_address_connect, text="Client address")
        client_address_label.grid(column=1, row=0, sticky='W')
        
        # Add a Textbox Entry widgets (myAddr, peerAddr) in the frame_addr_connect
        self.server_address = tk.StringVar()
        self.server_address_entry = ttk.Entry(frame_address_connect, width=15, textvariable="")
        self.server_address_entry.grid(column=0, row=1, sticky='W')

        self.client_address = tk.StringVar()
        self.client_address_entry = ttk.Entry(frame_address_connect, width=15, textvariable="")
        self.client_address_entry.grid(column=1, row=1, sticky='W')

        # Add ScrolledText fields of display and input
        scrol_w, scrol_h = 40, 20
        msgDisplay_label = ttk.Label(frame, text="Mesage Display ({})".format(self.mode))
        msgDisplay_label.grid(column=0, row=1)
        self.scrDisplay = scrolledtext.ScrolledText(frame, width=scrol_w, height=scrol_h, wrap=tk.WORD)
        self.scrDisplay.grid(column=0, row=2, sticky='E')
        
        msgInput_label = ttk.Label(frame, text="Input Text Message ({}) :".format(self.mode))
        msgInput_label.grid(column=0, row=3)
        
        self.scrTextInput = scrolledtext.ScrolledText(frame, width=40, height=3, wrap=tk.WORD)
        self.scrTextInput.grid(column=0, row=4)  # columnspan=3
        
        # Add Buttons (cli_send, serv_send)
        txButton = ttk.Button(frame, text="Send Message to Peer", command=self.sockSendMsg)
        txButton.grid(column=0, row=5, sticky='E')

        # Place cursor into the message input scrolled text
        self.scrTextInput.focus()
    
        
