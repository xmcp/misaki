#! python2
#coding=utf-8
from __future__ import print_function

import hooker
import const

import threading
import multiprocessing
import Queue as queue
import time

from Tkinter import *
from ttk import *

if not const.print_log:
    print=lambda *__,**_:None

if __name__=='__main__':
    multiprocessing.freeze_support()
    keyqueue=multiprocessing.Queue()
    mousequeue=multiprocessing.Queue()

    tk=Tk()
    tipvar=StringVar(value='...')
    
    tk.title('Misaki Toolbar')
    tk.attributes('-topmost',True)
    tk.resizable(True,False)
    tk.configure(background='black')
    tk.geometry('800x27')
    s=Style(tk)
    s.configure('BtnOn.TLabel',background='yellow',foreground='black',font='Consolas -20')
    s.configure('BtnOff.TLabel',background='#666',foreground='white',font='Consolas -20')
    s.configure('Black.TFrame',background='black')

    tk.rowconfigure(0,weight=1)
    tk.columnconfigure(1,weight=1)
    Label(tk,textvariable=tipvar,foreground='white',background='black',font='Consolas -20').grid(row=0,column=0)
    keyframe=Frame(tk,style='Black.TFrame')
    keyframe.grid(row=0,column=1,sticky='we')
    mouseframe=Frame(tk)
    mouseframe.grid(row=0,column=2)

    mousebtn=[
        Label(mouseframe,text='[ ',style='BtnOff.TLabel'),
        Label(mouseframe,text='|',style='BtnOff.TLabel'),
        Label(mouseframe,text=' ]',style='BtnOff.TLabel'),
    ]
    for ind,lbl in enumerate(mousebtn):
        lbl.grid(row=0,column=ind)

_current_callbacks={}
def register_after(delay,channel,callback):
    def wrapped(*__,**_):
        del _current_callbacks[channel]
        callback(*__,**_)
    
    if channel in _current_callbacks:
        tk.after_cancel(_current_callbacks[channel])
    _current_callbacks[channel]=tk.after(delay,wrapped)
        
class Keyboarder:
    def __init__(self):
        self.labels={}
        self.alive_keys=set()
        self.lbindex=0
        self.clearlock=threading.Event()

    def _clear(self):
        if not self.labels:
            return
        print('clear label',len(self.labels))
        def holy_after():
            for item in self.labels.values():
                item.grid_forget()
            self.labels={}
            self.clearlock.set()
            print('-- clear ok')
        self.lbindex=0
        print('-- clear start')
        tk.after_idle(holy_after)
        self.clearlock.wait()
        self.clearlock.clear()
        
    def push(self,key):
        if not self.alive_keys: # clear history
            self._clear()
            print('-- clear continue')
        self.alive_keys.add(key)
        
        if key not in self.labels:
            print('key down',key)
            def holy_after():
                self.labels[key]=Label(keyframe,text=key,style='BtnOn.TLabel')
                self.labels[key].grid(row=0,column=self.lbindex)
                self.lbindex+=1
                #print('key down-done',len(self.alive_keys))
            tk.after_idle(holy_after)
        else:
            print('key revive',key)
            self.labels[key]['style']='BtnOn.TLabel'
    
    def pop(self,key):
        self.alive_keys.discard(key)
        def holy_after():
            if key in self.labels:
                self.labels[key]['style']='BtnOff.TLabel'
                print('key up',key,'/ alive keys =',len(self.alive_keys))
            else:
                print('key up-ignored',key)
        tk.after(50,holy_after)

    def try_clear(self):
        if not self.alive_keys:
            self._clear()
            
class Mouser:
    def __init__(self):
        pass
        
    def push(self,key):
        print('mouse down',key)
        mousebtn[key]['style']='BtnOn.TLabel'
    
    def pop(self,key):
        print('mouse up',key)
        def holy_after():
            mousebtn[key]['style']='BtnOff.TLabel'
        register_after(50,'mouse %s'%key,holy_after)
        
    def wheel(self,scroll_down):
        mousebtn[1]['style']='BtnOn.TLabel'
        mousebtn[1]['text']='↓' if scroll_down else '↑'
        def holy_after():
            mousebtn[1]['text']='|'
            mousebtn[1]['style']='BtnOff.TLabel'
        register_after(100,'wheel',holy_after)

mckey=Keyboarder()
mcmouse=Mouser()
    
def run_thread(target):
    t=threading.Thread(target=target)
    t.setDaemon(True)
    t.start()

def key_fetcher():
    alpha_flag=1
    while True:
        try:
            typ,code=keyqueue.get(block=True,timeout=.5)
        except queue.Empty:
            mckey.try_clear()
        else:
            dispcode=' %s '%const.friendly_name.get(code,code)
            if typ: # keydown
                mckey.push(dispcode)
                if code=='Pause':
                    alpha_flag=1-alpha_flag
                    tk.after_idle(tk.attributes,'-alpha',alpha_flag)
                    tk.after_idle(tk.attributes,'-toolwindow',1-alpha_flag)
                    #tk.after_idle(tk.focus_force)
            else: # keyup
                mckey.pop(dispcode)

def mouse_fetcher():
    while True:
        typ,code=mousequeue.get(block=True)
        if code==-1:
            mcmouse.wheel(typ)
        elif typ==True:
            mcmouse.push(code)
        else:
            mcmouse.pop(code)

def tipper():
    while True:
        tipvar.set(time.strftime(const.tip_format,time.localtime()))
        time.sleep(1-time.time()%1+.1)

if __name__=='__main__':
    run_thread(key_fetcher)
    run_thread(mouse_fetcher)
    run_thread(tipper)
    p=multiprocessing.Process(target=hooker.run_forever,args=(keyqueue,mousequeue))
    p.daemon=True
    p.start()
    mainloop()