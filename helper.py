#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018, Dan Sheffner Digital Imaging Software Solutions, INC
# All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

"""
python script to bridge docker commands
"""


import argparse
import datetime
import subprocess
import os

class Helper(object):

    verion = "0.1"

    def __init__(self):

        # number of threads
        self.threads = 4

        # what containers do you want to pull
        self.container_list = [
            'alpine:latest',
            'ubuntu:latest',
            'ubuntu:16.04',
            'postgres:latest',
            'mysql:5.6',
            'jupyter/base-notebook',
            'python:3.6.4-stretch',
            'python:3.7.0a4',
            'golang:alpine',
            'golang:latest',
            'gopherdata/gophernotes-ds',
            'thesheff17/apt-cacher-ng:latest',
            'couchbase/server:enterprise-4.6.3',
            'memcached:latest',
            'redis:latest',
            'amazonlinux:latest',
            'ruby:2.4.0',
            'centos:latest',
            'debian:latest',
            'nginx:latest',
            'httpd:latest',
            'openjdk:latest',
            'haproxy:latest',
            'jenkins:latest',
            'influxdb:latest',
            'grafana/grafana:latest',
            'scylladb/scylla:latest',
            ]

        self.save_location = os.getenv("HOME") + "/ipython/images/"

        if not os.path.isdir(self.save_location):
            os.makedirs(self.save_location)

    def cleanup_docker_containers(self):
        command1 = "docker ps | wc -l"
        output1 = subprocess.check_output(command1, shell=True)
        if int(output1) > 1:
            command2 = "docker stop $(docker ps -a -q)"
            subprocess.run(command2, shell=True)

        command3 = "docker ps -a | wc -l"
        output2 = subprocess.check_output(command3, shell=True)
        if int(output2) > 1:
            command4 = "docker rm -f $(docker ps -a -q)"
            subprocess.run(command4, shell=True)

    def clean_all(self):
        command1 = "docker images | wc -l"
        output1 = subprocess.check_output(command1, shell=True)
        if int(output1) > 1:
            command2 = "docker rmi -f $(docker images -q)"
            subprocess.run(command2, shell=True, check=True)

    def pull_containers(self):
        for each in self.container_list:
            command1 = "docker pull " + each
            subprocess.run(command1, shell=True, check=True)

    def save(self):
        """
        I use bash here with the wait command because I was lazy.  
        Feel free to write this in python.
        """
        f1 = open("docker_save.sh", "w")
        f2 = open("docker_load.sh", "w")
        f1.write("#!/bin/bash\n")
        f2.write("#!/bin/bash\n")
        f1.write("\n")
        f2.write("\n")
        x = 1

        for each in self.container_list:
            format_each1 = each.replace(":", "-")
            format_each2 =  format_each1.replace("/", "-")
            command1 = "docker save " + each + " | gzip > " + self.save_location + format_each2 + ".tgz &\n"
            command2 = "gunzip -c " + self.save_location + format_each2 + ".tgz | docker load &\n"
            f1.write(command1)
            f2.write(command2)

            # determains threads in bash file
            if x % self.threads == 0:
                f1.write("wait\n")
                f2.write("wait\n")

            x += 1

        f1.write('wait\n')
        f2.write('wait\n')
        f1.write('echo "docker_save.sh completed."')
        f2.write('echo "docker_load.sh completed."')
        f1.close()
        f2.close()

        command3 = "chmod +x docker_save.sh docker_load.sh"
        subprocess.run(command3, shell=True, check=True)

        command4 = "./docker_save.sh"
        subprocess.run(command4, shell=True, check=True)

    def load(self):
        command4 = "./docker_load.sh"
        subprocess.run(command4, shell=True, check=True)


if __name__ == "__main__":
    a = datetime.datetime.now().replace(microsecond=0)

    helper = Helper()
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", help="cleans up docker containers running but not images", action="store_true")
    parser.add_argument("--cleanAll", help="cleans up docker containers and images", action="store_true" )
    parser.add_argument("--pull", help="pulls the containers most used by devs.", action="store_true" )
    parser.add_argument("--save", help="save the docker images currently in the list", action="store_true")
    parser.add_argument("--load", help="save the docker images currently in the list", action="store_true")
    parser.add_argument("--doIt", help="clean containers, clean images, loads stored images, docker pull images", action="store_true")
    args = parser.parse_args()

    if args.clean:
        helper.cleanup_docker_containers()

    if args.cleanAll:
        helper.clean_all()

    if args.pull:
        helper.pull_containers()

    if args.save:
        helper.save()

    if args.load:
        helper.load()

    if args.doIt:
        helper.clean_all()
        helper.load()
        helper.pull_containers()

    b = datetime.datetime.now().replace(microsecond=0)
    output = (b - a)
    print ("helper.py completed. took: " + str(output))