
#include "nr-sl-sci-f1a-header.h"
#include "nr-sl-mac-pdu-tag.h"
#include "google/protobuf/message.h"

#include <stdio.h>
#include <dlfcn.h>


int main(int argc, char* argv[]){
    void *myso = dlopen("/usr/local/lib/libe2sim.so", RTLD_GLOBAL);
    std::cout << "Dl openened" << std::endl;
    // dlclose(myso);

    std::cout << "End of main" << std::endl;
}