#!/bin/bash

source ~/.bash_profile

base_dir=$(cd "$(dirname "$0")"; pwd)

# start token-server
cd $base_dir

cur_dir=$(pwd)
if [ ! -d log ]; then
   mkdir log
fi


python manage.py runserver 0.0.0.0:13060
#nohup python $cur_dir/name_parser.py >log/name_predict.log 2>&1 &

if [ $? != 0 ]; then
    echo "Error happend when start cache server"
    exit
fi

echo "Done"
