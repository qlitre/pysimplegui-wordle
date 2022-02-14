"""Wordleのロジックを定義するファイル"""

import random


class Wordle:
    """Wordleのロジック"""

    def __init__(self, word_list: list):
        self.word_list = word_list
        self.answer = None

    def set_answer(self):
        """answerをセットする"""
        max_index = len(self.word_list)
        index = random.randrange(start=0, stop=max_index)
        self.answer = self.word_list[index]

    def is_word_in_word_list(self, word: str):
        """単語がword listの中に存在していたらTrue"""
        return word in self.word_list

    def is_word_collect(self, word: str):
        """
        5文字の単語が答えに合っていればTrue
        """
        return word == self.answer

    @staticmethod
    def dict_with_position(word):
        d = {}
        for pos, c in enumerate(word, 1):
            d[pos] = c
        return d

    def get_hint(self, guess):
        """
        入力値からヒントを返す
        本家に合わせて、
        答え ULTRA
        入力 MAMMA
        というような場合に2文字目のAを灰色にするように変更
        TODO もっといいやり方
        """
        # {1:char,2:char...}という辞書を作る
        answer = self.dict_with_position(self.answer)
        guess = self.dict_with_position(guess)

        hint = []

        # 緑を確認
        for pos, char in guess.items():
            if answer[pos] == char:
                hint.append({'pos': pos, 'char': char, 'hint': 'green'})

                # ヒットしたら答えと入力を空文字にする
                answer[pos] = ''
                guess[pos] = ''

        # 黄色を確認
        for pos, char in guess.items():
            if not char:
                continue
            if char in answer.values():
                hint.append({'pos': pos, 'char': char, 'hint': 'orange'})
                # 同じく空文字にする
                guess[pos] = ''
                for k, v in answer.items():
                    if v == char:
                        answer[k] = ''

        # 残ったのは灰色
        for pos, char in guess.items():
            if not char:
                continue
            hint.append({'pos': pos, 'char': char, 'hint': 'gray'})

        hint.sort(key=lambda x: x['pos'])
        return hint
