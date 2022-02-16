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

    def is_word_in_word_list(self, guess: str):
        """単語がword listの中に存在していたらTrue"""
        return guess in self.word_list

    def is_word_collect(self, guess: str):
        """
        5文字の単語が答えに合っていればTrue
        """
        return guess == self.answer

    @staticmethod
    def dict_with_position(guess: str):
        d = {}
        for pos, c in enumerate(guess, 1):
            d[pos] = c
        return d

    def get_hint(self, guess_w_pos):
        """
        入力値からヒントを返す
        本家に合わせて、
        答え ULTRA
        入力 MAMMA
        というような場合に2文字目のAを灰色にするように変更
        TODO もっといいやり方
        """
        # {1:char,2:char...}という辞書を作る
        answer_w_pos = self.dict_with_position(self.answer)
        guess_w_pos = self.dict_with_position(guess_w_pos)

        hints = []

        # 緑を確認
        for pos, char in guess_w_pos.items():
            if answer_w_pos[pos] == char:
                hints.append({'pos': pos, 'char': char, 'hint': 'green'})

                # ヒットしたら答えと入力を空文字にする
                answer_w_pos[pos] = ''
                guess_w_pos[pos] = ''

        # 黄色を確認
        for pos, char in guess_w_pos.items():
            if not char:
                continue
            if char in answer_w_pos.values():
                hints.append({'pos': pos, 'char': char, 'hint': 'orange'})
                # 同じく空文字にする
                guess_w_pos[pos] = ''
                for k, v in answer_w_pos.items():
                    if v == char:
                        answer_w_pos[k] = ''
                        break

        # 残ったのは灰色
        for pos, char in guess_w_pos.items():
            if not char:
                continue
            hints.append({'pos': pos, 'char': char, 'hint': 'gray'})

        hints.sort(key=lambda x: x['pos'])
        return hints
