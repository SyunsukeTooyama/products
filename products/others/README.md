# wavefunc.py
無限井戸型ポテンシャルの定常状態の波動関数のアニメーションを表示するプログラムです。

## 環境
+ python
  + matplotlib

## GIF

![wavefunc](https://github.com/SyunsukeTooyama/products/assets/138125489/8ac989af-4ed5-4820-80dd-9cabb32ce0c3)

# percolation.c
パーコレーションとは
このソースコードも公開していません。メールでGoogleDriveの限定公開URLを共有します。

## 環境
+ C言語
  + gnuplot

## デモ
![スクリーンショット 2023-12-03 131912](https://github.com/SyunsukeTooyama/products/assets/138125489/ac8aa77b-a301-4a34-bb98-6225f9a4c11b)

grid size n = 400
probability = 0.7

サイズはメモリの関係か400ぐらいが限界です。

## 使用方法
`percolation.c`をコンパイルして実行するとターミナルに
```terminal
Input seed of random number

input grid size n

Input probability

```
という文が表示されるのでそれぞれお好きな数字を入力するとgnuplotのウィンドウが現れ、パーコレートしている場合はその道筋が色付きで表示されます。また、ターミナルに横方向では`horizontal percolation!!`、縦方向では`vertical percolation!!`と表示されます。
