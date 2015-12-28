#! /usr/bin/env python
# -*- coding: utf-8 -*-

# *************************************************************
#     Filename @  kigh.py
#       Author @  Huoty
#  Create date @  2015-12-25 16:59:16
#  Description @
# *************************************************************

from os import getcwd, path
from time import sleep, strftime, localtime
from re import match
from threading import Thread, current_thread
import pynotify

def parse_conf_file(file_object):
    status = 0  # 状态机： 0 - 初始状态， 1 - 读取休息提醒配置， 2 - 读取代办事项配置
    remind_rest_dict = {}
    todo_list_dict = {}

    file_content = [ line.strip() for line in file_object.readlines() ]
    for line in file_content:
        if len(line) == 0 or line[0] == "#":
            continue
        elif line == "[REST_INTERVAL]":
            status = 1
            continue
        elif line == "[TODO_LIST]":
            status = 2
            continue
        else:
            if line.count("=") != 1:
                continue
            else:
                key, val = [ item.strip() for item in line.split("=") ]
                if status == 1:
                    if not cmp(key, "interval"):
                        remind_rest_dict["interval"] = int(val)
                    elif not cmp(key, "message"):
                        remind_rest_dict["message"] = val
                    else:
                        print "未定义的配置项"
                elif status == 2:
                    todo_list_dict[key] = val
                else:
                    print "未定义的状态"

    return remind_rest_dict, todo_list_dict

def get_conf(conf_item = "all"):
    """
    Return configuration information by
specific configuration Item
    conf_item: all, rest, todo
    """

    user_conf_file = path.expandvars('$HOME') + "/.kigh.conf"
    global_conf_file = path.expandvars('$HOME') + "/kigh.conf"
    if path.exists(user_conf_file) and path.isfile(user_conf_file):
        fp = open(user_conf_file, "r")
    elif path.exists(global_conf_file) and path.isfile(global_conf_file):
        fp = open(global_conf_file, "r")
    else:
        print "没有找到配置文件！"
        return None

    all_conf = parse_conf_file(fp)
    if not cmp(conf_item, "all"):
        return all_conf
    elif not cmp(conf_item, "rest"):
        return all_conf[0]
    elif not cmp(conf_item, "todo"):
        return all_conf[1]
    else:
        print "该配置项（%s）还未定义" % conf_item
        return None


def remind_rest(interval = 30):
    config = get_conf("rest")
    if not config:
        print "未读取到相关配置！"
        return

    title_notify = "休息提醒"
    msg_notify = config["message"] % (config["interval"] / 60.0)
    icon_notify = getcwd() + "/alarm_clock_time_32px_.png"
    pynotify.init("Rest-reminder")
    rnotify = pynotify.Notification(title_notify, msg_notify, icon_notify)
    rnotify.set_timeout(15000)
    rnotify.set_urgency("normal")
    while True:
        try:
            sleep(interval)
            rnotify.show()
        except Exception, e:
            print e

def remind_todo():
    config = get_conf("todo")
    if not config:
        print "未读取到相关配置！"
        return

    todo_everyday = {}
    todo_exact = {}
    for key, val in config.items():
        if match("Everyday [\d]{2}:[0-6]{2}:[0-6]{2}", key.strip()):
            conf_time = key.split()[1]
            todo_everyday[conf_time] = val
        elif match("[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[0-6]{2}:[0-6]{2}", key.strip()):
            todo_exact[key] = val
            #print "Other: ", val
        else:
            print "配置内容格式不正确！"

    title_notify = "待办事项"
    icon_notify = getcwd() + "/alarm_clock_time_32px_.png"
    while True:
        if todo_everyday:
            for conf_time, message in todo_everyday.items():
                curr_time = strftime("%H:%M:%S", localtime())
                if not cmp(conf_time, curr_time):
                    pynotify.init("Todo-reminder")
                    rnotify = pynotify.Notification(title_notify, message, icon_notify)
                    rnotify.set_timeout(15000)
                    rnotify.set_urgency("normal")
                    rnotify.show()

        if todo_exact:
            for conf_time, message in todo_exact.items():
                curr_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
                if not cmp(conf_time, curr_time):
                    pynotify.init("Todo-reminder")
                    rnotify = pynotify.Notification(title_notify, message, icon_notify)
                    rnotify.set_timeout(15000)
                    rnotify.set_urgency("normal")
                    rnotify.show()

    curr_time = strftime("%H:%M:%S", localtime())
    # msg_notify = config["message"] % (config["interval"] / 60.0)
    # icon_notify = getcwd() + "/alarm_clock_time_32px_.png"
    # pynotify.init ("Rest-reminder")
    # rnotify = pynotify.Notification (title_notify, msg_notify, icon_notify)
    # rnotify.set_timeout(15000)
    # rnotify.set_urgency("normal")
    # while True:
    #     try:
    #         sleep(interval)
    #         rnotify.show()
    #     except Exception, e:
    #         print e

# Script starts from here

if __name__ == "__main__":
    # print('thread %s is running...' % current_thread().name)
    # thread_remind_rest =  Thread(target=remind_rest, name='RemindRestThread')
    # thread_remind_rest.start()
    # thread_remind_rest.join()
    # print('thread %s ended.' % current_thread().name)
    remind_todo()
