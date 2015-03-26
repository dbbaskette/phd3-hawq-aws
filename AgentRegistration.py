__author__ = 'dbaskette'
import argparse
import socket
import time

import requests
from requests.auth import HTTPBasicAuth


def registrationMonitor(numAgents):
    hostName = socket.getfqdn()
    auth = HTTPBasicAuth('admin', 'admin')
    url = "http://" + hostName + ":8080/api/v1/hosts"
    complete = False
    while not complete:
        registeredCount = 0
        agentInfo = requests.get(url, auth=auth)
        ambariHosts = open("ambari-hosts.json", "w")
        for line in agentInfo:
            if line.contains("host_name"):
                ambariHosts.write(line)
                registeredCount += 1
        if registeredCount == numAgents:
            complete = True
        time.sleep(15)


def cliParse():
    VALID_ACTION = ["monitor"]
    parser = argparse.ArgumentParser(description='Agent Registration')
    subparsers = parser.add_subparsers(help='sub-command help', dest="subparser_name")
    parser_monitor = subparsers.add_parser("monitor", help="Monitor Agent Registration")
    parser_monitor.add_argument("--agents", dest='numAgents', action="store", help="Number of Agents to Register",
                                required=True)

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    print "Agent Registration"
    args = cliParse()
    numAgents = int(args.numAgents) + 1  # Account for Agent on Ambari Server itself
    registrationMonitor(numAgents)
