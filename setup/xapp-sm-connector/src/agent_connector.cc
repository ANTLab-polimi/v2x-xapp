#include "agent_connector.hpp"


// open client of control socket with agent
int open_control_socket_agent(const char* dest_ip, const int dest_port) {

  std::cout << "Opening control socket with host " << dest_ip << ":" << dest_port << std::endl;

  int control_sckfd = socket(AF_INET, SOCK_STREAM, 0);
  if (control_sckfd < 0) {
	  std::cout << "ERROR: OPEN SOCKET" << std::endl;
      close(control_sckfd);
      return -1;
  }

  // SET SOCKET OPTIONS TO RELEASE THE SOCKET ADDRESS IMMEDIATELY AFTER
  // THE SOCKET IS CLOSED
  int option(1);
  setsockopt(control_sckfd, SOL_SOCKET, SO_REUSEADDR, (char*)&option, sizeof(option));

  struct sockaddr_in dest_addr = {0};
  dest_addr.sin_family = AF_INET;
  dest_addr.sin_port = htons(dest_port);

  // convert dest_ip from char* to network address
  if (inet_pton(AF_INET, dest_ip, &dest_addr.sin_addr) <= 0) {
      std::cout << "ERROR CONVERTING IP TO INTERNET ADDR" << std::endl;
      close(control_sckfd); // if conversion fail, close the socket and return error -2
      return -2;
  }

  if (connect(control_sckfd, (struct sockaddr *) &dest_addr, sizeof(dest_addr)) < 0) {
      std::cout << "ERROR: CONNECT" << std::endl;
      close(control_sckfd);
      return -3;
  }

  // update map
  std::string agent_ip;
  agent_ip.assign(dest_ip);
  // std::cout << "Agent IP " << agent_ip << std::endl;
  agentIp_socket[agent_ip] = control_sckfd;

  return 0;
}


// close control sockets
void close_control_socket_agent(void) {

  std::cout << "Closing control sockets with agent(s)" << std::endl;

  std::map<std::string, int>::iterator it;
  for (it = agentIp_socket.begin(); it != agentIp_socket.end(); ++it) {
    std::string agent_ip = it->first;
    int control_sckfd = it->second;

    close(control_sckfd);
  }

  // clear maps
  std::cout << "Clearing maps" << std::endl;
  agentIp_socket.clear();
  agentIp_gnbId.clear();
}


// find agent IP of socket to use with gNB id
std::string find_agent_ip_from_gnb(unsigned char* gnb_id_trans) {

  std::map<std::string, int>::iterator it_sck;
  std::map<std::string, std::list<std::string>>::iterator it_gnb;
  std::string agent_ip;

  // convert transaction identifier (unsigned char*) to string
  std::string gnb_id(reinterpret_cast<char*>(gnb_id_trans));

  // std::cout << "Searching gnb id " << gnb_id << std::endl;

  // check if gnb_id is already in agentIp_gnbId map
  bool found = false;
  for (it_gnb = agentIp_gnbId.begin(); it_gnb != agentIp_gnbId.end(); ++it_gnb) {
    // check if string (gnb_id) is in list
    for (std::list<std::string>::iterator it = it_gnb->second.begin(); it != it_gnb->second.end(); ++it){
      // std::cout << "Comparing local " << (*it) << " with " << gnb_id << std::endl;
      if((*it).compare(gnb_id) == 0){
        agent_ip = it_gnb->first;
        found = true;
        break;
      }
    }
  }

  if (!found) {
    // check if agent_ip is already in agentIp_gnbId map
    for (it_sck = agentIp_socket.begin(); it_sck != agentIp_socket.end(); ++it_sck) {
      agent_ip = it_sck->first;

      it_gnb = agentIp_gnbId.find(agent_ip);
      if (it_gnb == agentIp_gnbId.end()) {
        // insert into agentIp_gnbId map, as single element since is the first time
        std::cout << "Inserting gnb " << gnb_id << " to agent " << agent_ip << std::endl;
        agentIp_gnbId[agent_ip].push_back(gnb_id);
        break;
      }
      else{
        // means the gnb id has not been inserted in the list, so we insert it
        // the main entry in the map exists
        std::cout << "Inserting gnb " << gnb_id << " to agent " << agent_ip << std::endl;
        agentIp_gnbId[agent_ip].push_back(gnb_id);
        break;
      }
    }
  }

  return agent_ip;
}


// send through socket
int send_socket(char* buf, std::string dest_ip) {

  int control_sckfd = -1;

  // get socket file descriptor
  std::map<std::string, int>::iterator it;
  for (it = agentIp_socket.begin(); it != agentIp_socket.end(); ++it) {
    std::string agent_ip = it->first;

    if (dest_ip.compare(agent_ip) == 0) {
      control_sckfd = it->second;
      break;
    }
  }

  if (control_sckfd == -1) {
    std::cout << "ERROR: Could not find socket for destination " << dest_ip << std::endl;
    return -1;
  }

  // const size_t max_size = 512;
  // char buf[max_size] = "Hello, Server!";  // store the data in a buffer
  size_t data_size = strlen(buf);
  // size_t data_size = sizeof(buf);
  int sent_size = send(control_sckfd ,buf, data_size, 0);
  std::cout << "Message sent with size " << sent_size << " & data size " << data_size << std::endl;

  if(sent_size < 0) { // the send returns a size of -1 in case of errors
      std::cout <<  "ERROR: SEND to agent " << dest_ip << std::endl;
      return -2;
  }
  else {
      std::cout << "Message sent" << std::endl;
  }

  return 0;
}

// modified
// send through socket
int send_payload_socket(const void* buf, int buf_size, std::string dest_ip) {

  int control_sckfd = -1;

  // get socket file descriptor
  std::map<std::string, int>::iterator it;
  for (it = agentIp_socket.begin(); it != agentIp_socket.end(); ++it) {
    std::string agent_ip = it->first;

    if (dest_ip.compare(agent_ip) == 0) {
      control_sckfd = it->second;
      break;
    }
  }

  if (control_sckfd == -1) {
    std::cout << "ERROR: Could not find socket for destination " << dest_ip << std::endl;
    return -1;
  }

  int sent_size = send(control_sckfd ,buf, buf_size, 0);

  if(sent_size < 0) { // the send returns a size of -1 in case of errors
      std::cout <<  "ERROR: SEND to agent " << dest_ip << std::endl;
      return -2;
  }
  // else {
  //     std::cout << "Message sent with size " << sent_size << std::endl;
  // }

  return 0;
}
// end modification
