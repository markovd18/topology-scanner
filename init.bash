#!/bin/bash

apt update && \
  apt upgrade && \
  apt install git && \
  apt install pip && \
  pip install pysnmp && \
  pip unsinstall pyasn1 && \
  pip install pyasn1==0.4.8
