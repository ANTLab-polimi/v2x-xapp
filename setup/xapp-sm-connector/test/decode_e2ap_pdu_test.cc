#include "tinyxml2.h"
// #include "stdio.h"
#include <ostream>
#include <fstream>
#include <iostream>
#include <stdlib.h>
#include <string>
#include <sstream>
#include <iterator>
#include "control_message_encoder_decoder.h"

char* converHexToByteLocal(std::string hexString) {

    char * bytes = new char[hexString.length()/2];
    std::stringstream converter;

    for(int i = 0; i < hexString.length(); i+=2)
    {
        converter << std::hex << hexString.substr(i,2);
        int byte;
        converter >> byte;
        bytes[i/2] = byte & 0xFF;
        converter.str(std::string());
        converter.clear();
    }
    // char* bytesPointer= bytes;
    // return bytesPointer;
    return bytes;
}  

int main(int argc, char* argv[])
{


    const char* _e2ap_pdu_long = "0005408265000008001d00050000000000000500020000000f000100001b00020001001c0001000019001211000000000000001a906031313100310000001a00821f821d109800010000084e5243656c6c4355000140053030303031070030506f735810000030506f7359100000404672616d65000202a700705375624672616d650001090030536c6f74000100008054696d657374616d7000021a9000b053696e676c655265706f7274340000000001000500000100030000000a00010064400200000a0014000200644004000014001e00020064400400000000000200030000000a00010064400200000a0014000200644004000014001e00020064400400000000000300030000000a00010064400200000a0014000200644004000014001e00020064400400000000000400030000000a00010064400200000a0014000200644004000014001e00020064400400000000000500030000000a00010064400200000a0014000200644004000014001e000200644004000000000001000380010540053030303033070030506f735810000030506f7359100000404672616d65000202a700705375624672616d650001090030536c6f74000100008054696d657374616d7000021a9000b053696e676c655265706f7274340000000003000300000300030000000a00010064400200000a0014000200644004000014001e00020064400400000000000400030000000a00010064400200000a0014000200644004000014001e00020064400400000000000500030000000a00010064400200000a0014000200644004000014001e0002006440040000000000010003800105001400050463706964";
    

    const char* _e2ap_pdu_short = "0005408191000008001d000500001800000005000200c8000f000101001b00020001001c00010000190012110000000000000048b56031313100310040001a00814b8149109800030000084e5243656c6c43550001400530303030350700b053696e676c655265706f7274560000000005000100000500030000000a00010064400200000a0014000200644004000014001e00020064400400000000000030506f735810000030506f7359100000404672616d650002074500705375624672616d650001020030536c6f74000100008054696d657374616d70000248b5400530303030340700b053696e676c655265706f7274560000000004000200000400030000000a00010064400200000a0014000200644004000014001e00020064400400000000000500030000000a00010064400200000a0014000200644004000014001e00020064400400000000000030506f735810000030506f7359100000404672616d650002074500705375624672616d650001020030536c6f74000100008054696d657374616d70000248b5001400050463706964";

    const char* _e2ap_pdu = _e2ap_pdu_long;
    // const char* _e2ap_pdu = _e2ap_pdu_short;

    std::string _e2ap_pduString = std::string(_e2ap_pdu);
    std::cout << "Length of string " << _e2ap_pduString.size() << std::endl;
    // std::string s = std::string(_e2ap_pdu);
    // s.erase(std::remove_if(s.begin(), s.end(), [](unsigned char x) { return std::isspace(x); }), s.end());

    char* bytes = converHexToByteLocal(_e2ap_pduString);

    std::cout << " Size new string " << std::string(bytes)<<std::endl;

    uint8_t *e2ApBuffer = (uint8_t *)calloc(1, (_e2ap_pduString.length()));
    memcpy(e2ApBuffer, bytes, (_e2ap_pduString.length()/2));

    // for (int _i = 0; _i< _e2ap_pduString.length(); ++_i){
    //     e2ApBuffer[_i] = _e2ap_pdu[_i];
    // }

    // memcpy(e2ApBuffer, (uint8_t*)_e2ap_pdu, _e2ap_pduString.length());

    int _total_bytes_consumed = 0;
    while(_total_bytes_consumed<(int)_e2ap_pduString.length()){
        std::cout << "Total bytes consumed " << _total_bytes_consumed << std::endl;
        e2ap_stcp_buffer_t *res = decode_e2ap_to_xml((e2ApBuffer+_total_bytes_consumed), (_e2ap_pduString.length()-_total_bytes_consumed));

        std::cout << "Decoding length " << res->msg_length << std::endl;
        std::cout << "Bytes consumed " << res->bytes_consumed << std::endl;
        if (res->msg_length>0){
            std::cout << "Rsult of decoding " << std::string((char*)res->msg_buffer) << std::endl;
        }else{
            break;
        }
        

        _total_bytes_consumed += (int)res->bytes_consumed;
    }

    


    // std::ostringstream ss;
    // std::copy(res->msg_buffer, res->msg_buffer+sizeof(res->msg_length), std::ostream_iterator<int>(ss, ","));
    // std::cout << ss.str() << std::endl;

    std::cout << "Finished " <<std::endl;
}