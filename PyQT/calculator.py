import sys

from functools import partial
from operator import truediv, mul, add, sub
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from typing import Dict, List, Union, Optional, NoReturn, Json

from PyQt5.QtWidgets import (QApplication, 
                             QWidget,
                             QHBoxLayout,
                             QVBoxLayout,
                             QGridLayout,
                             QMainWindow,
                             QPushButton,
                             QLineEdit,
                             QListWidget,
                             QLabel,
                             QSizePolicy)


def percent(first, second=1):
    first = first * second
    return first

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs) -> NoReturn:
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Pyculator")
        self.setGeometry(100, 100, 280, 80)
        self.first_value: str = ''
        self.second_value: str = ''
        self.operation: str = ''
        self.temp1: str = ''
        self.temp: str = ''
        self.temp_operation: str = ''
        self.number_of_minus: int = 0
        self.dot: int = 0
        self.operations = {
                           '+':add,
                           '-':sub,
                           '*':mul,
                           '/':truediv,
                           '%':percent
                           }
        self.widget = QWidget()
        self.mainLayout = QHBoxLayout()
        self.mainSubLayout = QVBoxLayout()
        self._createDisplay()
        self._createButtons()
        self.mainSubLayout.addLayout(self.buttonLayout)
        self.mainLayout.addLayout(self.mainSubLayout)
        self.history = QListWidget()
        self.mainLayout.addWidget(self.history)
        self.widget.setLayout(self.mainLayout)
        self.setCentralWidget(self.widget)
        self.buttons_processing()

    def _createDisplay(self) -> NoReturn:
        self.display = QLineEdit('')
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.mainSubLayout.addWidget(self.display)

    def _createButtons(self) -> NoReturn:
        self.buttons: set = {}
        self.buttonLayout = QGridLayout()
        buttons: dict = [
            {
                'name':'C',
                'row':0,
                'col':4
            },
            {
                'name':'%',
                'row':2,
                'col':4,
            },
            {
                'name':'=',
                'row':3,
                'col':4,
            },
            {
                'name':'←',
                'row':1,
                'col':4
            },
            {
                'name':'1',
                'row':0,
                'col':0
            },
            {
                'name':'2',
                'row':0,
                'col':1
            },
            {
                'name':'3',
                'row':0,
                'col':2
            },
            {
                'name':'4',
                'row':1,
                'col':0
            },
            {
                'name':'5',
                'row':1,
                'col':1
            },
            {
                'name':'6',
                'row':1,
                'col':2
            },
            {
                'name':'7',
                'row':2,
                'col':0
            },
            {
                'name':'8',
                'row':2,
                'col':1
            },
            {
                'name':'9',
                'row':2,
                'col':2
            },
            {
                'name':'0',
                'row':3,
                'col':0,
                'colSpan': 2
            },
            {
                'name':'.',
                'row':3,
                'col':2
            },
            {
                'name':'+',
                'row':0,
                'col':3
            },
            {
                'name':'-',
                'row':1,
                'col':3
            },
            {
                'name':'*',
                'row':2,
                'col':3
            },
            {
                'name':'/',
                'row':3,
                'col':3
            },
        ]

        for buttonConfig in buttons:
            name: str = buttonConfig.get('name','')
            btn = QPushButton(name)
            font = QFont()
            font.setBold(True)
            btn.setFont(font)
            btn.setSizePolicy(QSizePolicy.Preferred, 
                              QSizePolicy.Expanding)
            self.buttons[name]: set = btn
            self.buttonLayout.addWidget(btn,
                                   buttonConfig['row'],
                                   buttonConfig['col'],
                                   buttonConfig.get('rowSpan',1),
                                   buttonConfig.get('colSpan',1))


    def change_text(self, text) -> None:
        if self.first_value != '' and self.operation == '':
            self.first_value = ''
            self.history.clear()
            self.temp = ''
            self.temp1 = ''
            self._clearDisplay()
            self.display.setText(self.display.text()+text)
            return
        self.display.setText(self.display.text() + text)

    def buttons_processing(self) -> NoReturn:
        for button_name in self.buttons:
            btn = self.buttons[button_name]
            if button_name in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                btn.clicked.connect(partial(self.change_text, button_name))
            elif button_name == 'C':
                btn.clicked.connect(self._clearAll)
            elif button_name == '←':
                btn.clicked.connect(self._remove)
            elif button_name == '+':
                btn.clicked.connect(self._additing)
            elif button_name == '=':
                btn.clicked.connect(self._ending)
            elif button_name == '-':
                btn.clicked.connect(self._substracting)
            elif button_name == '*':
                btn.clicked.connect(self._multiplication)
            elif button_name == '/':
                btn.clicked.connect(self._division)
            elif button_name == '%':
                btn.clicked.connect(self._percent)
            elif button_name == '.':
                btn.clicked.connect(self._dotting)                

    def _dotting(self) -> None:
        value = self.displayText()
        if '.' in value:
            return
        else:
            self.display.setText(self.display.text() + ".")

    def int_or_float(self, num) -> Union[int, float]:
            num = float(num)
            if num.is_integer():
                return int(num)
            return num

    def input_processing(self) -> Optional[bool]:
        value = self.displayText()

        if value == '':
            return True

        if self.first_value == '':
            self.first_value = value
            self.history.addItem(value)
            self.number_of_minus = 0
            self._clearDisplay()
            return

        if self.first_value != '':
            if self.second_value == '' and self.operation != '':
                self.second_value = value
                self.history.addItem(self.displayText())
                self._clearDisplay()
                self.number_of_minus = 0
                return

    def setDisplayText(self, text='') -> NoReturn:
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self) -> str:
        return self.display.text()

    def _clearDisplay(self) -> NoReturn:
        self.setDisplayText()

    def _clearAll(self) -> NoReturn:
        self.first_value = ''
        self.second_value = ''
        self.operation = ''
        self.result = ''
        self.temp1 = ''
        self.temp = ''
        self.history.clear()
        self._clearDisplay()
        self.temp_operation = ''
        self.number_of_minus = 0
        self.dot = 0

    def _remove(self) -> NoReturn:
        value = self.displayText()

        if len(value) == 0:
            self.setDisplayText("")
        else:
            value = value[:-1]
            self.display.setText(value)


    def _ending(self) -> None:
        self.input_processing()
        if self.operation == '%' and self.first_value != '' and self.second_value == '':
            return
        if self.second_value == '' and self.operation == '':
            for symbol in self.operations:
                if symbol == self.temp_operation:
                    self.temp1 = self.first_value
                    self.first_value = self.operations[self.temp_operation](self.int_or_float(self.first_value), self.int_or_float(self.temp))
                    self.setDisplayText(str(self.first_value))
                    self.history.addItem(f"{str(self.temp1)} {self.temp_operation} {str(self.temp)} = {str(self.int_or_float(self.first_value))}")
                    return
        for symbol in self.operations:
            if symbol == self.operation:
                self.temp1 = self.first_value
                try:
                    self.first_value = self.operations[self.operation](self.int_or_float(self.first_value), self.int_or_float(self.second_value))
                except ZeroDivisionError:
                    self._clearAll()
                    self.history.addItem("Zero Division Error")
                    return

        self.history.clear()
        self.history.addItem(f"{str(self.temp1)} {self.operation} {str(self.second_value)} = {str(self.int_or_float(self.first_value))}")
        self.temp = self.second_value
        self.temp_operation = self.operation
        self.operation = ''
        self.second_value = ''
        self.setDisplayText(str(self.first_value))


    def _additing(self) -> None:
        self.input_processing()
        if self.first_value == '':
            return
        if self.first_value != '' and self.second_value == '':
            self.operation = '+'
            self.history.addItem('+')
            self._clearDisplay()
            return
        if self.second_value != '':
            self.first_value = self.int_or_float(self.first_value)
            self.second_value = self.int_or_float(self.second_value)
            self.temp = self.second_value
            self.temp1 = self.first_value
            self.first_value = self.first_value + self.second_value
            self.second_value = '' 
            return

    def _percent(self) -> None:
        self.input_processing()
        if self.first_value == '':
            return
        if self.second_value == '':
            self.operation = '%'
            self.first_value = self.int_or_float(self.first_value)/100
            self.history.addItem(str(self.first_value))
            return
        if self.second_value != '':
            self.first_value = self.int_or_float(self.first_value)*self.int_or_float(self.second_value)
            self.history.addItem(str(self.first_value))
            self.second_value = ''
            return

    def _multiplication(self) -> None:
        self.input_processing()
        if self.first_value == '':
            return
        if self.first_value != '' and self.second_value == '':
            self.operation = '*'
            self.history.addItem('*')
            self._clearDisplay()
            return
        if self.second_value != '':
            self.first_value = self.int_or_float(self.first_value)
            self.second_value = self.int_or_float(self.second_value)
            self.temp = self.second_value
            self.temp1 = self.first_value
            self.first_value = self.first_value * self.second_value
            self.second_value = ''
            return


    def _substracting(self) -> None:
        self.input_processing()
        if self.operation == '/' and self.second_value == 0:
            self._clearAll()
            self.history.addItem("Zero Division Error")
            return
        if self.first_value == '':
            self.number_of_minus += 1
            self.setDisplayText('-')
        if self.first_value != '' and self.operation == '':
            self.operation = '-'
            self._clearDisplay()
            self.history.addItem('-')
            self.number_of_minus = 0
            return
        if self.operation != '' and self.number_of_minus == 0:
            self.number_of_minus += 1
            self.setDisplayText('-')
            return
        if self.first_value != '':    
            self.history.addItem(self.operation)
            self.number_of_minus = 0
            return
        if self.first_value !='' and self.second_value !='':
            self.first_value = self.int_or_float(self.first_value)
            self.second_value = self.int_or_float(self.second_value)
            self.temp1 = self.first_value
            self.first_value = self.int_or_float(self.first_value) - self.int_or_float(self.second_value)
            self.history.addItem('=')
            self.history.addItem(str(self.int_or_float(self.first_value)))
            self.history.addItem(self.operation)
            return

    def _division(self) -> None:
        self.input_processing()
        if self.first_value == '':
            return
        if self.first_value != '' and self.second_value == '':
            self.operation = '/'
            self.history.addItem('/')
            self._clearDisplay()
            return
        if self.second_value != '':
            self.first_value = self.int_or_float(self.first_value)
            self.second_value = self.int_or_float(self.second_value)
            self.temp = self.second_value
            self.temp1 = self.first_value
            try:
                self.first_value = self.first_value / self.second_value
            except ZeroDivisionError:
                self._clearAll()
                self.history.addItem("Zero Division Error")
                return
            return

def main_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
        main_window()
        