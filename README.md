# pysimplegui-wordle
PySimpleGUIでWordleが遊べるアプリです。

# 始め方

git cloneします。

```
git clone https://github.com/qlitre/pysimplegui-wordle/
```

仮想環境を作成してライブラリをインストールします。

```
cd pysimplegui-wordle
python -m venv myvenv
myvenv\scripts\activate
pip install -r requirements.txt
```

後はgampe.pyを起動します。

```
game.py
```

# 遊び方
ゲームが始まるとwords.pyからランダムで答えの英単語がセットされます。

キーボードボタンから５文字の単語を入力していきます。

![image](https://user-images.githubusercontent.com/77523162/151696947-5b517fef-970e-46b4-a64e-b2f4aad68bb8.png)

入力が終わったらEnterを押しましょう。

![image](https://user-images.githubusercontent.com/77523162/151696970-3e37c2a6-3013-45c8-9718-f8f434f3582f.png)

- 緑色    → 入力位置と文字が正解とあっている
- オレンジ→ 文字は正解の中に含まれているが、位置が合っていない
- 灰色    → 全く正解の中に含まれていない

![image](https://user-images.githubusercontent.com/77523162/151697036-e47090ee-16ac-4e49-b713-172fea86bcc1.png)

入力された単語が単語リストになかったら次に進めません。

![image](https://user-images.githubusercontent.com/77523162/151696996-0aa85b89-a473-48a8-9ce4-3f23a69e0d86.png)

6ターン過ぎて正解できなかったらゲームオーバーです。
正解が発表されてもう一回やるか聞かれます。

![image](https://user-images.githubusercontent.com/77523162/151697088-b3b3f878-c3a0-4e71-b1e3-efa845e27bc5.png)

正解したらおめでとうポップアップが出ます。