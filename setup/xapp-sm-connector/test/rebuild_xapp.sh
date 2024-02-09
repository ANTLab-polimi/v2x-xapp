#!/bin/bash

export DEBUG=0
export CONNECTOR_DIR=/home/xapp-sm-connector

# these are replaced through the dockerfile
GNB_ID=ns-o-ran
XAPP_ID=24

# get build clean from cli arguments
if [ $# -ne 0 ]; then
    BUILD_CLEAN=1
fi

# build
if [ ${BUILD_CLEAN} ]; then
    cd ${CONNECTOR_DIR}/test && make clean && make -j ${nproc} && make install && ldconfig
else
    cd ${CONNECTOR_DIR}/test && make -j ${nproc} && make install && ldconfig
fi

