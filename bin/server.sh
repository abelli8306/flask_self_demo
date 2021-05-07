#!/bin/bash

export WORKDIR=$( cd ` dirname $0 ` && pwd )

cd "$WORKDIR/../" || exit 1
# source ./init.sh

# Global definitions
PRO_BIN="flask_app.py"
PRO_BINLOG="log/info.log"
PRO_INTERVAL_TIME=900
#PRO_USER="root"

RETVAL=0

# [ ! -x "$PRO_BIN" ] && echo "$PRO_BIN: No execute permission" && exit 5 

__getpid_for_commandname() {
    local base=${1##*/}
    local i options= pid= tmp_pid=

    shift;
    options="$*"

    tmp_pid=$( ps -o pid,ppid,args -C |grep -i "$base" | awk '
                $1 ~ /'"$PPID"'|'"$$"'/{next;} 
                /awk|grep/{next;} 
                /'"$options"'/{print $1}')

    for i in $tmp_pid ; do
        [ -z "${i//[0-9]/}" ] && pid="$pid $i"
    done

    if [ -n "$pid" ]; then
        echo $pid
        return 0
    fi

    return 3 # "Program is not running"
}

start() {
	nohup python $PRO_BIN 2>&1 &
    sleep 1
    pid="$(__getpid_for_commandname "$PRO_BIN")"
    echo "Starting $PRO_BIN successed , Pid is : $pid "
    return 0
}

stop() {
    pid="$(__getpid_for_commandname "$PRO_BIN")"

    if [ -n "$pid" ]; then
        kill -9 $pid
        echo "Shutting down $PRO_BIN successed, Pid is : $pid"
        return 0
    fi

    echo "$PRO_BIN not run "
    
    return 3
}

# See how we were called.
case "$1" in
  "start")
        start
        ;;
  "stop")
        stop
        ;;
  "restart")
        stop
        start
        ;;
  *)
	echo "Usage: $0 {start|stop|restart}" 
	exit 1
esac

exit 0
