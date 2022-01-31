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
        if word in self.word_list:
            return True
        else:
            return False

    def is_word_collect(self, word: str):
        """
        5文字の単語が答えに合っていればTrue
        """
        if word == self.answer:
            return True
        else:
            return False

    def is_char_in_answer(self, char: str):
        """
        英語一文字が答えに含まれていたらTrue
        """
        if char in self.answer:
            return True
        else:
            return False

    def is_char_right_position(self, char: str, pos: int):
        """
        英語一文字が答えと照らし合わせて位置が合っていたらTrue
        """
        if self.answer[pos] == char:
            return True
        else:
            return False
