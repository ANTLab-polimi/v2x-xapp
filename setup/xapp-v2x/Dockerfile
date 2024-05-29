##-----------------------------------
# BS Connector
#------------------------------------
ARG SCHEMA_PATH=schemas
ARG XAPP_DIR=xapp-v2x
# ARG IPSO_DIR=ipso-xapp
ARG CONNECTOR_DIR=xapp-sm-connector
ARG STAGE_DIR=/home/${CONNECTOR_DIR}
ARG DBAAS_SERVICE_HOST=10.0.2.12
ARG DBAAS_SERVICE_PORT="6379"

#==================================================================================
FROM xapp-base:latest as ricbuild
# Need to download from rayproject to have ray installed
# FROM rayproject/ray:latest as ricbuild


# to override repo base, pass in repo argument when running docker build:
# docker build --build-arg REPOBASE=http://abc.def.org . ....
ARG REPOBASE=https://gerrit.oran-osc.org/r
ARG SCHEMA_FILE
ARG SCHEMA_PATH
ARG XAPP_DIR
# ARG IPSO_DIR
ARG CONNECTOR_DIR
ARG STAGE_DIR

ARG MDC_VER=0.0.4-1
ARG RMR_VER=4.0.5
ARG RNIB_VER=1.0.0

# RUN apt-get update && apt-get install -y protobuf-compiler libprotobuf-dev

ENV RMR_RTG_SVC="9999" \
  RMR_SEED_RT="/home/${CONNECTOR_DIR}/init/routes.txt" \
  LD_LIBRARY_PATH="/usr/local/lib:/usr/local/libexec" \
  VERBOSE=0 \
  CONFIG_FILE=/opt/ric/config/config-file.json \
  DBAAS_SERVICE_HOST=${DBAAS_SERVICE_HOST} \
  DBAAS_SERVICE_PORT=${DBAAS_SERVICE_PORT} \
  # Added to avoid stopping at time zone
  TZ=Europe/Rome \
  DEBIAN_FRONTEND=noninteractive

RUN  apt update && apt install -y g++ unzip zip && pip install protobuf==3.20.*


# WORKDIR /home

# RUN wget https://github.com/protocolbuffers/protobuf/archive/refs/tags/v27.0.tar.gz \
#   && wget https://github.com/bazelbuild/bazel/releases/download/7.1.2/bazel-7.1.2-installer-linux-x86_64.sh \
#   && chmod +x bazel-7.1.2-installer-linux-x86_64.sh \
#   && ./bazel-7.1.2-installer-linux-x86_64.sh \
#   && rm bazel-7.1.2-installer-linux-x86_64.sh \
#   && tar -xvzf v27.0.tar.gz \
#   && rm v27.0.tar.gz \
#   && cd protobuf-27.0 \
#   && bazel build :protoc :protobuf

WORKDIR /home

# COPY ${CONNECTOR_DIR}/init ${STAGE_DIR}/init
COPY ${XAPP_DIR}/ /home/${XAPP_DIR}/
# COPY ${XAPP_DIR} /home
# COPY ${CONNECTOR_DIR}/src/xapp.cc ${STAGE_DIR}/src 
# COPY ${CONNECTOR_DIR}/src/ns3_decode/* ${STAGE_DIR}/src
# COPY ${XAPP_DIR}/*.py /home/${XAPP_DIR}
# COPY ${IPSO_DIR} /home/${IPSO_DIR}


# RUN rm -R ${CONNECTOR_DIR}
# COPY ${CONNECTOR_DIR}/ ${STAGE_DIR}/
# WORKDIR ${STAGE_DIR}
# RUN mkdir -p build
# RUN chmod +x ric_message_sl.sh && ./ric_message_sl.sh

# RUN cd src/ns3_decode \
#     && protoc --cpp_out=. sl-sci-msg.proto \
#     && cd ../..

##-----------------------------------
# Now install the program
#------------------------------------
# build connector
WORKDIR ${STAGE_DIR}

RUN export CPATH=$CPATH:/usr/local/include \
  && cd src \
  && make clean \
  && make -j ${nproc} \
  && make install \
  && ldconfig \
  && sysctl -w net.ipv6.conf.lo.disable_ipv6=1 \
###-----------------------------------
## DRL Agent
##------------------------------------
## install packages and pip requirements
#  && pip3 --no-cache-dir install -U pip \
#  && pip3 --no-cache-dir install -r /home/${XAPP_DIR}/requirements.txt \
  && apt-get autoremove -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*







