import json;
import sys;
import os;
import signal;
import time;

def signal_handler(signum, frame):
    print("Received signal {0}\n".format(signum));
    if(xapp_subprocess == None or xapp_pid == None):
        print("No xapp running. Quiting without sending signal to xapp\n");
    else:
        print("Sending signal {0} to xapp ...".format(signum));
        xapp_subprocess.send_signal(signum);

#================================================================
if __name__ == "__main__":

    import subprocess;
#    cmd = ["../src/hw_xapp_main"];
    cmd = ["/usr/local/bin/decoding_test"];
    # cmd = ["/usr/local/bin/hw_unit_tests"];

    # Register signal handlers
    # signal.signal(signal.SIGINT, signal_handler);
    # signal.signal(signal.SIGTERM, signal_handler);

    # Start the xAPP
    print("Executing xAPP ....");
    # xapp_subprocess = subprocess.Popen(cmd, shell = False, stdin=None, stdout=None, stderr = None);
    _file = open(os.path.join(".", "logfile.log"), 'w')
    xapp_subprocess = subprocess.Popen(cmd, shell = False, stdin=None, stdout=_file, stderr = _file);
    xapp_pid = xapp_subprocess.pid;

    # xapp_subprocess.wait()

    # Periodically poll the process every 5 seconds to check if still alive
    while(1):
        xapp_status = xapp_subprocess.poll();
        if xapp_status == None:
            time.sleep(5);
        else:
            print("XaPP terminated via signal {0}\n".format(-1 * xapp_status));
            break;