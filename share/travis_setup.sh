#!/bin/bash
set -evx

mkdir ~/.lusocore

# safety check
if [ ! -f ~/.lusocore/.luso.conf ]; then
  cp share/luso.conf.example ~/.lusocore/luso.conf
fi
