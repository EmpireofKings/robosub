#!/bin/bash

set -xe

wget --quiet https://download.stereolabs.com/zedsdk/2.3/ubuntu -O /tmp/ZED_SDK.run
chmod +x /tmp/ZED_SDK.run
/tmp/ZED_SDK.run --quiet -- silent

rm -rf /tmp/*
