#! /usr/bin/env python
# -*- coding: utf-8 -*-

# *************************************************************
#     Filename @  kreminder.py
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
    Return configuration information by specific configuration Item
    conf_item: all, rest, todo
    """

    user_conf_file = path.expandvars('$HOME') + "/.config/kreminder.py"
    global_conf_file =  "/etc/kreminder.conf"
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
    icon_notify = getcwd() + "/icon/clock_32x32.png"
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

    event_list = []
    title_notify = "待办事项"
    icon_notify = getcwd() + "/icon/clock_32x32.png"
    for time, message in config.items():
        if match("Everyday [\d]{2}:[\d]{2}:[\d]{2}", time.strip()):
            pynotify.init("Todo-reminder-" + time.split()[1])
            rnotify = pynotify.Notification(title_notify, message, icon_notify)
            rnotify.set_timeout(15000)
            rnotify.set_urgency("normal")
            remind_item = {"conf_time": time.split()[1], "notify_obj": rnotify}
            event_list.append(remind_item)
        elif match("[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}", time.strip()):
            pynotify.init("Todo-reminder-" + time.split()[1])
            rnotify = pynotify.Notification(title_notify, message, icon_notify)
            rnotify.set_timeout(15000)
            rnotify.set_urgency("normal")
            remind_item = {"conf_time": time.strip(), "notify_obj": rnotify}
            event_list.append(remind_item)
        else:
            print "配置内容格式不正确！", time, message

    if event_list:
        while True:
            for remind_item in event_list:
                curr_time = strftime("%H:%M:%S", localtime())
                curr_date = strftime("%Y-%m-%d %H:%M:%S", localtime())
                if remind_item["conf_time"] == curr_time or remind_item["conf_time"] == curr_date:
                    remind_item["notify_obj"].show()

                del curr_time
                del curr_date
                del remind_item

def startup_notice():
    help_file = getcwd() + "/man/readme.html"
    icon_notify = getcwd() + "/icon/hint_32x32.png"
    title_notify = "启动通知"
    msg_notify = 'Kreminder 已经启动，点击<a href="' + help_file + '">这里</a>可以查看帮助！'
    pynotify.init("Startup-notice")
    rnotify = pynotify.Notification(title_notify, msg_notify, icon_notify)
    rnotify.set_timeout(15000)
    rnotify.set_urgency("normal")
    rnotify.show()

# Script starts from here

if __name__ == "__main__":
    startup_notice()
    # print('thread %s is running...' % current_thread().name)
    # thread_remind_rest =  Thread(target=remind_rest, name='RemindRestThread')
    # thread_remind_rest.start()
    # thread_remind_rest.join()
    # print('thread %s ended.' % current_thread().name)
    #remind_rest()
    remind_todo()
