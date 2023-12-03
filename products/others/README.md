# wavefunc.py
無限井戸型ポテンシャルの定常状態の波動関数のアニメーションを表示するプログラムです。
授業で習った量子力学の式で表される状態が、どのように時間発展するのか興味がわいたため自習していたPythonを用いて可視化してみました。

## 環境
+ python
  + matplotlib

## GIF
![wavefunc](https://github.com/SyunsukeTooyama/products/assets/138125489/8ac989af-4ed5-4820-80dd-9cabb32ce0c3)

## 導出
１次元Schrödinger方程式
```math
iℏ\frac{\partial}{\partial t}\psi=-\frac{ℏ^2}{2m}\frac{\partial^2}{\partial x^2}\psi
```
定常状態では
$\psi (x,t)=\phi (x)\chi (t)$
として
```math
E\phi=-\frac{ℏ^2}{2m}\frac{\partial^2}{\partial x^2}\phi
```
$(A,B=Const.)$

$k=\frac{\sqrt{2mE}}{ℏ}$として

```math
\phi=Acos(kx)+Bsin(kx)
```

境界条件
$\phi(x=0,x=L)=0$
、規格化
$\int^\infty_{-\infty} \phi^* \phi dx=1$
を考えて
```math
\phi=\frac{1}{\sqrt{L}}sin(\frac{n\pi}{L}x)
```
$(nは自然数)$

よって
$k=\frac{\sqrt{2mE}}{ℏ}=\frac{n\pi}{L}$
より
```math
E=\frac{n^2ℏ^2\pi^2}{2mL^2}
```
また時間部分は
```math
iℏ\frac{\partial}{\partial t}\chi=E\chi
```
より
```math
\chi=\chi (0)e^{-i\frac{E}{ℏ}t}
```
$(簡略化のため\chi(0)=0とする)$

よって

```math
\psi=\frac{1}{\sqrt{L}}e^{-i\frac{E}{ℏ}t} sin(\frac{n\pi}{L}x)
```
これを見やすいように位置をずらしながら下から
$n=0,1,2,3,4,5$
について振幅を調整して表示するようにしました。

# percolation.c
パーコレーション判別プログラムとは、あるサイズの格子点上にある確率に沿って点を打ち、左右または上下に点が離接している点をつないでいったときに、設定したサイズの左右または上下にひとつながりに点が結べたときパーコレートしていると判別します。

**このソースコードも公開していません。メールでGoogleDriveの限定公開URLを共有します。**

## 環境
+ C言語
  + gnuplot

## デモ
![スクリーンショット 2023-12-03 131912](https://github.com/SyunsukeTooyama/products/assets/138125489/ac8aa77b-a301-4a34-bb98-6225f9a4c11b)

grid size n = 400, probability = 0.7

サイズはメモリの関係か400くらいが限界です。

## 使用方法
`percolation.c`をコンパイルして実行するとターミナルに
```terminal
Input seed of random number //シード値の設定（なんでも良い整数値）
input grid size n //一辺当たりの格子点の数（任意の自然数値<=400くらい）
Input probability //点を打つ確率（任意の浮動小数点値　0.6付近が閾値）
```
という文が表示されるのでそれぞれ任意の数字を入力するとgnuplotのウィンドウが現れ、パーコレートしている場合はその道筋が色付きで表示されます。また、ターミナルに横方向では`horizontal percolation!!`、縦方向では`vertical percolation!!`と表示されます。

パーコレートしていない場合は線が引かれずターミナルにも表示されません。

パーコレートする閾値は大体0.6あたりで、方法として全通りを試すプログラムのため、probabilityが0.6付近では処理に時間がかかります。

## 改善点
+ サイズが４００くらいが限界なのですが、うまくコードを書けばもう少しメモリを節約できそうな気がします。
  + 例えばオセロで用いたビットボードの方法が使えそう
    
+ 表示される線は最短距離ではないこと
  + 最短距離を求めようとすると確実にすべてのパーコレートする通りを求めねばならず、処理が重くなることを考えて一つ見つかった時点で`break`するようにしました。
  
## 総括
　全通りの道順を考えるために、分岐している道をすべて考えなければならず一度通過した分岐先などを除外する処理を書くことが大変でした。
合流や分岐や行き止まり、縦方向と横方向の判定の競合など様々な可能性を考えたり、実際に実行したりして現れた問題にそれぞれに対処するようにコードを修正するのは大変骨の折れる作業でしたが、修正しきった時の達成感や現場でのバグ修正をイメージできてよい経験だったと感じています。
