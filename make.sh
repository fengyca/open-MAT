#!/bin/bash
### END INIT INFO
case $1 in 
   start)  # 服务启动需要做的步骤
           echo "----正在启动-----"
           kill -9 $(ps -ef|grep adb |awk '$0 !~/grep/ {print $2}' |tr -s '\n' ' ') > /dev/null
           rm -rf static > /dev/null
           python manage.py collectstatic > /dev/null
           sleep 1s
           uwsgi -x django_uwsgi.xml
           sleep 1s
           sudo nginx
           echo "----启动成功-----"
           ;;
    stop)  # 服务停止需要做的步骤
           echo "----正在停止-----"
           rm -rf static > /dev/null
           kill -9 $(ps -ef|grep node |awk '$0 !~/grep/ {print $2}' |tr -s '\n' ' ')
           kill -9 $(ps -ef|grep adb |awk '$0 !~/grep/ {print $2}' |tr -s '\n' ' ') > /dev/null
           sleep 1s
           kill -9 $(ps -ef|grep uwsgi |awk '$0 !~/grep/ {print $2}' |tr -s '\n' ' ')
           uwsgi --stop uwsgi.pid
           sleep 1s
           sudo nginx -s stop
           echo "----停止成功-----"
           ;;
   restart) # 重启服务需要做的步骤
           echo "----正在重启-----"
           kill -9 $(ps -ef|grep node |awk '$0 !~/grep/ {print $2}' |tr -s '\n' ' ')
           kill -9 $(ps -ef|grep adb |awk '$0 !~/grep/ {print $2}' |tr -s '\n' ' ') > /dev/null
           sleep 1s
           uwsgi --stop uwsgi.pid
           sleep 1s
           sudo nginx -s stop
           kill -9 $(ps -ef|grep adb |awk '$0 !~/grep/ {print $2}' |tr -s '\n' ' ') > /dev/null
           uwsgi -x django_uwsgi.xml
           sleep 1s
           sudo nginx
           echo "----重启成功-----"
            ;;
esac