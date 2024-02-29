CXX:= g++ --std=c++14 -O2 -L/usr/local/lib
CC:= gcc -O2 -L/usr/local/lib

TEST:=./
SRC:=../src
UTILSRC=../src/xapp-utils
MGMTSRC:=../src/xapp-mgmt

ASNSRC:=../asn1c_defs
E2APSRC:=../src/xapp-asn/e2ap
E2SMSRC:=../src/xapp-asn/e2sm

# modified
TINYXMLSRC:=../src/xapp-tinyxml2
RICCONTROLSRC:=../src/xapp_ric_control
NS3DECODESRC:=../src/ns3_decode
# end modification

####### Logging library and flags
CLOGFLAGS:= `pkg-config mdclog --cflags`
LOG_LIBS:= `pkg-config mdclog --libs`
CURL_LIBS:= `pkg-config libcurl --libs`
RNIB_LIBS:= -pthread /usr/local/include/rnib/rnibreader.a
GTEST_LIBS:= -lgtest -lgtest_main
######## Keep include dirs separate so we have transparency


BASEFLAGS=  -Wall -std=c++14 $(CLOGFLAGS) 
C_BASEFLAGS= -Wall $(CLOGFLAGS) -DASN_DISABLE_OER_SUPPORT

XAPPFLAGS= -I$(SRC)
UTILFLAGS= -I$(UTILSRC)
MGMTFLAGS= -I$(MGMTSRC)

# modified
NS3DECODEFLAGS=-I$(NS3DECODESRC)
TINYXMLFLAGS = -I$(TINYXMLSRC)
CONTROLMESSAGEFLAGS = -I$(RICCONTROLSRC)
# end modification
ASNFLAGS = -I$(ASNSRC) -DASN_DISABLE_OER_SUPPORT
E2APFLAGS = -I$(E2APSRC)
E2SMFLAGS = -I$(E2SMSRC)

########libs

LIBS= -lsdl -lrmr_si -lpthread -lm $(LOG_LIBS) $(CURL_LIBS) $(RNIB_LIBS) # $(GTEST_LIBS)
COV_FLAGS= -fprofile-arcs -ftest-coverage

#######
TEST_SRC= v2x_scheduling_test.cc hw_unit_tests.cc decoding_test.cc decode_e2ap_pdu_test.cc
XAPP_SRC= ../src/xapp.cc ../src/agent_connector.cc
TEST_HDR=$(wildcard $(TEST)/*.h)
UTIL_SRC= $(wildcard $(UTILSRC)/*.cc)
MGMT_SRC= $(wildcard $(MGMTSRC)/*.cc)

E2AP_SRC= $(wildcard $(E2APSRC)/*.cc)
E2SM_SRC= $(wildcard $(E2SMSRC)/*.cc)
ASN1C_SRC= $(wildcard $(ASNSRC)/*.c)

# modified
NS3DECODE_SRC= $(wildcard $(NS3DECODESRC)/*.cc)
TINYXML_SRC=$(wildcard $(TINYXMLSRC)/*.cpp)
CONTROL_MESSAGE_SRC=$(wildcard $(RICCONTROLSRC)/*.cc)
CONTROL_MESSAGE_SRC_C_FILES=$(wildcard $(RICCONTROLSRC)/*.c)
# end modification

##############Objects
UTIL_OBJ=${UTIL_SRC:.cc=.o}
MGMT_OBJ=${MGMT_SRC:.cc=.o}
XAPP_OBJ=${XAPP_SRC:.cc=.o}
TEST_OBJ=${TEST_SRC:.cc=.o} 

# modified
TINYXML_OBJ=${TINYXML_SRC:.cpp=.o}
NS3DECODE_OBJ=${NS3DECODE_SRC:.cc=.o}
CONTROL_MESSAGE_OBJ = ${CONTROL_MESSAGE_SRC:.cc=.o} 
CONTROL_MESSAGE_C_FILES_OBJ = ${CONTROL_MESSAGE_SRC_C_FILES:.c=.o}
# end modification

E2AP_OBJ = $(E2AP_SRC:.cc=.o)
E2SM_OBJ = $(E2SM_SRC:.cc=.o)

ASN1C_MODULES = $(ASN1C_SRC:.c=.o)
$(ASN1C_MODULES): export CFLAGS = $(C_BASEFLAGS) $(ASNFLAGS)

$(UTIL_OBJ):export CPPFLAGS=$(BASEFLAGS) $(UTILFLAGS) $(MGMTFLAGS) $(TINYXMLFLAGS)
$(MGMT_OBJ):export CPPFLAGS=$(BASEFLAGS) $(MGMTFLAGS) $(ASNFLAGS) $(E2APFLAGS) $(E2SMFLAGS) $(TINYXMLFLAGS)

$(E2AP_OBJ): export CPPFLAGS = $(BASEFLAGS) $(ASNFLAGS) $(E2APFLAGS)
$(E2SM_OBJ): export CPPFLAGS = $(BASEFLAGS) $(ASNFLAGS) $(E2SMFLAGS)
$(XAPP_OBJ): export CPPFLAGS = $(BASEFLAGS) $(XAPPFLAGS) $(UTILFLAGS) $(MGMTFLAGS) $(E2APFLAGS) $(E2SMFLAGS) $(ASNFLAGS) $(TINYXMLFLAGS)

$(TEST_OBJ):export CPPFLAGS=$(BASEFLAGS) $(ASNFLAGS) $(TINYXMLFLAGS) $(NS3DECODEFLAGS) $(CONTROLMESSAGEFLAGS)
# $(TEST_OBJ) = $(TEST_HDR) $(TEST_OBJ) 

# modified
$(TINYXML_OBJ):export CPPFLAGS= $(BASEFLAGS) $(TINYXMLFLAGS)
$(NS3DECODE_OBJ):export CPPFLAGS= $(BASEFLAGS) $(NS3DECODEFLAGS)
$(CONTROL_MESSAGE_OBJ):export CPPFLAGS= $(BASEFLAGS) $(C_BASEFLAGS) $(CONTROLMESSAGEFLAGS) $(ASNFLAGS) $(TINYXMLFLAGS) $(NS3DECODEFLAGS)
$(CONTROL_MESSAGE_C_FILES_OBJ):export CFLAGS= $(BASEFLAGS) $(C_BASEFLAGS) $(CONTROLMESSAGEFLAGS) $(ASNFLAGS) $(TINYXMLFLAGS) $(NS3DECODEFLAGS)
# end modification


OBJ= $(TEST_OBJ) $(UTIL_OBJ) $(MGMT_OBJ) $(ASN1C_MODULES) $(E2AP_OBJ) $(E2SM_OBJ) $(XAPP_OBJ) $(TINYXML_OBJ) $(NS3DECODE_OBJ) $(CONTROL_MESSAGE_OBJ) $(CONTROL_MESSAGE_C_FILES_OBJ)

print-%  : ; @echo $* = $($*)

hw_unit_tests: $(OBJ)
	$(CXX) -o $@  $(OBJ) $(LIBS) $(RNIBFLAGS) $(CPPFLAGS) $(CLOGFLAGS) $(TINYXMLFLAGS) $(ASNFLAGS) $(NS3DECODEFLAGS) $(CONTROLMESSAGEFLAGS)

decoding_test: $(OBJ)
	$(CXX) -o $@ $(OBJ) $(LIBS) $(RNIBFLAGS) $(CPPFLAGS) $(CLOGFLAGS) $(TINYXMLFLAGS) $(ASNFLAGS) $(NS3DECODEFLAGS) $(CONTROLMESSAGEFLAGS)

v2x_scheduling_test: $(OBJ)
	$(CXX) -o $@ $(OBJ) $(LIBS) $(RNIBFLAGS) $(CPPFLAGS) $(CLOGFLAGS) $(TINYXMLFLAGS) $(ASNFLAGS) $(NS3DECODEFLAGS) $(CONTROLMESSAGEFLAGS)

decode_e2ap_pdu_test: $(OBJ)
	$(CXX) -o $@ $(OBJ) $(LIBS) $(RNIBFLAGS) $(CPPFLAGS) $(CLOGFLAGS) $(TINYXMLFLAGS) $(ASNFLAGS) $(NS3DECODEFLAGS) $(CONTROLMESSAGEFLAGS)

# install: hw_unit_tests decoding_test v2x_scheduling_test
# 	install  -D hw_unit_tests  /usr/local/bin/hw_unit_tests
# 	install  -D decoding_test  /usr/local/bin/decoding_test
# 	install  -D v2x_scheduling_test  /usr/local/bin/v2x_scheduling_test

# install: decoding_test
# 	install decoding_test  /usr/local/bin/decoding_test

# install: v2x_scheduling_test
# 	install -D v2x_scheduling_test  /usr/local/bin/v2x_scheduling_test

install: decode_e2ap_pdu_test
	install -D decode_e2ap_pdu_test  /usr/local/bin/decode_e2ap_pdu_test

test: decoding_test
	./decoding_test

# Standard GNU target
check: decoding_test
	./decoding_test

check_scheduling: v2x_scheduling_test
	./v2x_scheduling_test

check_e2ap: decode_e2ap_pdu_test
	./decode_e2ap_pdu_test

clean:
	-rm *.o $(E2APSRC)/*.o $(UTILSRC)/*.o $(E2SMSRC)/*.o  $(MGMTSRC)/*.o $(SRC)/*.o \
	$(RICCONTROLSRC)/*.o $(NS3DECODESRC)/*.o $(TINYXMLSRC)/*.o \
	decoding_test hw_unit_tests v2x_scheduling_test decode_e2ap_pdu_test

.PHONY: decoding_test hw_unit_tests v2x_scheduling_test decode_e2ap_pdu_test
