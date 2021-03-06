#! /usr/bin/env python
#
# GUI module generated by PAGE version 4.5
# In conjunction with Tcl version 8.6
#    Jun 11, 2015 02:30:47 PM
import sys
from collectOptions2 import *

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

import options_file_support
import thread
import time



def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    root.title('New_Toplevel_1')
    geom = "287x289+464+429"
    root.geometry(geom)
    w = New_Toplevel_1 (root)
    options_file_support.init(root, w)
    root.mainloop()
    return root

w = None
def create_New_Toplevel_1(root, param=None):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    w.title('New_Toplevel_1')
    geom = "287x289+464+429"
    w.geometry(geom)
    w_win = New_Toplevel_1 (w)
    options_file_support.init(w, w_win, param)
    return w_win

def destroy_New_Toplevel_1():
    global w
    w.destroy()
    w = None

def go(stock_value,file_name):
    enter_stock_symbol = False
    #display_header()
    if enter_stock_symbol == False:
        user_input = stock_value
        print "User Input",user_input
        enter_stock_symbol = checkStockSymbol(user_input)
        if enter_stock_symbol == True:
            end_result = getOptionPrices(user_input,file_name)
            if end_result == False:
                new_text = Text(root,height=2, width = 30)
                new_text.pack()
                new_text.insert(END,"Market is Closed")
            else:
                new_text = Text(root,height=2, width = 30)
                new_text.pack()
                new_text.insert(END,"Collecting Data")
                #root.after(100000,go(stock_value,file_name))

class New_Toplevel_1:
    def __init__(self, master=None):
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 
        master.configure(background="#d9d9d9")
        master.configure(highlightbackground="#d9d9d9")
        master.configure(highlightcolor="black")


        self.stock_symbol_input = Text(master)
        self.stock_symbol_input.place(relx=0.52, rely=0.24, relheight=0.08
                , relwidth=0.26)
        self.stock_symbol_input.configure(background="white")
        self.stock_symbol_input.configure(font="TkTextFont")
        self.stock_symbol_input.configure(foreground="black")
        self.stock_symbol_input.configure(highlightbackground="#d9d9d9")
        self.stock_symbol_input.configure(highlightcolor="black")
        self.stock_symbol_input.configure(insertbackground="black")
        self.stock_symbol_input.configure(selectbackground="#c4c4c4")
        self.stock_symbol_input.configure(selectforeground="black")
        self.stock_symbol_input.configure(width=74)
        self.stock_symbol_input.configure(wrap=WORD)

        self.Label1 = Label(master)
        self.Label1.place(relx=0.28, rely=0.07, height=41, width=131)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background=_bgcolor)
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Options Data Collector''')

        self.start_button = Button(text="Start",command=lambda: self.start_button.after(100000,go(self.stock_symbol_input.get("1.0",'end-1c'),self.file_name_input.get("1.0",'end-1c'))))
        self.start_button.place(relx=0.21, rely=0.52, height=24, width=67)
        self.start_button.configure(activebackground="#d9d9d9")
        self.start_button.configure(activeforeground="#000000")
        self.start_button.configure(background=_bgcolor)
        self.start_button.configure(disabledforeground="#a3a3a3")
        self.start_button.configure(foreground="#000000")
        self.start_button.configure(highlightbackground="#d9d9d9")
        self.start_button.configure(highlightcolor="black")
        self.start_button.configure(pady="0")
        self.start_button.configure(text='''Start''')

        self.file_name_input = Text(master)
        self.file_name_input.place(relx=0.52, rely=0.38, relheight=0.08
                , relwidth=0.26)
        self.file_name_input.configure(background="white")
        self.file_name_input.configure(font="TkTextFont")
        self.file_name_input.configure(foreground="black")
        self.file_name_input.configure(highlightbackground="#d9d9d9")
        self.file_name_input.configure(highlightcolor="black")
        self.file_name_input.configure(insertbackground="black")
        self.file_name_input.configure(selectbackground="#c4c4c4")
        self.file_name_input.configure(selectforeground="black")
        self.file_name_input.configure(width=74)
        self.file_name_input.configure(wrap=WORD)

        self.stop_button = Button(master, command="break")
        self.stop_button.place(relx=0.56, rely=0.52, height=24, width=67)
        self.stop_button.configure(activebackground="#d9d9d9")
        self.stop_button.configure(activeforeground="#000000")
        self.stop_button.configure(background=_bgcolor)
        self.stop_button.configure(disabledforeground="#a3a3a3")
        self.stop_button.configure(foreground="#000000")
        self.stop_button.configure(highlightbackground="#d9d9d9")
        self.stop_button.configure(highlightcolor="black")
        self.stop_button.configure(pady="0")
        self.stop_button.configure(text='''Stop''')

        self.menubar = Menu(master,bg=_bgcolor,fg=_fgcolor)
        master.configure(menu = self.menubar)



        self.symbol_label = Label(master)
        self.symbol_label.place(relx=0.24, rely=0.24, height=21, width=78)
        self.symbol_label.configure(activebackground="#f9f9f9")
        self.symbol_label.configure(activeforeground="black")
        self.symbol_label.configure(background=_bgcolor)
        self.symbol_label.configure(disabledforeground="#a3a3a3")
        self.symbol_label.configure(foreground="#000000")
        self.symbol_label.configure(highlightbackground="#d9d9d9")
        self.symbol_label.configure(highlightcolor="black")
        self.symbol_label.configure(text='''Stock Symbol''')

        self.file_name_label = Label(master)
        self.file_name_label.place(relx=0.28, rely=0.38, height=21, width=59)
        self.file_name_label.configure(activebackground="#f9f9f9")
        self.file_name_label.configure(activeforeground="black")
        self.file_name_label.configure(background=_bgcolor)
        self.file_name_label.configure(disabledforeground="#a3a3a3")
        self.file_name_label.configure(foreground="#000000")
        self.file_name_label.configure(highlightbackground="#d9d9d9")
        self.file_name_label.configure(highlightcolor="black")
        self.file_name_label.configure(text='''File Name''')

        # self.messages_output = Text(master)
        # self.messages_output.place(relx=0.21, rely=0.66, relheight=0.22
        #         , relwidth=0.57)
        # self.messages_output.configure(background="white")
        # self.messages_output.configure(font="TkTextFont")
        # self.messages_output.configure(foreground="black")
        # self.messages_output.configure(highlightbackground="#d9d9d9")
        # self.messages_output.configure(highlightcolor="black")
        # self.messages_output.configure(insertbackground="black")
        # self.messages_output.configure(selectbackground="#c4c4c4")
        # self.messages_output.configure(selectforeground="black")
        # self.messages_output.configure(width=164)
        # self.messages_output.configure(wrap=WORD)


if __name__ == '__main__':
    vp_start_gui()