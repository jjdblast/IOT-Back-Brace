#!/bin/bash
##### Start up data collection jobs ####
/usr/local/kafka/bin/zookeeper-server-start.sh /usr/local/kafka/config/zookeeper.properties > /dev/null 2>&1 &
/usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties > /dev/null 2>&1 &