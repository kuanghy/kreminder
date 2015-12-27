#! /usr/bin/env python
# -*- coding: utf-8 -*-

# *************************************************************
#     Filename @  kigh.py
#       Author @  Huoty
#  Create date @  2015-12-25 16:59:16
#  Description @  
# *************************************************************

from os import getcwd
from time import sleep
from threading import Thread, current_thread
import pynotify

def remind_rest(interval = 30):
    title_notify = "休息提醒"
    msg_notify = "您已经连续工作 0.1 小时，适当休息有益于健康！"
    icon_notify = getcwd() + "/alarm_clock_time_32px_.png"
    pynotify.init ("Rest-reminder")  
    rnotify = pynotify.Notification (title_notify, msg_notify, icon_notify)  
    rnotify.set_timeout(5000)
    rnotify.set_urgency("normal")
    while True:
        sleep(interval)
        rnotify.show()



# Script starts from here

if __name__ == "__main__":
    print('thread %s is running...' % current_thread().name)
    thread_remind_rest =  Thread(target=remind_rest, name='RemindRestThread')
    thread_remind_rest.start()
    thread_remind_rest.join()
    print('thread %s ended.' % current_thread().name)
