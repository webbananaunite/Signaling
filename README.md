# BlockChain Library Suite
[日本語](READMEjp.md)

## about blocks
blocks is a iOS library as introduce BlockChain System to your Apps, based on Satoshi Nakamoto's Paper,
for various purpose (*** Exclude exchangeable digital currency in cryptocurrency exchange ***) iOS App.  

Characteristically, blocks is pre-contained Activities in Social System (Government, Public, Private Sectors) as Birth Registration, Residential Record, Guarantor.

It is depend on overlayNetwork library.

## about overlayNetwork
overlayNetwork is a iOS library as Peer-to-Peer Overlay Network Communicate System, based on Distributed Hash Table Lookup Protocol MIT Laboratory's Paper named Chord.  

Nothing depending other libraries.

## about Testy
Testy is alternative to Basic Resident Register Card.  

It is made as Reference iOS App based on blocks and overlayNetwork libraries.

## about Signaling
Signaling coordinate Node to Node Communication (TCP/IP) in Overlay Network, with NAT Traverse,
as Translate OverlayNetworkAddress to IP/Port.

Signaling emit signal at claim by Nodes in Cloud (Python).

Signaling make NAT Traverse in Overlay Network.

## download
blocks - BlockChain Library α version  
[download](https://github.com/webbananaunite/blocks)  
https://github.com/webbananaunite/blocks  
 
overlayNetwork - Peer-to-Peer Overlay Network Communicate Library β version  
[download](https://github.com/webbananaunite/overlayNetwork)  
https://github.com/webbananaunite/overlayNetwork  
 
Testy - Basic Resident Register Application β version  
[download](https://github.com/webbananaunite/Testy)  
https://github.com/webbananaunite/Testy  
 
Signaling - Coordinater in Translate OverlayNetworkAddress to IP/Port β version  
[download](https://github.com/webbananaunite/Signaling)  
https://github.com/webbananaunite/Signaling  

## How to Use
### Swift Package (Recommended)
1) Open Testy Project or Your App Project in Xcode.  
2) File - Add Packages
3) Input following blocks URL to Search or Enter Package URL Box on UpRight.
https://github.com/webbananaunite/blocks
4) You see blocks library's README.md.
5) Tap Add Package Button on DownRight.
6) Make Sure there Added blocks library in Project - Frameworks, Libraries and Embeded Content.
7) Make Sure there Added The BlockChain Library Suite(blocks and overlayNetwork libraries) at Package Dependencies in Project Navigator in Xcode.
8) At First, a Simulator / Device must run as Boot Node.
   For App run as Boot Node, Set {RunAsBootNode} as Run Argument / Environment Variable on Edit Scheme on Xcode.
9) Xcode Build and Install Devices or Simulators.  
10) Open App and Tap "Join blocks Network" Button then Start Communication to Signaling Server on Cloud.  
11) Wait Around 8 min. up to Done Initialize DHC table. (Initial Boot time Only)  
### Carthage (*Not Available upper 0.3.0, Use Swift Package Instead)
- $ cd your project directory
- $ echo 'github "webbananaunite/blocks" "carthage"' > Cartfile
- $ carthage update --use-xcframeworks
### CocoaPods (*Not Available upper 0.3.0, Use Swift Package Instead)
- $ cd your project directory
- $ pod init
- $ vi Podfile
```
target 'target name in your App proj' do
  use_frameworks!
	pod 'blocks-blockchain'
end
```
- $ pod install
- Open your app.xcworkspace created by pod.

## limitations
NOT running Boot Node in Public Network yet in Beta Version. Cause First device must run as Boot Node.  
Signaling Server is Working on Cloud.

## license
blocks library & overlayNetwork library & Testy is published under MIT License,  
as embedding your apps, any who can use any purpuse (*** Exclude exchangeable digital currency in cryptocurrency exchange ***). by free.

## prohibited matter
Use as exchangeable digital currency in cryptocurrency exchange is PROHIBITED.

## description
### Actors:
- Boot Node

First Node in Overlay Network (blocks P2P Network).

- Baby Sitter

As A Node Joinning Overlay Network in OSI Session Layer, At First, Take Baby Sitter Node's IP and Port From TXT Record in bind Server.  
Then Send FS Command to Baby Sitter Node for any Entry in Distributed Hush Table (Code Protocol).  

- Taker

First of All, As Joinning blocks Block Chain Network in OSI Presentation/Application Layer, The Node Should Submit Application for Birth Registration to The Network.
No There Administrator Node/Person In The Network, The Node Should Find Taker Node for Send AT (Ask For Taker) Claim as Publish Transaction.

- Booker

The Booker Node Collect Non-Booked Transactions, Do Proof of Work as Calculate A Nonce, Publish Block.  
As Firstest and Legitimate Nonce Value than Other Node, The Node be Booker.  
The Booker Do Beheivier as Temporary Administrator of Book (blocks Block Chain) Up to Next Proof of Work.

### Things:
- Book

What Wrote blocks Block Chain.


### language:  
- SwiftUI (Protocol Oriented) 
- C++ (Metal) 
- objc (DNS resolv)
- Python (Signaling)

### using 3rd party libraries:
Nothing, but program include other one copyrights.  
- QuadKey - Microsoft Corporation  
- SHA-512 - Aaron D. Gifford

### programming architecture:  
around DDD, Onion (Protocol Oriented)

### byteOrder:  
- Distributed Hash Table (Finger table) address  
Little Endian

- nonce  
Little Endian

### cpu, gpu:
nonce calculator is choosable cpu or gpu.

## status
Beta  
Have Implemented All Features but following Advanced Features.

#### Un Implemented Advanced Features (as 20240709 13:33 JST Tokyo):
- Complessed Block, Light Node
- Complessed Command Operand
- Be Hi-Speed Detect Duplicate Birth Transaction、BasicIncome Transaction
- Procedure as for Occurred Irregular
- Write Documents for Developer
- Make and Boot up Boot Node on Cloud (linux)
- Beta Test
- Multi Signaling Servers Orchestration Work 

#### Join us!:
Interested in Building Social Infrastructure by Peer-to-Peer Overlay Network, Block-chain System, On volunteer, please join my Project.  

but, Don't accept application from one related to Cryptocurrency Exchange.  

Let's Make Our Future!  
