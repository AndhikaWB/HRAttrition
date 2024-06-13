#!/bin/bash
cd $(dirname "$0")
rm -f *.log

# https://www.metabase.com/start/oss/jar
java -Xmx512M -jar metabase.jar