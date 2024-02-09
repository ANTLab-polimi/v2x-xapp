#include "tinyxml2.h"
// #include "stdio.h"
#include <ostream>
#include <fstream>
#include <iostream>
#include <stdlib.h>
#include "control_message_encoder_decoder.h"
#include "nr-sl-sci-f1a-header.h"
#include "nr-sl-mac-pdu-tag.h"

// using namespace tinyxml2;

int main_new(int argc, char* argv[]){
    std::cout << "Start" << std::endl; 
    printf("Hello again, world\n");
    const char* msg = "<E2SM-KPM-IndicationMessage>"
    "    <indicationMessage-Format1>"
    "        <pm-Containers>"
    "            <PM-Containers-Item>"
    "                <performanceContainer>"
    "                    <oCU-CP>"
    "                        <cu-CP-Resource-Status>"
    "                            <numberOfActive-UEs>4</numberOfActive-UEs>"
    "                        </cu-CP-Resource-Status>"
    "                    </oCU-CP>"
    "                </performanceContainer>"
    "            </PM-Containers-Item>"
    "        </pm-Containers>"
    "        <cellObjectID>NRCellCU</cellObjectID>"
    "        <list-of-matched-UEs>"
    "            <PerUE-PM-Item>"
    "                <ueId>30 30 30 30 31</ueId>"
    "                <list-of-PM-Information>"
    "                    <PM-Info-Item>"
    "                        <pmType>"
    "                            <measName>SciHeaderBuffer</measName>"
    "                        </pmType>"
    "                        <pmVal>"
    "                            <valueOctetString>"
    "                                00 00 00 00 0E 00 00 00 01 01 FF 00 0C 00 0A 07 "
    "                                01 03 0C 01 0B 0A 00 00 00 00 00 00 00 00 00 00"
    "                            </valueOctetString>"
    "                        </pmVal>"
    "                    </PM-Info-Item>"
    "                    <PM-Info-Item>"
    "                        <pmType>"
    "                            <measName>SciTagBuffer</measName>"
    "                        </pmType>"
    "                        <pmVal>"
    "                            <valueOctetString>"
    "                                00 00 00 00 14 00 00 00 01 00 00 01 00 01 01 00 "
    "                                01 00 01 01 01 00 00 00 01 00 00 00 00 00 00 00 "
    "                                00 00 00 00"
    "                            </valueOctetString>"
    "                        </pmVal>"
    "                    </PM-Info-Item>"
    "                </list-of-PM-Information>"
    "            </PerUE-PM-Item>"
    "            <PerUE-PM-Item>"
    "                <ueId>30 30 30 30 30</ueId>"
    "                <list-of-PM-Information>"
    "                    <PM-Info-Item>"
    "                        <pmType>"
    "                            <measName>SciHeaderBuffer</measName>"
    "                        </pmType>"
    "                        <pmVal>"
    "                            <valueOctetString>"
    "                                00 00 00 00 0E 00 00 00 01 01 FF 00 0C 00 0A 07 "
    "                                01 03 0C 01 0B 0A 00 00 00 00 00 00 00 00 00 00"
    "                            </valueOctetString>"
    "                        </pmVal>"
    "                    </PM-Info-Item>"
    "                    <PM-Info-Item>"
    "                        <pmType>"
    "                            <measName>SciTagBuffer</measName>"
    "                        </pmType>"
    "                        <pmVal>"
    "                            <valueOctetString>"
    "                                00 00 00 00 14 00 00 00 01 00 00 01 00 01 01 00 "
    "                                01 00 01 01 01 00 00 00 01 00 00 00 00 00 00 00 "
    "                                00 00 00 00"
    "                            </valueOctetString>"
    "                        </pmVal>"
    "                    </PM-Info-Item>"
    "                </list-of-PM-Information>"
    "            </PerUE-PM-Item>"
    "        </list-of-matched-UEs>"
    "    </indicationMessage-Format1>"
    "</E2SM-KPM-IndicationMessage>";
    const char* _header = 
    "<E2SM-KPM-IndicationHeader>"
    "    <indicationHeader-Format1>"
    "        <collectionStartTime>98 00 03 00 00 08 4E 52</collectionStartTime>"
    "        <id-GlobalE2node-ID>"
    "            <ng-eNB>"
    "                <global-ng-eNB-ID>"
    "                    <plmn-id>65 6C 6C</plmn-id>"
    "                    <enb-id>"
    "                        <enb-ID-longmacro>31 00 00 00</enb-ID-longmacro>"
    "                    </enb-id>"
    "                </global-ng-eNB-ID>"
    "            </ng-eNB>"
    "        </id-GlobalE2node-ID>"
    "    </indicationHeader-Format1>"
    "</E2SM-KPM-IndicationHeader>";
    tinyxml2::XMLDocument pduDoc;
	tinyxml2::XMLDocument headerDoc;
    tinyxml2::XMLDocument msgDoc;
    tinyxml2::XMLElement* mainElement = pduDoc.NewElement("message");
    // mainElement->SetText("message");
    tinyxml2::XMLNode* headerNode = pduDoc.InsertFirstChild(mainElement->DeepClone(&pduDoc));
    headerDoc.Parse(_header);
    msgDoc.Parse(msg);
    tinyxml2::XMLNode* rootHeader = headerDoc.FirstChild()->DeepClone(&pduDoc); 
    pduDoc.FirstChild()->InsertEndChild(rootHeader);
    tinyxml2::XMLNode* rootMessage = msgDoc.FirstChild()->DeepClone(&pduDoc);
    pduDoc.FirstChild()->InsertEndChild(rootMessage);

    // tinyxml2::XMLPrinter* headerPrinter = new tinyxml2::XMLPrinter();
    // headerDoc.Print(headerPrinter);
    // uint8_t* headerBuff = (uint8_t *) calloc(1, headerPrinter->CStrSize());
    // memcpy(headerBuff, headerPrinter->CStr(), headerPrinter->CStrSize());
    // std::string _headerDocString = std::string((char*)headerBuff);
    // std::cout << "Header " << _headerDocString << std::endl;
    

    // tinyxml2::XMLPrinter* messagePrinter = new tinyxml2::XMLPrinter();
    // msgDoc.Print(messagePrinter);
    // uint8_t* msgBuff = (uint8_t *) calloc(1, messagePrinter->CStrSize());
    // memcpy(msgBuff, messagePrinter->CStr(), messagePrinter->CStrSize());
    // std::string _msgDocString = std::string((char*)msgBuff);
    // std::cout << "Message " << _msgDocString << std::endl;


    // v2x_sci_header_buffer_t * headerBuffer = decode_v2x_sci_header(msgBuff, messagePrinter->CStrSize());
    
    // entire doc
    // tinyxml2::XMLPrinter* docPrinter = new tinyxml2::XMLPrinter();
    // pduDoc.Print(docPrinter);
    // uint8_t* pduBuff = (uint8_t *) calloc(1, docPrinter->CStrSize());
    // memcpy(pduBuff, docPrinter->CStr(), docPrinter->CStrSize());
    // std::string _pduDocString = std::string((char*)pduBuff);
    // std::cout << "Pdu " << _pduDocString << std::endl;
    
    // e2ap_stcp_buffer_t * e2apBufferPointer = decode_e2ap_to_xml(pduBuff, docPrinter->CStrSize());

    // testing the sci header
    const char* _sciHeader = "00 00 00 00 0E 00 00 00 01 01 FF 00 0C 00 0A 07 "
    "                                01 03 0C 01 0B 0A 00 00 00 00 00 00 00 00 00 00";
    const char* _sciTag = " 00 00 00 00 14 00 00 00 01 00 00 01 00 01 01 00 "
    "                                01 00 01 01 01 00 00 00 01 00 00 00 00 00 00 00 "
    "                                00 00 00 00";

    // remove spaces by converting first to string 
    std::string _sciHeaderString = std::string(_sciHeader);
    std::cout << "Passing these arguments to the function " << _sciHeaderString << " length " << _sciHeaderString.length() << std::endl;
    v2x_sci_header_buffer_t * sciHeaderBufferPointer = decode_v2x_sci_header((uint8_t*)_sciHeader, _sciHeaderString.length());
    std::cout << " tot sub channels " <<  sciHeaderBufferPointer->m_totalSubChannels << std::endl;

    std::string _sciTagString = std::string(_sciTag);
    std::cout << "Passing these arguments to the function " << _sciTagString << " length " << _sciTagString.length() << std::endl;
    v2x_sci_tag_buffer_t * sciTagBufferPointer = decode_v2x_sci_tag((uint8_t*)_sciTag, _sciTagString.length());
    std::cout << " numerology " <<  sciTagBufferPointer->m_numerology << std::endl;

    std::cout << "All good" << std::endl; 
    delete sciHeaderBufferPointer;
    return 0;
}

