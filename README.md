# BlockChain Library Suite
[日本語](READMEjp.md)

## All We Did up to 20250318
All Done applied on Linux Platform except Calculate Nonce as same Code as iOS/iPadOS. Should be install Swift Compiler to Linux [download](https://www.swift.org/install/linux/#platforms)https://www.swift.org/install/linux/#platforms.  

Running BootNode in Public Network. (Library will find out TXT Records on Name Server.) But it is cheep environment cause Suddenly Stop BootNode as Shorting Memory.  

Signaling Server is Working in Public Network. (Library will find out TXT Records on Name Server.)  

## Our Goals
In Our Goaled Community, Use Blockchained Points issued by the SYSTEM(in other words Autonomous Intelligence) instead of Money issued by CentralBank/Fed./Gov./Co. (Coin/Bill/Credit/Debit/Prepaid).  

Blockchained Points is for exchange Goods/Services.  

Must NOT any Working for get the Points.  
Get the Points every month on demand.  

## blocks
blocks is a iOS/Linux library as introduce BlockChain System to your Apps, based on Satoshi Nakamoto's Paper,  
for various purpose (*** Exclude exchangeable digital currency in cryptocurrency exchange ***) iOS App/Linux App.  

Characteristically, blocks is pre-contained Activities in Social System (Government, Public, Private Sectors) as Birth Registration, Residential Record, Guarantor.

It is depend on overlayNetwork library.

## overlayNetwork
overlayNetwork is a iOS/Linux library as Peer-to-Peer Overlay Network Communicate System, based on Distributed Hash Table Lookup Protocol MIT Laboratory's Paper named Chord.  

Do Communicate Other Node with NAT Traverse (TCP Hole punching).  

Work with POSIX select() system call as Multiplexing Communication in Swift Code.  

Nothing depending other libraries.  

## Testy
Testy is alternative to Basic Resident Register Card. (Work on iOS/Linux)  

It is made as Reference iOS App/Linux App based on blocks and overlayNetwork libraries.

## Signaling
Signaling coordinate Node to Node Communication (TCP/IP) in Overlay Network, with NAT Traverse,
as Translate OverlayNetworkAddress to IP/Port.

Signaling emit signal at claim by Nodes in Cloud (Python Code).

Signaling make NAT Traverse (TCP Hole punching) in Overlay Network.  

Work with POSIX select() system call as Multiplexing Communication in Python Code.  

## download
blocks - BlockChain Library  
[download](https://github.com/webbananaunite/blocks)  
https://github.com/webbananaunite/blocks  
 
overlayNetwork - Peer-to-Peer Overlay Network Communicate Library NAT Traverse (TCP Hole punching)  
[download](https://github.com/webbananaunite/overlayNetwork)  
https://github.com/webbananaunite/overlayNetwork  
 
Testy - Basic Resident Register Application  
[download](https://github.com/webbananaunite/Testy)  
https://github.com/webbananaunite/Testy  
 
Signaling - Coordinater in Translate OverlayNetworkAddress to IP/Port NAT Traverse (TCP Hole punching)  
[download](https://github.com/webbananaunite/Signaling)  
https://github.com/webbananaunite/Signaling  

## How to Build Linux Apps with Closs-Compile on macOS as using Swift Linux Static Library
0) To Open Project for Linux App, Open Testy/Package.swift in Xcode instead Testy/Testy.xcodeproj.  
1) Download and Install Swift Compiler [download](https://www.swift.org/install/macos/)https://www.swift.org/install/macos/.  
  ex. swift-6.0.3-RELEASE-osx.pkg  
2) Extract toolchain spcifier for define TOOLCHAINS environment variable.  
```
$ plutil -extract CFBundleIdentifier raw /Library/Developer/Toolchains/swift-6.0.3-RELEASE.xctoolchain/Info.plist 
org.swift.603202412101a
```
3) Install Static Linux SDK for Swift cf. [https://www.swift.org/documentation/articles/static-linux-getting-started.html](https://www.swift.org/documentation/articles/static-linux-getting-started.html)  
```
$ TOOLCHAINS=org.swift.603202412101a swift sdk install ~/Downloads/swift-6.0.3-RELEASE_static-linux-0.0.1.artifactbundle.tar.gz
```
4) Closs-Compile for Linux App  
```
$ cd ~/Documents/block\ chain/Testy
$ TOOLCHAINS=org.swift.603202412101a swift build -v --swift-sdk x86_64-swift-linux-musl --build-path ~/appOutput/Testy
```
5) Copy binary to Target Linux.  
```
ex.
$ scp -i {your key file} ~/appOutput/Testy/x86_64-swift-linux-musl/debug/TestyOnLinux {target user}@{target host name}:{target path}
```
6) Set Target Run Environment on by Linux Distribution  
[download](https://www.swift.org/install/linux/#platforms)https://www.swift.org/install/linux/#platforms  
```
ex.
$ wget https://download.swift.org/swift-6.0.3-release/ubi9/swift-6.0.3-RELEASE/swift-6.0.3-RELEASE-ubi9.tar.gz
$ tar -xzf swift-6.0.3-RELEASE-ubi9.tar.gz
$ vi .bashrc
export PATH=~/swift-6.0.3-RELEASE-ubi9/usr/bin:"${PATH}"
```
7) Run App on shell.
```
$ lldb TestyLinux
```

## How to Build with Xcode on iPhone/iPad
### Swift Package (Recommended)
1) Open Testy Project or Your App Project in Xcode.  
2) File - Add Packages
3) Input following blocks URL to Search or Enter Package URL Box on UpRight.
https://github.com/webbananaunite/blocks
4) You see blocks library's README.md.
5) Tap Add Package Button on DownRight.
6) Make Sure there Added blocks library in Project - Frameworks, Libraries and Embeded Content.
7) Make Sure there Added The BlockChain Library Suite(blocks and overlayNetwork libraries) at Package Dependencies in Project Navigator in Xcode.
8) Xcode Build and Install Devices or Simulators.  
9) Open App and Tap "Join blocks Network" Button then Start Communication to Signaling Server on Cloud.  
10) Wait Around 5 min. up to Done Initialize OverlayNetwork Finger table. (Initial Boot time Only)  
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
BootNode Running in Public Network is cheep environment cause Suddenly Stop BootNode as Shorting Memory.  

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
- Swift (Protocol Oriented)
- SwiftUI iOS only
- C++ (Metal) iOS only
- objc (DNS resolv) iOS only
- Python (Signaling)

### using 3rd party libraries:
Nothing, but program include other one copyrights.  
- QuadKey - Microsoft Corporation  
- SHA-512 - Aaron D. Gifford

### programming architecture:  
DDD, Onion Architecture (Protocol Oriented)

### byteOrder:  
- Distributed Hash Table (Finger table) address  
Little Endian

- nonce  
Little Endian

### cpu, gpu:
nonce calculator is choosable cpu or gpu. iOS only

## status
Beta  
Have Implemented All Features but following Advanced Features.

#### Un Implemented Advanced Features (as 20250318 16:53 JST Tokyo):
- Complessed Block, Light Node
- Complessed Command Operand
- Be Hi-Speed Detect Duplicate Birth Transaction, BasicIncome Transaction
- Procedure as for Occurred Irregular
- Write Documents for Developer
- Beta Test
- Multi Signaling Servers Orchestration Work 
