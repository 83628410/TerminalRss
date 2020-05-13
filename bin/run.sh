#!/bin/bash
PRG="$0"

while [ -h "$PRG" ]; do
  ls=`ls -ld "$PRG"`
  link=`expr "$ls" : '.*-> \(.*\)$'`
  if expr "$link" : '/.*' > /dev/null; then
    PRG="$link"
  else
    PRG=`dirname "$PRG"`/"$link"
  fi
done

PRGDIR=`dirname "$PRG"`
TER_HOME=`cd "$PRGDIR/.." >/dev/null; pwd`
#运行命令
$TER_HOME/venv/bin/python $TER_HOME/terminal.py
