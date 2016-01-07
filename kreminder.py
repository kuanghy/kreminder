#! /usr/bin/env python
# -*- coding: utf-8 -*-

# *************************************************************
#     Filename @  kreminder.py
#       Author @  Huoty
#  Create date @  2015-12-25 16:59:16
#  Description @
# *************************************************************

from os import getcwd, path, makedirs
from time import sleep, strftime, localtime
from re import match
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from random import sample
from PyQt4.QtGui import QApplication
from trayIcon import TrayIcon
import pynotify
import sys
import logging
logging.basicConfig()

def get_random_str(length):
    """
    Generating random number
    """

    chars = "qwertyuiopasdfghjklzxcvbnm1234567890"
    return "".join(sample(chars, length))

def log(msg, type = "info"):
    """
    Write information to log file.
    type: info, warn, error
    """

    log_dir = path.expandvars('$HOME') + "/.log/kreminder"
    log_file  = log_dir + "/kreminder.log"
    if not path.exists(log_dir):
        makedirs(log_dir)

    curr_time = "[ " + strftime("%Y-%m-%d %H:%M:%S", localtime()) + " " + " ]"
    if type == "info":
        content = curr_time + " <INFO> " + msg + "\n"
    elif type == "warn":
        content = curr_time + " <WARNNING> " + msg + "\n"
    elif type == "error":
        content = curr_time + " <ERROR> " + msg + "\n"
    else:
        content = curr_time + "没有定义的日志类型！\n"

    file_object = open(log_file, "a")
    file_object.write(content)
    file_object.close()

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
                        log(key + " 是未定义的配置项.", "error")
                elif status == 2:
                    todo_list_dict[key] = val
                else:
                    log("在解析配置文件时出现未定义的状态： " + status, "error")

    return remind_rest_dict, todo_list_dict

def get_conf(conf_item = "all"):
    """
    Return configuration information by specific configuration Item
    conf_item: all, rest, todo
    """

    user_conf_file = path.expandvars('$HOME') + "/.config/kreminder.conf"
    global_conf_file =  "/etc/kreminder.conf"
    if path.exists(user_conf_file) and path.isfile(user_conf_file):
        fp = open(user_conf_file, "r")
    elif path.exists(global_conf_file) and path.isfile(global_conf_file):
        fp = open(global_conf_file, "r")
    else:
        log("没有找到配置文件.", "error")
        return None

    all_conf = parse_conf_file(fp)
    if not cmp(conf_item, "all"):
        return all_conf
    elif not cmp(conf_item, "rest"):
        return all_conf[0]
    elif not cmp(conf_item, "todo"):
        return all_conf[1]
    else:
        log("该配置项（%s）还未定义." % conf_item, "warn")
        return None


def show_notify(title, msg, icon):
    #name = get_random_str(8)
    pynotify.init("Kreminder")
    knotify = pynotify.Notification(title, msg, icon)
    knotify.set_timeout(15000)
    knotify.set_urgency("normal")
    knotify.show()
    del knotify

def startup_notice():
    help_file = getcwd() + "/man/readme.html"
    icon_notify = getcwd() + "/icon/hint_32x32.png"
    title_notify = "启动通知"
    msg_notify = 'Kreminder 已经启动，点击<a href="' + help_file + '">这里</a>可以查看帮助！'
    pynotify.init("Startup-notice")
    knotify = pynotify.Notification(title_notify, msg_notify, icon_notify)
    knotify.set_timeout(8000)
    knotify.set_urgency("normal")
    knotify.show()
    del knotify

# Script starts from here

if __name__ == "__main__":
    # show startup notify
    #startup_notice()
    # log("hello world")
    # import sys
    # sys.exit()
    app = QApplication(sys.argv)
    ti = TrayIcon()
    ti.show()
    ti.showMessage(u"启动通知",u"Kreminder 已经启动",)



    jobstores = {
        'default': MemoryJobStore()
        #'sqlite': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    }
    executors = {
        'default': ThreadPoolExecutor(10),
        'processpool': ProcessPoolExecutor(5)
    }

    job_defaults = {
        'coalesce': False,
        'max_instances': 4
    }



    # scheduler of Reminding rest
    rest_config = get_conf("rest")

    if rest_config:
        try:
            rest_notify_icon = getcwd() + "/icon/clock_32x32.png"
            rest_remind_scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
            # rest_remind_scheduler.add_job(show_notify, 'interval', \
            #                                             minutes = rest_config["interval"], \
            #                                             args = ["休息提醒", rest_config["message"], rest_notify_icon], \
            #                                             id = "remind_rest")
            rest_remind_scheduler.add_job(ti.showMessage, 'interval', minutes = rest_config["interval"], args = [u"休息提醒", rest_config["message"]], id = "remind_rest")
            rest_remind_scheduler.start()
        except Exception, e:
            log(e, "error")
    else:
        log("未获取到 rest 的相关配置.", "error")


    # scheduler of Reminding todo

    todo_config = get_conf("todo")

    if todo_config:
        todo_notify_icon = getcwd() + "/icon/clock_32x32.png"
        try:
            todo_remind_scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
            for todo_date, todo_msg in todo_config.items():
                if match("Everyday [\d]{2}:[\d]{2}:[\d]{2}", todo_date.strip()):
                    todo_time = (todo_date.split()[1]).split(":")
                    todo_remind_scheduler.add_job(show_notify, 'cron', \
                                                                day = "*", \
                                                                hour = todo_time[0], \
                                                                minute = todo_time[1], \
                                                                second = todo_time[2],  \
                                                                args = ["待办事项", todo_msg, todo_notify_icon], \
                                                                id = todo_date)
                elif match("[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}", todo_date.strip()):
                    if todo_date > strftime("%Y-%m-%d %X", localtime()):
                        todo_remind_scheduler.add_job(show_notify, "date", \
                                                                    run_date = todo_date, \
                                                                    args = ["待办事项", todo_msg, todo_notify_icon], \
                                                                    id = todo_date)
                    else:
                        log("设置的日期已经过期", "warn")
                else:
                    log("Todo 配置项的日期格式不正确： " + todo_date, "error")
            todo_remind_scheduler.start()
        except Exception, e:
            log(e, "error")
    else:
        log("未获取到 todo 的相关配置.", "error")

    # main process
    try:
        while True:
            #sleep(2)
            sys.exit(app.exec_())
    except Exception, e:
        log(e, "error")
        rest_remind_scheduler.shutdown()
        todo_remind_scheduler.shutdown()
