# BlockChain Library Suite

## blocks について
blocks は中本智さんの論文に基づいて開発されたiOSライブラリです。
あなたのアプリにブロックチェーンを導入できます。

いろんな目的に使用できますが、仮想通貨取引所で交換可能な暗号資産として使用することを禁止します。

このブロックチェーン・ライブラリが特徴的なのは、政府・公共・民間の社会システムにおける活動をあらかじめ組み込まれていることです。（出生証明、住民票、身元保証など）

添付の overlayNetwork ライブラリに依存します。

## overlayNetwork について
overlayNetwork は、Peer-to-Peerオーバーレイ・ネットワーク通信システムです。
MIT Laboratoryの分散ハッシュテーブルの実装である Chord 論文に基づいて開発されたものです。

他のライブラリに依存しません。

## Testy について
Testy は住民基本台帳カードの代替として開発されています。

blocksライブラリとoverlayNetworkライブラリの使用参考例として作成されたものです。

## Signaling について
Signalingはオーバーレイネットワークにおいて、NATトラバーサルを用い、オーバーレイネットワークアドレスをIP/ポートに変換することで、ノード間の通信をコーディネートします。
Signalingはクラウド上で動作し、ノードの要求に応じ、通信調整を行います。
Signalingはオーバーレイネットワークにおいて、NAT越えを実現します。

## download

blocks - ブロックチェーン・ライブラリβ版  
[ダウンロード](https://github.com/webbananaunite/blocks)  
https://github.com/webbananaunite/blocks  
 
overlayNetwork - peer-to-peer分散ハッシュテーブル通信ライブラリβ版  
[ダウンロード](https://github.com/webbananaunite/overlayNetwork)  
https://github.com/webbananaunite/overlayNetwork  
 
Testy - 住民基本台帳アプリβ版  
[ダウンロード](https://github.com/webbananaunite/Testy)  
https://github.com/webbananaunite/Testy  
 
Signaling - オーバーレイネットワークアドレスをIP/ポートに変換β版  
[ダウンロード](https://github.com/webbananaunite/Signaling)  
https://github.com/webbananaunite/Signaling  

## ライブラリ利用方法
### Swift Package (推奨)
1) XcodeでTestyプロジェクトまたはあなたのアプリを開きます。  
2) File - Add Packages
3) 右上のSearch or Enter Package URLに次のblocks URLを入力します。
https://github.com/webbananaunite/blocks
4) blocks libraryのREADME.mdが表示されます。
5) 右下のAdd Packageボタンをタップします。
6) TestyプロジェクトまたはあなたのアプリのプロジェクトのFrameworks, Libraries and Embeded Contentにblocks libraryがあることを確認します。 
7) TestyプロジェクトまたはあなたのアプリのプロジェクトのProject NavigatorのPackage Dependenciesにブロックチェーン・ライブラリ・スイート(blocks and overlayNetwork libraries)があることを確認します。
8) 最初の一台は、ブートノードとして起動する必要があります。
アプリをブートノードとして起動するためには、XcodeのEdit Scheme から RunAsBootNode という名称で Run Argument / Environment Variable のどちらかを設定します。
9) Xcodeでビルド、デバイスやシミュレータへのインストールを行います。  
10) アプリを起動し、"Join blocks Network"ボタンをタップすることで、稼働中のSignaling Serverとの通信を開始します。
11) DHCテーブルの初期化が完了するまで8分ほど待ちます。（初回起動時のみ）  
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
ブートノードを公開アドレス上に作成できていないため、ベータ版を動作させるには、最初のNodeをブートノードとして起動する必要があります。  
Signaling Serverはクラウド上において、運用実施中です。

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

- Book

blocksブロックチェーンが記述されたもの。

- Booker

Bookerとして振る舞うノードは、まだBookされていないトランザクションを収集し、プルーフオブワークによりノンスを計算し、ブロックをネットワークに流します。
ノンス値が正確な場合、最初のノードがBookerとなり、一時的にブロックチェーン管理者として振舞います。次回のプルーフオブワークまでの期間です。

### 言語:  
- SwiftUI (Protocol Oriented) 
- C++ (Metal) 
- objc (DNS resolv)
- Python (Signaling)

### サードパーティライブラリの使用:
使用していません。しかし、他の著作物を含んでいます。
- QuadKey - Microsoft Corporation  
- SHA-512 - Aaron D. Gifford

### プログラミングアーキテクチャ:  
around DDD, Onion (Protocol Oriented)

### バイトオーダー:  
- Distributed Hash Table (Finger table) address  
Little Endian

- nonce  
Little Endian

### cpu, gpu:
nonce の計算はcpuもしくはgpuを選択可能です。

## ステータス
Beta  
Advanced Featuresを除く、すべての機能が実装されました。

#### 未実装のAdvanced Features (20240709 13:33 JST Tokyo 現在):
- Blockの圧縮、Light Node
- Commandオペランドの圧縮
- Birth Transaction、BasicIncome Transactionの重複チェックの高速化
- イレギュラー発生時の手続き
- ライブラリ利用ドキュメントの整備
- Boot NodeをCloud (linux)に作成し稼働させる
- Beta Test
- 複数の Signaling Server の協調動作

#### Join us!:
Peer-to-Peerオーバーレイ・ネットワークと、ブロックチェーンでの社会基盤構築に賛同していただける方、ボランティアになりますが、共に開発に貢献してくれる方やテストに参加してくれる方を募っています。  

ただし、仮想通貨取引所関係の方はお断りさせていただいておりますことをご了承ください。  

ともに未来を作りましょう。ご連絡をお待ちしています。  
