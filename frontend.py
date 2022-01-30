"""GUIの見た目を定義するファイル"""

import PySimpleGUI as sg


class Widget:
    """widgetを定義"""

    def __init__(self):
        self.size_input_box = (4, 1)
        self.size_keyboard_button = (4, 1)
        self.size_active_row_mark = (4, 1)
        self.size_window = (800, 500)
        self.color_input = 'black'
        self.color_input_background = 'white'
        self.color_keyboard = ('#FFFFFF', '#283b5b')
        self.window_title = 'PySimpleGui Wordle'
        self.font_active_row_mark = ('', 10)

    def widget_active_row_mark(self, color: str, key: str):
        """現在の入力行を示すマーク"""
        return sg.T('●',
                    size=self.size_active_row_mark,
                    text_color=color,
                    font=self.font_active_row_mark,
                    key=key)

    def widget_input_box(self, key: str, disabled: bool):
        """input widget"""
        return sg.InputText('',
                            key=key,
                            size=self.size_input_box,
                            disabled=disabled,
                            text_color=self.color_input,
                            justification='c',
                            background_color=self.color_input_background)

    def widget_keyboard_button(self, char: str, key: str):
        """キーボードボタンwidget"""
        return sg.Button(char,
                         key=key,
                         size=self.size_keyboard_button,
                         button_color=self.color_keyboard)

    @staticmethod
    def popup_does_not_exist(word: str):
        """単語リストにありませんpopup"""
        sg.popup(f'Sorry, "{word}" does not exist in my word list')

    @staticmethod
    def popup_game_over(answer):
        """ゲームオーバーpopup"""
        msg = f'Game Over!\nThe answer is {answer}\nDo it again?'
        return sg.popup_ok_cancel(msg)

    @staticmethod
    def popup_congratulation():
        """ゲームクリアpopup"""
        msg = 'Congratulation!\nDo it again?'
        return sg.popup_ok_cancel(msg)

    @staticmethod
    def popup_see_you_later():
        """see you later popup"""
        return sg.popup('See you later')


class GuiFrontEnd(Widget):
    """GUIの見た目を定義"""

    def input_box_widgets(self):
        """縦6 x 横5の入力マス"""
        widgets = []

        for row_num in range(1, 7):
            disabled = False if row_num == 1 else True
            color_mark = 'green' if row_num == 1 else 'white'
            active_row_mark = self.widget_active_row_mark(color=color_mark, key=f'row{row_num}')

            row = [active_row_mark]
            for col_num in range(1, 6):
                # keyはr1c1形式で記入
                key = f'r{row_num}c{col_num}'
                widget = self.widget_input_box(key=key, disabled=disabled)
                row.append(widget)

            widgets.append(row)
        widgets = sg.Column(layout=widgets, justification='c')

        return widgets

    def key_boards_widgets(self):
        """キーボードボタン"""
        widgets = []
        keyboards = ['QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM']
        for chars in keyboards:
            row = []
            for char in list(chars):
                widget = self.widget_keyboard_button(char=char, key=char)
                row.append(widget)
            row = sg.Column(layout=[row], justification='c')
            widgets.append([row])

        return widgets

    def layout(self):
        """レイアウトを返す"""
        col_control = sg.Column(layout=[[sg.Button('ENTER'),
                                         sg.Button('BACK'),
                                         sg.Button('PREV'),
                                         sg.Button('NEXT')]],
                                justification='c')
        layout = [[self.input_box_widgets()],
                  [self.key_boards_widgets()],
                  [col_control]]

        return layout

    def window(self):
        """ウィンドウを返す"""
        window = sg.Window(title=self.window_title,
                           layout=self.layout(),
                           size=self.size_window,
                           finalize=True)
        return window
