#!/bin/bash

apt install pip -y && \
  pip install pysnmp && \
  pip uninstall pyasn1 -y && \
  pip install pyasn1==0.4.8
