#! /usr/bin/sh
# sh run_svm.sh kenketsu 100

TOPIC=$1
DIM=$2 # LSAによる圧縮次元数

for i in `seq 1 10`
do

FILE=/home/ishitsuka/enjo/data/output/test/${TOPIC}/${DIM}/train_${i}

# 欠損値処理+ランダムサンプリング
# 出力ファイル: $FILE.sampled
# pandasのdropnaの動作がおかしいのでRで処理
# /home/ishitsuka/vir/bin/python /home/ishitsuka/enjo/program/model/maeshori.py $FILE

# LSAによる次元圧縮
# 出力ファイル: $FILE.svd
python /home/ishitsuka/enjo/program/model/svds.py $FILE $DIM

# CSVファイルをLIBSVMファイルに変換
# 出力ファイル: $FILE.lib
python /home/ishitsuka/enjo/phraug/csv2libsvm.py ${FILE}.svd ${FILE}.lib 0 0

# 特徴量のスケーリング
# 出力ファイル: $FILE.scale
/home/ishitsuka/enjo/libsvm/svm-scale -l 0 ${FILE}.lib > ${FILE}.scale

# グリッドサーチ
# カーネルはRBFが精度よい
python /home/ishitsuka/enjo/libsvm/tools/grid.py ${FILE}.scale > ${FILE}.rbf
# python /home/ishitsuka/enjo/libsvm/tools/grid.py -t 0 ${FILE}.scale > ${FILE}.linear
# python /home/ishitsuka/enjo/libsvm/tools/grid.py -t 1 ${FILE}.scale > ${FILE}.poly
# python /home/ishitsuka/enjo/libsvm/tools/grid.py -t 3 ${FILE}.scale > ${FILE}.sigmoid

done
