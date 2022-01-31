"""GUIの見た目を定義するファイル"""

import PySimpleGUI as sg


class Widget:
    """widgetを定義"""

    """スタイル"""

    # relief style
    relief_size = (30, 1)
    relief_font = ("Helvetica", 15)
    relief_text = "PysimpleGUI Wordle!"

    # input box style
    input_box_color = 'black'
    input_box_color_bg = 'white'
    input_box_size = (4, 1)

    # keyboard button style
    keyboard_btn_size = (4, 1)
    keyboard_btn_color = ('#FFFFFF', '#283b5b')

    # active row mark style
    active_row_mark_text = "●"
    active_row_mark_size = (4, 1)
    active_row_mark_font = ('', 10)

    # window style
    window_title = 'PySimpleGui Wordle'
    window_size = (800, 500)

    def widget_relief(self):
        """リリーフ"""
        return sg.T(text=self.relief_text,
                    size=self.relief_size,
                    justification='center',
                    font=self.relief_font,
                    relief=sg.RELIEF_RIDGE)

    def widget_active_row_mark(self, color: str, key: str):
        """現在の入力行を示すマーク"""
        return sg.T(text=self.active_row_mark_text,
                    size=self.active_row_mark_size,
                    text_color=color,
                    font=self.active_row_mark_font,
                    key=key)

    def widget_input_box(self, key: str, disabled: bool):
        """input box widget"""
        return sg.InputText('',
                            key=key,
                            size=self.input_box_size,
                            disabled=disabled,
                            text_color=self.input_box_color,
                            justification='c',
                            background_color=self.input_box_color_bg,
                            enable_events=True)

    def widget_keyboard_button(self, char: str, key: str):
        """キーボードボタンwidget"""
        return sg.Button(char,
                         key=key,
                         size=self.keyboard_btn_size,
                         button_color=self.keyboard_btn_color)

    @staticmethod
    def popup_does_not_exist(word: str):
        """単語リストにありませんpopup"""
        sg.popup(f'Sorry, "{word}" does not exist in my word list')

    @staticmethod
    def popup_game_over(answer: str):
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
        layout = []

        for row in range(1, 7):
            disabled = False if row == 1 else True
            color_mark = 'green' if row == 1 else 'white'
            active_row_mark = self.widget_active_row_mark(color=color_mark,
                                                          key=f'row{row}')

            widgets = [active_row_mark]
            for col in range(1, 6):
                # keyはr1c1形式で記入
                key = f'r{row}c{col}'
                widget = self.widget_input_box(key=key, disabled=disabled)
                widgets.append(widget)

            layout.append(widgets)

        layout = sg.Column(layout=layout, justification='c')

        return layout

    def key_boards_widgets(self):
        """キーボードボタン"""
        layout = []
        keyboards = ['QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM']
        for chars in keyboards:
            widgets = []
            for char in list(chars):
                widget = self.widget_keyboard_button(char=char, key=char)
                widgets.append(widget)
            widgets = sg.Column(layout=[widgets], justification='c')
            layout.append([widgets])

        return layout

    def layout(self):
        """レイアウトを返す"""

        col_relief = sg.Column([[self.widget_relief()]], justification='c')

        col_control = sg.Column(layout=[[sg.Button('ENTER'),
                                         sg.Button('BACK'),
                                         sg.Button('PREV'),
                                         sg.Button('NEXT'),
                                         sg.Button('CLEAR')]],
                                justification='c')
        layout = [[col_relief],
                  [self.input_box_widgets()],
                  [self.key_boards_widgets()],
                  [col_control]]

        return layout

    def window(self):
        """ウィンドウを返す"""
        window = sg.Window(title=self.window_title,
                           layout=self.layout(),
                           size=self.window_size,
                           finalize=True)
        return window
