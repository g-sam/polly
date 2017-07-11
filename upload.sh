#!/bin/bash

for file in "$@"
do
  webrepl/webrepl_cli.py $file 192.168.1.218:/$file
done
