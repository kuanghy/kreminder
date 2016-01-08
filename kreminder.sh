#!/bin/bash

# Filename: delete.sh  2016.01.07
# Author: huoty <sudohuoty@163.com>
# Script starts from here:

sleep 60s
killall reminder.py
cd $HOME/.kreminder
nohup python kreminder.py
