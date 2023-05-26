#!/bin/bash

apt update && \
  apt upgrade && \
  apt install git && \
  apt install pip && \
  pip install pysnmp && \
  pip uninstall pyasn1 && \
  pip install pyasn1==0.4.8 && \
  git clone https://github.com/markovd18/topology-scanner.git
