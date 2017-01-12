#! python2
#coding=utf-8

import hooker
import const
import threading
import Queue as queue

from Tkinter import *
from ttk import *

tk=Tk()
tk.title('Misaki Toolbar')
tk.attributes('-topmost',True)
tk.configure(background='black')
tk.geometry('500x27')
s=Style(tk)
s.configure('BtnOn.TLabel',background='yellow',foreground='black',font='Consolas -20')
s.configure('BtnOff.TLabel',background='#666',foreground='white',font='Consolas -20')
s.configure('Black.TFrame',background='black')

tk.columnconfigure(0,weight=1)
keyframe=Frame(tk,style='Black.TFrame')
keyframe.grid(row=0,column=0,sticky='we')
mouseframe=Frame(tk)
mouseframe.grid(row=0,column=1)

mousebtn=[
    Label(mouseframe,text='[ ',style='BtnOff.TLabel'),
    Label(mouseframe,text='|',style='BtnOff.TLabel'),
    Label(mouseframe,text=' ]',style='BtnOff.TLabel'),
]
for ind,lbl in enumerate(mousebtn):
    lbl.grid(row=0,column=ind)

class Keyboarder:
    def __init__(self):
        self.labels={}
        self.alive_keys=set()
        self.lbindex=0
        self.pressed=0
        self.lock=threading.Lock()

    def _clear(self):
        for item in self.labels.values():
            print 'clear key',item
            tk.after_idle(item.grid_forget)
        self.labels={}
        self.lbindex=0
        
    def push(self,key):
        if not self.alive_keys: # clear history
            self._clear()
        self.alive_keys.add(key)
        
        if key not in self.labels:
            print 'key down',key
            def holy_after():
                self.labels[key]=Label(keyframe,text=key,style='BtnOn.TLabel')
                self.labels[key].grid(row=0,column=self.lbindex)
                self.lbindex+=1
                #self.lock.release()
                print 'key down-done',self.pressed

            #self.lock.acquire()
            tk.after_idle(holy_after)
        else:
            print 'key revive',key
            self.labels[key]['style']='BtnOn.TLabel'
    
    def pop(self,key):
        self.alive_keys.discard(key)
        def holy_after():
            with self.lock:
                if key in self.labels:
                    self.labels[key]['style']='BtnOff.TLabel'
                    print 'key up-done',self.pressed
                else:
                    print 'key up-ignored',key
        tk.after(50,holy_after)

    def try_clear(self):
        if not self.alive_keys:
            self._clear()
            
class Mouser:
    def __init__(self):
        self.after_id=None
        
    def push(self,key):
        print 'mouse down',key
        mousebtn[key]['style']='BtnOn.TLabel'
    
    def pop(self,key):
        print 'mouse up',key
        mousebtn[key]['style']='BtnOff.TLabel'
        
    def wheel(self,scroll_down):
        mousebtn[1]['style']='BtnOn.TLabel'
        mousebtn[1]['text']='↓' if scroll_down else '↑'
        def holy_after():
            mousebtn[1]['text']='|'
            mousebtn[1]['style']='BtnOff.TLabel'
        if self.after_id:
            tk.after_cancel(self.after_id)
        self.after_id=tk.after(50,holy_after)

mckey=Keyboarder()
mcmouse=Mouser()
    
def run_thread(target):
    t=threading.Thread(target=target)
    t.setDaemon(True)
    t.start()

def key_fetcher():
    while True:
        try:
            typ,code=hooker.keyqueue.get(block=True,timeout=.5)
        except queue.Empty:
            mckey.try_clear()
        else:
            code=' %s '%const.friendly_name.get(code,code)
            if typ: # keydown
                mckey.push(code)
            else: # keyup
                mckey.pop(code)

def mouse_fetcher():
    while True:
        typ,code=hooker.mousequeue.get(block=True)
        if code==-1:
            mcmouse.wheel(typ)
        elif typ==True:
            mcmouse.push(code)
        else:
            mcmouse.pop(code)
                
run_thread(key_fetcher)
run_thread(mouse_fetcher)
run_thread(hooker.run_forever)
mainloop()