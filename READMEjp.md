# BlockChain Library Suite

## all we did up 20250806 1900JST
見直したソケット通信におけるNATトラバーサルでハンドシェイク機能を修正しました。  

## 20250806 updated
translateできない場合の問題を修正しました。  
overlayNetworkアドレス翻訳テーブルを追加しました。translateNakへの対応のため。  
ソケット通信が大幅に見直されました。(overlayNetwork library)  

## 20250701までに完成した事
- イレギュラー発生時の手続き(in overlayNetwork library)  
Node離脱時に発生するtranslateNak(overlayNetworkAddressのIP変換不可)への対応(as Init Finger Table)  
Chord Finger Table中のSuccessor Nodeを複数候補記憶するように変更しました。  
例外割り込みのためのEnQueueメソッドを追加しました。(コマンドキュー、通信キュー)  

## 20250318までに完成した事
Linuxプラットフォームへの対応が完了しました。ただし、ノンス計算には対応していません。  
ソースコードはLinuxとiOSで共通です。(Swift Code)  
動作させるにはSwift環境をインストールする必要があります。[download](https://www.swift.org/install/linux/#platforms)https://www.swift.org/install/linux/#platforms  

ブートノードが公開ネットワークで動作し始めました。
BlockChain LibraryはネームサーバーのTXTレコードからブートノードを見つけ出します。  
ただし、インフラが貧弱なためブートノードはメモリ不足で停止する場合があります。  

シグナリングサーバー（NAT横断のためのTCPホールパンチング）が公開ネットワーク上で動作しています。
BlockChain LibraryはネームサーバーのTXTレコードからシグナリングサーバーを見つけ出します。  

## 私たちのゴール
中央銀行／政府／企業が発行したお金（硬貨、紙幣、クレジット、デビッド、プリペイド）の代わりに、システム（言い換えれば、自律インテリジェンス）によって発行されるポイント*で生活する社会をめざします。  
*ブロックチェーンで管理されるポイント  

ブロックチェーンで管理されるポイントはモノやサービスのやり取りに使われます。  

このポイントを得るために働く必要はありません。  
要求に応じて、毎月ポイントが発行されます。  

## blocks 
blocks は中本智さんの論文に基づいて開発されたiOS/Linuxライブラリです。
あなたのアプリにブロックチェーンを導入できます。

いろんな目的に使用できますが、仮想通貨取引所で交換可能な暗号資産として使用することを禁止します。

このブロックチェーン・ライブラリが特徴的なのは、政府・公共・民間の社会システムにおける活動をあらかじめ組み込まれていることです。（出生証明、住民票、身元保証など）

添付の overlayNetwork ライブラリに依存します。

## overlayNetwork 
overlayNetwork は、Peer-to-Peerオーバーレイ・ネットワーク通信システムです。
MIT Laboratoryの分散ハッシュテーブルの実装である Chord 論文に基づいて開発されたものです。

NAT越え（TCPホールパンチング）により他のノードと通信します。  

POSIX select() システムコールにより多重化通信を実現しています。(Swift Code)  

他のライブラリに依存しません。

## Testy 
Testy は住民基本台帳カードの代替として開発されています。

blocksライブラリとoverlayNetworkライブラリの使用参考例として作成されたiOS/Linuxアプリです。

## Signaling 
Signalingはオーバーレイネットワークにおいて、NATトラバーサルを用い、オーバーレイネットワークアドレスをIP/ポートに変換することで、ノード間の通信をコーディネートします。  

Signalingはクラウド上で動作し、ノードの要求に応じ、通信調整を行います。  

Signalingはオーバーレイネットワークにおいて、NAT越え（TCPホールパンチング）により他のノードと通信します。  

POSIX select() システムコールにより多重化通信を実現しています。(Swift Code)  

## download

blocks - ブロックチェーン・ライブラリ  
[ダウンロード](https://github.com/webbananaunite/blocks)  
https://github.com/webbananaunite/blocks  
 
overlayNetwork - peer-to-peer分散ハッシュテーブル通信ライブラリ　NAT越え（TCPホールパンチング）  
[ダウンロード](https://github.com/webbananaunite/overlayNetwork)  
https://github.com/webbananaunite/overlayNetwork  
 
Testy - 住民基本台帳アプリ  
[ダウンロード](https://github.com/webbananaunite/Testy)  
https://github.com/webbananaunite/Testy  
 
Signaling - オーバーレイネットワークアドレスをIP/ポートに変換　NAT越え（TCPホールパンチング）  
[ダウンロード](https://github.com/webbananaunite/Signaling)  
https://github.com/webbananaunite/Signaling  

## Linuxアプリとしてのビルド方法　ー　Swift Linux Static Libraryを用いてmacOS上でのクロスコンパイル
0) Linux用プロジェクトを開くには、Testy/Package.swiftをXcodeで開きます。Testy/Testy.xcodeprojではなく。  
1) Swiftコンパイラーをダウンロード、インストール [download](https://www.swift.org/install/macos/)https://www.swift.org/install/macos/.  
  ex. swift-6.0.3-RELEASE-osx.pkg  
2) TOOLCHAINS環境変数に定義するためのツールチェーン定義を抽出  
```
$ plutil -extract CFBundleIdentifier raw /Library/Developer/Toolchains/swift-6.0.3-RELEASE.xctoolchain/Info.plist 
org.swift.603202412101a
```
3) Static Linux SDK for Swiftをインストール cf.   [https://www.swift.org/documentation/articles/static-linux-getting-started.html](https://www.swift.org/documentation/articles/static-linux-getting-started.html)  
```
$ swift sdk install /Users/yoichi/Downloads/swift-6.1.2-RELEASE_static-linux-0.0.1.artifactbundle.tar --checksum df0b40b9b582598e7e3d70c82ab503fd6fbfdff71fd17e7f1ab37115a0665b3b
```
3-2) Change includePath in Package.swift if Download Libraries Source Code.  
```
let includePath = "{Your Absolute Path}/Library/org.swift.swiftpm/swift-sdks/swift-6.1.2-RELEASE_static-linux-0.0.1.artifactbundle/swift-6.1.2-RELEASE_static-linux-0.0.1/swift-linux-musl/musl-1.2.5.sdk/x86_64/usr/include"
```
3-3) Switch Dependency Setting in Package.swift (Testy App and blocks library) if Download Libraries Source Code to Local.  
```
dependenciesSettings  
    .package(name: "overlayNetwork", path: "../overlayNetwork"),  //using local source code.  
    .package(name: "blocks", path: "../blocks"),  //using source code in same device.
```
4) Linuxアプリとしてクロスコンパイル  
```
$ cd ~/Documents/block\ chain/Testy
$ TOOLCHAINS=org.swift.612202505261a swift build -v --swift-sdk x86_64-swift-linux-musl --build-path ~/appOutput/Testy  
```
5) 実行ファイルをLinuxにコピー  
```
$ rsync -ahvz -C --perms --chmod=F0755,D2770 -e 'ssh -i {your key file} ' ~/appOutput/Testy/x86_64-swift-linux-musl/debug/TestyOnLinux {target user}@{target host name}:{target path}  
```
6) Linux Distributionごとにターゲット環境を構築  
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

## XcodeでiOSアプリとしてビルドする方法
### Swift Package (推奨)
1) XcodeでTestyプロジェクトまたはあなたのアプリを開きます。  
2) File - Add Packages
3) 右上のSearch or Enter Package URLに次のblocks URLを入力します。
https://github.com/webbananaunite/blocks
4) blocks libraryのREADME.mdが表示されます。
5) 右下のAdd Packageボタンをタップします。
6) TestyプロジェクトまたはあなたのアプリのプロジェクトのFrameworks, Libraries and Embeded Contentにblocks libraryがあることを確認します。 
7) TestyプロジェクトまたはあなたのアプリのプロジェクトのProject NavigatorのPackage Dependenciesにブロックチェーン・ライブラリ・スイート(blocks and overlayNetwork libraries)があることを確認します。
8) Xcodeでビルド、デバイスやシミュレータへのインストールを行います。  
9) アプリを起動し、"Join blocks Network"ボタンをタップすることで、稼働中のSignaling Serverとの通信を開始します。
10) OverlayNetwork Fingerテーブルの初期化が完了するまで5分ほど待ちます。（初回起動時のみ）  
### Carthage (0.3.0以降には対応していません。Swift Packageを使用してください。)
- $ cd your project directory
- $ echo 'github "webbananaunite/blocks" "carthage"' > Cartfile
- $ carthage update --use-xcframeworks
### CocoaPods (0.3.0以降には対応していません。Swift Packageを使用してください。)
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

## 制限事項
現在、公開アドレス上に公開されているブートノード(Boot Node)はインフラが貧弱なためブートノードはメモリ不足で停止する場合があります。  

## ライセンス
blocks & overlayNetwork & Testy は MIT Licenseで公開されています。  

無料で、あなたのアプリに組み込んで利用できます。  
いろんな目的のアプリに組み込み可能ですが、仮想通貨取引所で交換可能な暗号資産として使用することを禁止します。

## 禁止事項
仮想通貨取引所で交換可能な暗号資産として使用することを禁止します。

## その他説明
### Actors:
- Boot Node

Overlay Network (blocks P2P Network)で最初のノードです。

- Baby Sitter

あるノードが、OSI参照モデルのセッションレイヤーとしてのオーバーレイネットワークに参加する際には、最初に Baby Sitter NodeをbindサーバーのTXTレコードから見つけ、FSコマンドを送信する必要があります。
Codeプロトコルによる実装されるDHT（分散ハッシュテーブル）のエントリーごとにです。

- Taker

OSI参照モデルのプレゼンテーションレイヤー／アプリケーションレイヤーとして振る舞うblocksブロックチェーンのネットワークに参加するために、まず最初に行うことは、出生証明書を申請することです。
このネットワークには、管理者や管理ノードは存在しないため、Takerとなってくれるノードを見つける必要があります。
AT (Ask For Taker) 要求をトランザクションとしてネットワークに流すためです。

- Booker

Bookerとして振る舞うノードは、まだBookされていないトランザクションを収集し、プルーフオブワークによりノンスを計算し、ブロックをネットワークに流します。
ノンス値が正確な場合、最初のノードがBookerとなり、一時的にブロックチェーン管理者として振舞います。次回のプルーフオブワークまでの期間です。

### Things:
- Book

blocksブロックチェーンが記述されたもの。


### 言語:  
- Swift (Protocol Oriented)
- SwiftUI iOSのみ
- C++ (Metal) iOSのみ
- objc (DNS resolv) iOSのみ
- Python (Signaling)

### サードパーティライブラリの使用:
使用していません。しかし、他の著作物を含んでいます。
- QuadKey - Microsoft Corporation  
- SHA-512 - Aaron D. Gifford

### プログラミングアーキテクチャ:  
DDD, Onion Architecture (Protocol Oriented)

### バイトオーダー:  
- Distributed Hash Table (Finger table) address  
Little Endian

- nonce  
Little Endian

### cpu, gpu:
nonce の計算はcpuもしくはgpuを選択可能です。iOSのみ

## ステータス
Beta  
Advanced Featuresを除く、すべての機能が実装されました。

#### 未実装のAdvanced Features (20250318 16:53 JST Tokyo 現在):
- Blockの圧縮、Light Node
- Commandオペランドの圧縮
- Birth Transaction, BasicIncome Transactionの重複チェックの高速化
- ライブラリ利用ドキュメントの整備
- Beta Test
- 複数の Signaling Server の協調動作
