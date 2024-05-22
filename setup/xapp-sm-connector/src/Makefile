CXX:= g++ --std=c++14 -O2 -L/usr/local/lib
CC:= gcc -O2 -L/usr/local/lib

SRC:=.
HWSRC:=./
UTILSRC=./xapp-utils
MSGSRC:=./xapp-mgmt

ASNSRC:=../asn1c_defs
E2APSRC:=./xapp-asn/e2ap
E2SMSRC:=./xapp-asn/e2sm

# modified
TINYXMLSRC:=./xapp-tinyxml2
RICCONTROLSRC:=./xapp_ric_control
NS3DECODESRC:=./ns3_decode
# end modification

####### Logging library and flags
CLOGFLAGS:= `pkg-config mdclog --cflags`
LOG_LIBS:= `pkg-config mdclog --libs`
CURL_LIBS:= `pkg-config libcurl --libs`
RNIB_LIBS:= -pthread /usr/local/include/rnib/rnibreader.a
######## Keep include dirs separate so we have transparency


BASEFLAGS=  -Wall -std=c++14 $(CLOGFLAGS) 
C_BASEFLAGS= -Wall $(CLOGFLAGS) -DASN_DISABLE_OER_SUPPORT

XAPPFLAGS=-I./
HWFLAGS=-I./
UTILFLAGS=-I$(UTILSRC)
MSGFLAGS=-I$(MSGSRC) 

# modified
NS3DECODEFLAGS=-I$(NS3DECODESRC) -I/usr/include
# NS3DECODELIBS=-L/usr/lib/x86_64-linux-gnu -lprotobuf
NS3DECODELIBS:= `pkg-config --cflags --libs protobuf`
TINYXMLFLAGS=-I$(TINYXMLSRC)
CONTROLMESSAGEFLAGS=-I$(RICCONTROLSRC)
# end modification
ASNFLAGS=-I$(ASNSRC) -DASN_DISABLE_OER_SUPPORT
E2APFLAGS=-I$(E2APSRC)
E2SMFLAGS=-I$(E2SMSRC)

########libs

LIBS= -lsdl -lrmr_si  -lpthread -lm $(LOG_LIBS) $(CURL_LIBS) $(RNIB_LIBS) $(NS3DECODELIBS)
COV_FLAGS= -fprofile-arcs -ftest-coverage

#######
HWXAPP_SRC= hw_xapp_main.cc
XAPP_SRC= xapp.cc
UTIL_SRC= $(wildcard $(UTILSRC)/*.cc)
MSG_SRC= $(wildcard $(MSGSRC)/*.cc)

E2AP_SRC= $(wildcard $(E2APSRC)/*.cc)
E2SM_SRC= $(wildcard $(E2SMSRC)/*.cc)
ASN1C_SRC= $(wildcard $(ASNSRC)/*.c)

# modified
NS3DECODE_SRC= $(wildcard $(NS3DECODESRC)/*.cc)
TINYXML_SRC=$(wildcard $(TINYXMLSRC)/*.cpp)
CONTROL_MESSAGE_SRC=$(wildcard $(RICCONTROLSRC)/*.cc)
# end modification

##############Objects
UTIL_OBJ=${UTIL_SRC:.cc=.o}
XAPP_OBJ=${XAPP_SRC:.cc=.o}
HWXAPP_OBJ=${HWXAPP_SRC:.cc=.o} 
MSG_OBJ=${MSG_SRC:.cc=.o}

# modified
TINYXML_OBJ=${TINYXML_SRC:.cpp=.o}
NS3DECODE_OBJ=${NS3DECODE_SRC:.cc=.o}
CONTROL_MESSAGE_OBJ = ${CONTROL_MESSAGE_SRC:.cc=.o}
# end modification

E2AP_OBJ = $(E2AP_SRC:.cc=.o)
E2SM_OBJ = $(E2SM_SRC:.cc=.o)

ASN1C_MODULES = $(ASN1C_SRC:.c=.o)
$(ASN1C_MODULES): export CFLAGS = $(C_BASEFLAGS) $(ASNFLAGS)

$(UTIL_OBJ):export CPPFLAGS=$(BASEFLAGS) $(UTILFLAGS) $(E2APFLAGS) $(E2SMFLAGS) $(ASNFLAGS) $(MSGFLAGS) $(TINYXMLFLAGS)
$(MSG_OBJ):export CPPFLAGS=$(BASEFLAGS) $(MSGFLAGS) $(ASNFLAGS) $(E2APFLAGS) $(E2SMFLAGS) $(TINYXMLFLAGS)

$(E2AP_OBJ): export CPPFLAGS = $(BASEFLAGS) $(ASNFLAGS) $(E2APFLAGS)
$(E2SM_OBJ): export CPPFLAGS = $(BASEFLAGS) $(ASNFLAGS) $(E2SMFLAGS)
$(XAPP_OBJ): export CPPFLAGS = $(BASEFLAGS) $(XAPPFLAGS) $(UTILFLAGS) $(MSGFLAGS) $(E2APFLAGS) $(E2SMFLAGS) $(ASNFLAGS)  $(TINYXMLFLAGS)

$(HWXAPP_OBJ):export CPPFLAGS=$(BASEFLAGS) $(HWFLAGS) $(XAPPFLAGS) $(UTILFLAGS) $(MSGFLAGS) $(E2APFLAGS) $(E2SMFLAGS) $(ASNFLAGS)  $(TINYXMLFLAGS)

# modified
$(TINYXML_OBJ):export CPPFLAGS= $(BASEFLAGS) $(TINYXMLFLAGS)
$(NS3DECODE_OBJ):export CPPFLAGS= $(BASEFLAGS) $(NS3DECODEFLAGS) $(NS3DECODELIBS)
$(CONTROL_MESSAGE_OBJ):export CPPFLAGS= $(C_BASEFLAGS) $(BASEFLAGS) $(HWFLAGS) $(XAPPFLAGS) $(UTILFLAGS) $(MSGFLAGS) $(E2APFLAGS) $(E2SMFLAGS) $(ASNFLAGS) $(CONTROLMESSAGEFLAGS)
# end modification

#  $(CONTROL_MESSAGE_OBJ)
OBJ=  $(HWXAPP_OBJ) $(UTIL_OBJ) $(MSG_OBJ) $(ASN1C_MODULES) $(TINYXML_OBJ) $(E2AP_OBJ) $(E2SM_OBJ) $(XAPP_OBJ)  $(NS3DECODE_OBJ)

print-%  : ; @echo $* = $($*)

hw_xapp_main: $(OBJ)
	$(CXX) $(NS3DECODELIBS) -o $@  $(OBJ) $(LIBS) $(RNIBFLAGS) $(CPPFLAGS) $(CLOGFLAGS) agent_connector.cc

install: hw_xapp_main
	install  -D hw_xapp_main  /usr/local/bin/hw_xapp_main

# $(RICCONTROLSRC)/*.o test_msg_creation
clean:
	-rm *.o $(NS3DECODE_OBJ)/*.o $(ASNSRC)/*.o $(E2APSRC)/*.o $(UTILSRC)/*.o $(E2SMSRC)/*.o  $(MSGSRC)/*.o $(SRC)/*.o hw_xapp_main 
