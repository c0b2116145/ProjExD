# 第1回
## 消えたアルファベットを探すゲーム（ex01/dalphabet.py）
### 遊び方
* コマンドラインでdalphabet.pyを実行すると，標準出力に問題が表示される．
* 欠損文字数を標準入力から答えを入力する．
* 正解なら「正解です。それでは、具体的に欠損文字を1つずつ入力してください」と表示される．
* 不正解なら「不正解です。またチャレンジしてください」と表示される．
*正解した場合、具体的に欠損文字を標準入力から答える.
* 欠損文字に不正解なら「不正解です。またチャレンジしてください」と表示される．
*欠損文字に正解したら「正解です。」と表示される.
* 挑戦回数は3回までで、全てに正解すれば終了.
### プログラム内䛾解説
* main関数：クイズプログラム䛾全体䛾流れを担当する．
* shutudai関数：対象文字列としてランダムに選んだアルファベットと表示文字列を表示する
* kaitou関数：回答と正解をチェックし，結果を出力する．

### To do
*文法エラーが出る
*時間の処理がまだ