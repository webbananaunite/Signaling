#!/usr/bin/env python
# coding:utf-8
"""
Based Paper:
Peer-to-Peer Communication Across Network Address Translators

Thank:
https://gist.github.com/somic/224795
https://github.com/laike9m/PyPunchP2P
"""

import socket
import struct
import sys
from collections import namedtuple
from select import select
import time
import inspect

"""
Supported 3 NAT Type for Full Cone, Restrict NAT, Restrict Port NAT.
"""
FullCone = "Full Cone"  # 0
RestrictNAT = "Restrict NAT"  # 1
RestrictPortNAT = "Restrict Port NAT"  # 2
SymmetricNAT = "Symmetric NAT"  # 3
UnknownNAT = "Unknown NAT" # 4
NATTYPE = (FullCone, RestrictNAT, RestrictPortNAT, SymmetricNAT, UnknownNAT)

# def log(*args):
#     frame = inspect.currentframe().f_back
#     print(frame.f_code.co_name, frame.f_lineno, time.asctime(), ' '.join([str(x) for x in args]))
# def log(*args):
#     # frame = inspect.currentframe().f_back
#     print(' '.join([str(x) for x in args]))
def log(*args):
    frame = inspect.currentframe().f_back
    print(frame.f_lineno, ' '.join([str(x) for x in args]))

poolqueue = {}
ClientInfo = namedtuple("ClientInfo", "addr, privateaddress, nat_type_id, conn")
NodeStatus = namedtuple("NodeStatus", "addr, command, data, pool, active, privateaddress, privateip, privateport, nat_type_id, poollength, translateDictionary")

def main():
    port = sys.argv[1]
    try:
        port = int(sys.argv[1])
    except (IndexError, ValueError):
        pass

    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sockfd.bind(("", port))
    sockfd.listen(10)
    sockfd.settimeout(1)    #Timeout secods on accept, recv, send
    log("listening on *:%d (tcp)" % port)
    conns = []
    connsAddrs = {}

    while True:
        try:
            log("Wait Connection for Acceptable.")
            conn = addr = None
            conn, addr = sockfd.accept()
        except socket.timeout:
            log("accept timeout occurred.")
        if conn != None and addr != None:
            log('^_^Connectted address: ', addr)
            conns.append(conn)
            log(conn)
            log(addr)
            connsAddrs[conn] = NodeStatus(addr, None, None, None, None, None, None, None, None, None, None)
            log(connsAddrs)
        selectsocket(conns, connsAddrs)
    log("program end.")

def selectsocket(conns, connsAddrs):
    log(len(conns))
    log(len(connsAddrs))
    if conns == [] or connsAddrs == {}:
        log("Not There Connected Node.")
        return
    r,w,x = select(conns, conns, [], 0)
    if r:
        log("r", len(r))
        for rSocket in r:
            data = rSocket.recv(1024)
            log("recv:", data)
            connsAddrs[rSocket] = connsAddrs[rSocket]._replace(data=data)
            connsAddrs[rSocket] = connsAddrs[rSocket]._replace(active=True)
        receivedDataProcess(connsAddrs)
    if w:
        log("w", len(w))
        for wSocket in w:
            command = connsAddrs[wSocket].command
            addr = connsAddrs[wSocket].addr
            log(command)
            if command == 'registerMe':
                log("sent okyours")
                log(connsAddrs)
                ip, port = addr
                sendBuff = "okyours {0}:{1}".format(ip, port)
                log('^_^', sendBuff)
                wSocket.sendto(sendBuff.encode(), addr)
                log("pool={0}, nat_type={1}, ok sent to client".format(connsAddrs[wSocket].pool, NATTYPE[int(connsAddrs[wSocket].nat_type_id)]))
            elif command == 'okregisterMe':
                log("sent registerMeAck")
                sendBuff = "registerMeAck"
                log(sendBuff)
                wSocket.sendto(sendBuff.encode(), addr)
            elif command == 'translate':
                log("Sent peer address pair to Claim Node.")
                #connsAddrsを表示
                

                publicaddress = connsAddrs[wSocket].translateDictionary['publicaddress']
                privateaddress = connsAddrs[wSocket].translateDictionary['privateaddress']
                overlayNetworkAddress = connsAddrs[wSocket].translateDictionary['overlayNetworkAddress']
                publicaddressForPeer = connsAddrs[wSocket].translateDictionary['publicaddressForPeer']
                privateaddressForPeer = connsAddrs[wSocket].translateDictionary['privateaddressForPeer']
                connForPeer = connsAddrs[wSocket].translateDictionary['connForPeer']
                overlayNetworkAddressForPeer = connsAddrs[wSocket].translateDictionary['overlayNetworkAddressForPeer']

                publicip, publicport = publicaddress
                privateip, privateport = privateaddress
                log(publicip, publicport, privateip, privateport, overlayNetworkAddress)
                sendBuff = "translateAck {0} {1} {2} {3} {4}".format(publicip, publicport, privateip, privateport, overlayNetworkAddress)
                log('^_^', sendBuff)
                wSocket.sendto(sendBuff.encode(), addr)

                log("Sent peer address pair to Peer Node.")
                publicip, publicport = publicaddressForPeer
                privateip, privateport = privateaddressForPeer
                log(publicip, publicport, privateip, privateport, overlayNetworkAddressForPeer)
                sendBuffForPeer = "translateAck {0} {1} {2} {3} {4}".format(publicip, publicport, privateip, privateport, overlayNetworkAddressForPeer)
                log('^_^', sendBuffForPeer)
                connForPeer.sendto(sendBuffForPeer.encode(), publicaddress)
            else:
                log("else command None")
            connsAddrs[wSocket] = connsAddrs[wSocket]._replace(command=None)

def poolqueueForPeer(addr):
    for key in poolqueue:
        if poolqueue[key].addr == addr:
            return poolqueue[key], key

"""
Receive Data, and attach any processes.
"""
def receivedDataProcess(connsAddrs):
    log(connsAddrs)
    for key in connsAddrs:
      log(connsAddrs[key].active)
      if connsAddrs[key].active:
        connsAddrs[key] = connsAddrs[key]._replace(active=False)
        data = connsAddrs[key].data
        addr = connsAddrs[key].addr
        conn = key
        log(data)
        log(addr)
        log(conn)

        if data.startswith(b"registerMe "):
            log("received registerMe")
            log("connection from {}".format(addr))
            log(data)

            #  data format:
            #  {private ip} {private port} {nat type id} {address length} {overlayNetworkAddress}null
            #  ex.
            #  '192.168.0.34 1402 0 128 8d3a6c0be806ba24b319f088a45504ea7d601970e0f820ca6965eeca1af2d8747d5bdf0ab68a30612004d54b88fe32a654fb7b300568acf8f3e8c6be439c20b9\x00'
            # log("---")
            log(data.decode().strip())
            command, privateip, privateport, nat_type_id, poollength, pool = data.decode().strip().split()
            privateaddress = (privateip, privateport)
            connsAddrs[key] = connsAddrs[key]._replace(command=command, privateip=privateip, privateport=privateport, nat_type_id=nat_type_id, poollength=poollength, pool=pool, privateaddress=privateaddress)
            log(connsAddrs[key].command)
            log(connsAddrs[key].privateaddress)
            log(connsAddrs[key].nat_type_id)
            log(connsAddrs[key].poollength)
            log(connsAddrs[key].pool)

        elif data.startswith(b"okregisterMe"):
            log("received okregisterMe")
            log(data, addr)
            connsAddrs[key] = connsAddrs[key]._replace(command="okregisterMe")
            log(connsAddrs[key].command)
            log("request received for pool:", connsAddrs[key].pool)
            poolqueue[connsAddrs[key].pool] = ClientInfo(addr, connsAddrs[key].privateaddress, connsAddrs[key].nat_type_id, conn)

        elif data.startswith(b"translate "):
            log("received translate")
            log("connection from {}".format(addr))
            log(data)
            log(data.decode().strip())
            command, poollength, pool = data.decode().strip().split()
            log(command)
            log(poollength)
            log(pool)
            log(poolqueue)
            try:
                translateDictionary = {}
                #to claimed node
                translateDictionary['publicaddress'] = poolqueue[pool].addr
                translateDictionary['privateaddress'] = poolqueue[pool].privateaddress
                poolForPeer, overlayNetworkAddressForPeer = poolqueueForPeer(addr)
                log(poolForPeer, overlayNetworkAddressForPeer)
                translateDictionary['overlayNetworkAddress'] = pool
                #to peer node
                translateDictionary['publicaddressForPeer'] = poolForPeer.addr
                translateDictionary['privateaddressForPeer'] = poolForPeer.privateaddress
                translateDictionary['connForPeer'] = poolqueue[pool].conn
                translateDictionary['overlayNetworkAddressForPeer'] = overlayNetworkAddressForPeer
                log(translateDictionary)
                connsAddrs[key] = connsAddrs[key]._replace(command=command, translateDictionary=translateDictionary)
                log(connsAddrs)
            except KeyError:
                log("connection from {}".format(addr))
        else:
            log("received illigal command", data)
            command = None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        log("usage: server.py port")
        exit(0)
    else:
        assert sys.argv[1].isdigit(), "port should be a number!"
        main()
