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
import threading

"""
Signaling

・Support NAT Types
Supported 3 NAT Type for Full Cone, Restrict NAT, Restrict Port NAT.

・Using words
private == local == internal
public == global == external
peer == source/destination
full cone == topology to which any function mappable. == perfect cone

・NAT Translation (Mapping) Table in Router(gateway) Examples
Full Cone (Not should be TCP Hole punching. Only know mapped public address.)
| private address | mapped public address | peer restriction |
| 192.168.0.2:1400 | 158.92.830.2:5001 | any ip in several minutes |
| 192.168.0.3:2800 | 158.92.830.2:5002 | any ip in several minutes |

Restrict NAT (Should be TCP Hole punching.)
| private address | mapped public address | peer restriction |
| 192.168.0.2:1400 | 158.92.830.2:5001 | only 16.8.23.78 in several minutes |
| 192.168.0.3:2800 | 158.92.830.2:5002 | only 200.120.23.102 in several minutes |

Restrict Port NAT (Should be TCP Hole punching.)
| private address | mapped public address | peer restriction |
| 192.168.0.2:1400 | 158.92.830.2:5001 | only 16.8.23.78:1490 in several minutes |
| 192.168.0.3:2800 | 158.92.830.2:5002 | only 200.120.23.102:538 in several minutes |

Symmetric NAT (Can NOT be TCP Hole punching. Almost NOT Used.)
| private address | mapped public address | peer restriction |
| 192.168.0.2:1400 | 158.92.830.2:1400 | only 16.8.23.78 |
| 192.168.0.3:2800 | 158.92.830.3:2800 | only 200.120.23.102 |

* aboved ip address and port number is just example.
"""
FullCone = "Full Cone"  # 0                 Receivable packets from any source ip restricted the desctination ip's device in LAN devices
RestrictNAT = "Restrict NAT"  # 1           Receivable packet from the source ip restricted the destination ip's device in LAN devices
RestrictPortNAT = "Restrict Port NAT"  # 2  Receivable packet from the source ip+port restricted the destination ip+port's device in LAN devices
SymmetricNAT = "Symmetric NAT"  # 3         Receivable packet restricted from source ip+port to the LAN device
UnknownNAT = "Unknown NAT" # 4
NATTYPE = (FullCone, RestrictNAT, RestrictPortNAT, SymmetricNAT, UnknownNAT)

def log(*args):
    #frame = inspect.currentframe().f_back
    #print(frame.f_lineno, time.asctime(), ' '.join([str(x) for x in args]))
    return
def logEssential(*args):
    frame = inspect.currentframe().f_back
    print(frame.f_lineno, time.asctime(), ' '.join([str(x) for x in args]))

poolqueue = {}
ClientInfo = namedtuple("ClientInfo", "addr, privateaddress, node_performance, conn, metricTime")
NodeStatus = namedtuple("NodeStatus", "addr, command, data, pool, active, privateaddress, privateip, privateport, node_performance, poollength, translateDictionary, metricTime")

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
            connsAddrs[conn] = NodeStatus(addr, None, None, None, None, None, None, None, None, None, None, None)
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
            try:
                data = rSocket.recv(1024)
                log("recv:", data)
                connsAddrs[rSocket] = connsAddrs[rSocket]._replace(data=data)
                connsAddrs[rSocket] = connsAddrs[rSocket]._replace(active=True)
            except ConnectionResetError:
                log("ConnectionResetError")
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
                logEssential('^_^', sendBuff)

                #save send okyours time
                receivedTime = time.time()
                connsAddrs[wSocket] = connsAddrs[wSocket]._replace(metricTime=receivedTime) #float

                wSocket.sendto(sendBuff.encode(), addr)
                log(receivedTime)
                # log("pool={0}, nat_type={1}, ok sent to client".format(connsAddrs[wSocket].pool, NATTYPE[int(connsAddrs[wSocket].node_performance)]))
                log("pool={0}, nat_type={1}, ok sent to client".format(connsAddrs[wSocket].pool, connsAddrs[wSocket].node_performance))
            elif command == 'okregisterMe':
                log("sent registerMeAck")
                sendBuff = "registerMeAck"
                logEssential(sendBuff)
                wSocket.sendto(sendBuff.encode(), addr)
            elif command == 'translate':
                log("Sent peer address pair to Claim Node.", connsAddrs[wSocket])
                try:
                    publicaddress = connsAddrs[wSocket].translateDictionary['publicaddress']
                    privateaddress = connsAddrs[wSocket].translateDictionary['privateaddress']
                    claimNodeSocket = wSocket
                    claimNodeAddress = addr
                    overlayNetworkAddress = connsAddrs[wSocket].translateDictionary['overlayNetworkAddress']
                    token = connsAddrs[wSocket].translateDictionary['token']

                    node_performance = connsAddrs[wSocket].translateDictionary['node_performance']

                    publicaddressForPeer = connsAddrs[wSocket].translateDictionary['publicaddressForPeer']
                    privateaddressForPeer = connsAddrs[wSocket].translateDictionary['privateaddressForPeer']
                    connForPeer = connsAddrs[wSocket].translateDictionary['connForPeer']
                    overlayNetworkAddressForPeer = connsAddrs[wSocket].translateDictionary['overlayNetworkAddressForPeer']
                    nodePerformanceForPeer = connsAddrs[wSocket].translateDictionary['nodePerformanceForPeer']
                    log(connsAddrs[wSocket].translateDictionary['node_performance'])  #1.0017
                    log(connsAddrs[wSocket].translateDictionary['nodePerformanceForPeer'])   #1.001805
                except Exception as exc:
                    logEssential(f"Occured Exception about {exc}")
                    publicaddress = None
                    privateaddress = None
                    claimNodeSocket = wSocket
                    claimNodeAddress = addr

                    # overlayNetworkAddress = None
                    overlayNetworkAddress = connsAddrs[wSocket].translateDictionary['overlayNetworkAddress']
                    token = connsAddrs[wSocket].translateDictionary['token']

                    node_performance = None
                    publicaddressForPeer = None
                    privateaddressForPeer = None
                    connForPeer = None
                    overlayNetworkAddressForPeer = None
                    nodePerformanceForPeer = None

                # metricTime = connsAddrs[wSocket].translateDictionary['metricTime']
                # metricTimeForPeer = connsAddrs[wSocket].translateDictionary['metricTimeForPeer']
                # timeDiff = metricTime - metricTimeForPeer
                # awaitTime = 0.3
                awaitTime = 0.0
                # awaitTimeForPeer = 0

                sync_event = threading.Event()
                def event_claim_node():
                    # publicip, publicport = publicaddress
                    if publicaddress != None:
                        publicip, publicport = publicaddress
                    else:
                        publicip, publicport = ("", 0)

                    # privateip, privateport = privateaddress
                    if privateaddress != None:
                        privateip, privateport = privateaddress
                    else:
                        privateip, privateport = ("", 0)

                    log(publicip, publicport, privateip, privateport, overlayNetworkAddress)
                    # sendBuff = "translateAck {0} {1} {2} {3} {4} {5}".format(publicip, publicport, privateip, privateport, node_performance, overlayNetworkAddress)
                    log('publicaddress', publicaddress)
                    if publicaddress != None:
                        log('translateAck')
                        sendBuff = "translateAck {0} {1} {2} {3} {4} {5}".format(publicip, publicport, privateip, privateport, node_performance, overlayNetworkAddress)
                    else:
                        log('translateNak')
                        # sendBuff = "translateNak {0}".format(overlayNetworkAddress)
                        sendBuff = "translateNak {0} {1}".format(overlayNetworkAddress, token)
                    logEssential('^_^', sendBuff, 'to', claimNodeAddress)
                    sync_event.wait()
                    log(awaitTime)
                    time.sleep(awaitTime) #seconds
                    # wSocket.sendto(sendBuff.encode(), addr)
                    # claimNodeSocket.sendto(sendBuff.encode() + b'\n', claimNodeAddress)
                    claimNodeSocket.sendto(sendBuff.encode(), claimNodeAddress)

                def event_peer_node():
                    if publicaddress != None:
                        log("Sent peer address pair to Peer Node.")
                        publicip, publicport = publicaddressForPeer

                        # privateip, privateport = privateaddressForPeer
                        if privateaddressForPeer != None:
                            privateip, privateport = privateaddressForPeer
                        else:
                            privateip, privateport = ("", 0)

                        log(publicip, publicport, privateip, privateport, overlayNetworkAddressForPeer)
                        sendBuffForPeer = "translateAck {0} {1} {2} {3} {4} {5}".format(publicip, publicport, privateip, privateport, nodePerformanceForPeer, overlayNetworkAddressForPeer)
                        logEssential('^_^', sendBuffForPeer, 'to', publicaddress)
                        connForPeer.sendto(sendBuffForPeer.encode(), publicaddress)
                    sync_event.set()

                thread_the_node = threading.Thread(target=event_claim_node)
                thread_peer_node = threading.Thread(target=event_peer_node)
                thread_peer_node.start()
                thread_the_node.start()
                # thread_the_node = threading.Thread(target=event_claim_node)
                # if publicaddress != None:
                #     thread_peer_node = threading.Thread(target=event_peer_node)
                # if publicaddress != None:
                #     thread_peer_node.start()
                # thread_the_node.start()

            elif command == 'translateIntentional':
                log("Sent peer address pair to Claim Node.", connsAddrs[wSocket])
                try:
                    publicaddress = connsAddrs[wSocket].translateDictionary['publicaddress']
                    privateaddress = connsAddrs[wSocket].translateDictionary['privateaddress']
                    claimNodeSocket = wSocket
                    claimNodeAddress = addr
                    overlayNetworkAddress = connsAddrs[wSocket].translateDictionary['overlayNetworkAddress']
                    node_performance = connsAddrs[wSocket].translateDictionary['node_performance']

                    publicaddressForPeer = connsAddrs[wSocket].translateDictionary['publicaddressForPeer']
                    privateaddressForPeer = connsAddrs[wSocket].translateDictionary['privateaddressForPeer']
                    connForPeer = connsAddrs[wSocket].translateDictionary['connForPeer']
                    overlayNetworkAddressForPeer = connsAddrs[wSocket].translateDictionary['overlayNetworkAddressForPeer']
                    nodePerformanceForPeer = connsAddrs[wSocket].translateDictionary['nodePerformanceForPeer']
                    log(connsAddrs[wSocket].translateDictionary['node_performance'])  #1.0017
                    log(connsAddrs[wSocket].translateDictionary['nodePerformanceForPeer'])   #1.001805
                    token = connsAddrs[wSocket].translateDictionary['token']

                except Exception as exc:
                    logEssential(f"Occured Exception about {exc}")
                    publicaddress = None
                    privateaddress = None
                    claimNodeSocket = wSocket
                    claimNodeAddress = addr

                    # overlayNetworkAddress = None
                    overlayNetworkAddress = connsAddrs[wSocket].translateDictionary['overlayNetworkAddress']

                    node_performance = None
                    publicaddressForPeer = None
                    privateaddressForPeer = None
                    connForPeer = None
                    overlayNetworkAddressForPeer = None
                    nodePerformanceForPeer = None
                    token = None

                awaitTime = 0.0
                sync_event = threading.Event()
                def event_claim_node():
                    # publicip, publicport = publicaddress
                    if publicaddress != None:
                        publicip, publicport = publicaddress
                    else:
                        publicip, publicport = ("", 0)

                    # privateip, privateport = privateaddress
                    if privateaddress != None:
                        privateip, privateport = privateaddress
                    else:
                        privateip, privateport = ("", 0)

                    log(publicip, publicport, privateip, privateport, overlayNetworkAddress, token)
                    if publicaddress != None:
                        # sendBuff = "translateIntentionalAck {0} {1} {2} {3} {4} {5}".format(publicip, publicport, privateip, privateport, node_performance, overlayNetworkAddress)
                        sendBuff = "translateIntentionalAck_ {0} {1} {2} {3} {4} {5} {6}".format(publicip, publicport, privateip, privateport, node_performance, overlayNetworkAddress, token)
                        sync_event.wait()
                        log(awaitTime)
                        time.sleep(awaitTime) #seconds
                    else:
                        # sendBuff = "translateIntentionalNak {0}".format(overlayNetworkAddress)
                        sendBuff = "translateIntentionalNak_ {0} {1}".format(overlayNetworkAddress, token)
                    # wSocket.sendto(sendBuff.encode(), addr)
                    logEssential('^_^', sendBuff, 'to', claimNodeAddress)
                    claimNodeSocket.sendto(sendBuff.encode(), claimNodeAddress)

                thread_the_node = threading.Thread(target=event_claim_node)
                thread_the_node.start()
            
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
    # log(connsAddrs)
    for key in connsAddrs:
      log(connsAddrs[key].active)
      if connsAddrs[key].active:
        connsAddrs[key] = connsAddrs[key]._replace(active=False)
        data = connsAddrs[key].data
        addr = connsAddrs[key].addr
        conn = key
        if data != b'':
            logEssential(data)
        log(addr)
        log(conn)
        if data.startswith(b"registerMe "):
            log("received registerMe")
            log("connection from {}".format(addr))
            log(data)

            #  data format:
            #  {private ip} {private port} {node performance} {address length} {overlayNetworkAddress}null
            #  ex.
            #  '192.168.0.34 1402 12345.432 128 8d3a6c0be806ba24b319f088a45504ea7d601970e0f820ca6965eeca1af2d8747d5bdf0ab68a30612004d54b88fe32a654fb7b300568acf8f3e8c6be439c20b9\x00'
            # log("---")
            log(data.decode().strip())
            # command, privateip, privateport, node_performance, poollength, pool = data.decode().strip().split()
            command, privateip, privateport, node_performance, poollength, pool = data.decode().strip().rstrip('\x00').split()

            privateaddress = (privateip, privateport)
            connsAddrs[key] = connsAddrs[key]._replace(command=command, privateip=privateip, privateport=privateport, node_performance=node_performance, poollength=poollength, pool=pool.rstrip('\x00'), privateaddress=privateaddress)
            log(connsAddrs[key].command)
            log(connsAddrs[key].privateaddress)
            log(connsAddrs[key].node_performance)
            log(connsAddrs[key].poollength)
            log(connsAddrs[key].pool)
            log(connsAddrs[key].metricTime)

        elif data.startswith(b"okregisterMe"):
            log("received okregisterMe")
            log(data, addr)
            connsAddrs[key] = connsAddrs[key]._replace(command="okregisterMe")
            log(connsAddrs[key].command)
            log("request received for pool:", connsAddrs[key].pool)
            #take metric time since send okyours time
            receivedTime = time.time()
            metricTime = receivedTime - connsAddrs[key].metricTime
            log(receivedTime)
            log(connsAddrs[key].metricTime)
            log(metricTime)
            poolqueue[connsAddrs[key].pool] = ClientInfo(addr, connsAddrs[key].privateaddress, connsAddrs[key].node_performance, conn, metricTime)
            # connsAddrs[key] = connsAddrs[key]._replace(metricTime=metricTime) #float

        elif data.startswith(b"translate "):
            log("received translate")
            log("connection from {}".format(addr))
            log(data)
            log(data.decode().strip())
            # command, poollength, pool = data.decode().strip().split()
            command, poollength, pool, token = data.decode().strip().rstrip('\x00').split()
            log(command)
            log(poollength)
            log(pool)
            log(token)
            log(poolqueue)
            try:
                translateDictionary = {}
                #to claimed node
                log(poolqueue[pool])
                translateDictionary['publicaddress'] = poolqueue[pool].addr

                # translateDictionary['privateaddress'] = poolqueue[pool].privateaddress
                outerip, outerport = poolqueue[pool].addr
                innerip, innerport = poolqueue[pool].privateaddress
                log(outerip, innerip)
                if outerip == innerip:
                    log("node is in outer network.")
                    translateDictionary['privateaddress'] = None
                else:
                    log("node is in inner NAT network.")
                    translateDictionary['privateaddress'] = poolqueue[pool].privateaddress
                    
                poolForPeer, overlayNetworkAddressForPeer = poolqueueForPeer(addr)
                log(poolForPeer, overlayNetworkAddressForPeer)
                translateDictionary['overlayNetworkAddress'] = pool.rstrip('\x00')
                translateDictionary['metricTime'] = poolqueue[pool].metricTime
                translateDictionary['node_performance'] = poolqueue[pool].node_performance
                #to peer node
                translateDictionary['publicaddressForPeer'] = poolForPeer.addr
                translateDictionary['privateaddressForPeer'] = poolForPeer.privateaddress
                translateDictionary['connForPeer'] = poolqueue[pool].conn
                translateDictionary['overlayNetworkAddressForPeer'] = overlayNetworkAddressForPeer
                translateDictionary['metricTimeForPeer'] = poolForPeer.metricTime
                translateDictionary['nodePerformanceForPeer'] = poolForPeer.node_performance
                translateDictionary['token'] = token

                log(translateDictionary)
                connsAddrs[key] = connsAddrs[key]._replace(command=command, translateDictionary=translateDictionary)
                log(connsAddrs)
            except KeyError:
                logEssential("no record for {} Cause reply translateNak.".format(pool))
                translateDictionary = {}
                translateDictionary['publicaddress'] = None
                translateDictionary['privateaddress'] = None
                translateDictionary['overlayNetworkAddress'] = pool.rstrip('\x00')
                translateDictionary['metricTime'] = None
                translateDictionary['node_performance'] = None
                translateDictionary['publicaddressForPeer'] = None
                translateDictionary['privateaddressForPeer'] = None
                translateDictionary['connForPeer'] = None
                translateDictionary['overlayNetworkAddressForPeer'] = None
                translateDictionary['metricTimeForPeer'] = None
                translateDictionary['nodePerformanceForPeer'] = None
                translateDictionary['token'] = token
                log(translateDictionary)
                connsAddrs[key] = connsAddrs[key]._replace(command=command, translateDictionary=translateDictionary)
        elif data.startswith(b"translateIntentional "):
            log("received translateIntentional")
            log("connection from {}".format(addr))
            log(data)
            log(data.decode().strip())
            # command, poollength, pool = data.decode().strip().split()
            # split data at terminator{\n\x00}
            # command, pool, token = data.decode().split('\n\x00')[0].strip().split()
            command, operands, token = data.decode().split('\n\x00')[0].strip().split()
            pool, originalToken = operands.strip().split(',')
            log(command)
            log(pool)
            # log(originalToken)
            log(poolqueue)
            try:
                translateDictionary = {}
                #to claimed node
                translateDictionary['publicaddress'] = poolqueue[pool].addr

                # translateDictionary['privateaddress'] = poolqueue[pool].privateaddress
                outerip, outerport = poolqueue[pool].addr
                innerip, innerport = poolqueue[pool].privateaddress
                log(outerip, innerip)
                if outerip == innerip:
                    log("node is in outer network.")
                    translateDictionary['privateaddress'] = None
                else:
                    log("node is in inner NAT network.")
                    translateDictionary['privateaddress'] = poolqueue[pool].privateaddress
                    
                poolForPeer, overlayNetworkAddressForPeer = poolqueueForPeer(addr)
                log(poolForPeer, overlayNetworkAddressForPeer)
                translateDictionary['overlayNetworkAddress'] = pool
                translateDictionary['metricTime'] = poolqueue[pool].metricTime
                translateDictionary['node_performance'] = poolqueue[pool].node_performance
                translateDictionary['token'] = token
                # translateDictionary['token'] = originalToken

                #to peer node
                translateDictionary['publicaddressForPeer'] = poolForPeer.addr
                translateDictionary['privateaddressForPeer'] = poolForPeer.privateaddress
                translateDictionary['connForPeer'] = poolqueue[pool].conn
                translateDictionary['overlayNetworkAddressForPeer'] = overlayNetworkAddressForPeer
                translateDictionary['metricTimeForPeer'] = poolForPeer.metricTime
                translateDictionary['nodePerformanceForPeer'] = poolForPeer.node_performance

                log(translateDictionary)
                connsAddrs[key] = connsAddrs[key]._replace(command=command, translateDictionary=translateDictionary)
                log(connsAddrs)
            except KeyError:
                logEssential("no record for {}".format(pool))
                translateDictionary = {}
                translateDictionary['publicaddress'] = None
                translateDictionary['privateaddress'] = None
                translateDictionary['overlayNetworkAddress'] = pool
                translateDictionary['metricTime'] = None
                translateDictionary['node_performance'] = None
                # translateDictionary['token'] = originalToken
                translateDictionary['token'] = token
                translateDictionary['publicaddressForPeer'] = None
                translateDictionary['privateaddressForPeer'] = None
                translateDictionary['connForPeer'] = None
                translateDictionary['overlayNetworkAddressForPeer'] = None
                translateDictionary['metricTimeForPeer'] = None
                translateDictionary['nodePerformanceForPeer'] = None
                log(translateDictionary)
                connsAddrs[key] = connsAddrs[key]._replace(command=command, translateDictionary=translateDictionary)
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
