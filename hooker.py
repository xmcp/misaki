#! python2
#coding=utf-8

import pyHook
import pythoncom
import multiprocessing
import const

def keydown(event):
    keyqueue.put([True,event.Key])
    return True

def keyup(event):
    keyqueue.put([False,event.Key])
    return True

def mousebtn(event):
    try:
        mousequeue.put(const.mouse_evt_name[event.MessageName])
    except KeyError:
        print 'unrecognized mouse event:',event.MessageName
    finally:
        return True

def mousewheel(event):
    mousequeue.put([event.Wheel<0,-1])
    return True
    
def run_forever(kq,mq):
    global keyqueue,mousequeue
    keyqueue=kq
    mousequeue=mq
    hm=pyHook.HookManager()
    
    hm.SubscribeKeyDown(keydown)
    hm.SubscribeKeyUp(keyup)
    hm.SubscribeMouseAllButtonsDown(mousebtn)
    hm.SubscribeMouseAllButtonsUp(mousebtn)
    hm.SubscribeMouseWheel(mousewheel)
    
    hm.HookKeyboard()
    hm.HookMouse()
    print 'hook start'
    while True:
        pythoncom.PumpWaitingMessages()
