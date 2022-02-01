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

    def is_char_in_answer(self, char: str):
        """
        英語一文字が答えに含まれていたらTrue
        """
        return char in self.answer

    def is_char_right_position(self, char: str, pos: int):
        """
        英語一文字が答えと照らし合わせて位置が合っていたらTrue
        """
        return self.answer[pos] == char
