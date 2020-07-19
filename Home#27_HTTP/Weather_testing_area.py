import requests
import json
import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtCore, QtWidgets
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
                             QSizePolicy,
                             QComboBox)

# for item in resource.json().keys():
#     if item == 'weather':
#         print(f"Weather condition: {resource.json()[item][0]['main']}")
#         print(f"Condition description: {resource.json()[item][0]['description']}")
#     if item == 'main':
#         print(f"Temperature: {resource.json()[item]['temp']}")
#         print(f"Feels like: {resource.json()[item]['feels_like']}")
#         print(f"Min temperature: {resource.json()[item]['temp_min']}")
#         print(f"Max temperature: {resource.json()[item]['temp_max']}")
#         print(f"Pressure: {resource.json()[item]['pressure']}")
#         print(f" Humidity: {resource.json()[item]['humidity']}")
#     if item == 'wind':
#         print("Wind:")
#         print(f"\tSpeed: {resource.json()[item]['speed']}")
#         print(f"\tDegree: {resource.json()[item]['deg']}")
#     if item == 'sys':
#         print(f"Sunrise: {resource.json()[item]['sunrise']}")
#         print(f"Sunset: {resource.json()[item]['sunset']}")

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.number_of_days = 1
        self.setWindowTitle("Weather App")
        self.setFixedSize(500, 150)
        self.resource = ''
        # self.widget = QWidget()
        # self.setCentralWidget(self.widget)
        # self.mainLayout = QVBoxLayout()
        # self._display()
        # self.widget.setLayout(self.mainLayout)

    # def _display(self):
        self.display = QLineEdit(self)
        self.OkButton = QPushButton('OK', self)
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('CITY: ')
        self.combo = QComboBox(self)
        self.combo.addItems(["Today","5 Days"])
        self.combo.move(80, 70)
        self.combo.resize(250,32)
        self.OkButton.resize(50, 32)
        self.display.resize(250, 30)
        self.nameLabel.move(30, 20)
        self.display.move(80, 20)
        self.OkButton.move(350, 20)
        self.display.setStyleSheet("color: blue;"
                        "background-color: yellow;"
                        "selection-color: yellow;"
                        "selection-background-color: blue;")
        # self.mainLayout.addWidget(self.display)
        self.OkButton.clicked.connect(self._clickMethod)
        self.combo.activated[str].connect(self.options) 
    
    def options(self, value):
        if value == '5 Days':
            self.number_of_days = 5
        else:
            self.number_of_days = 1

    def _add_QLabels(self):
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.mainLayout = QHBoxLayout()
        self._vertical_layout = QVBoxLayout()
        self.mainLayout.addLayout(self._vertical_layout)
        self.setLayout(self.mainLayout)
        self.setFixedSize(500, 500)
        self.mainLayout = QHBoxLayout()
        self.weather = QLabel()
        self.weather.setText("Weather")
        self.weather_main = QLabel()
        self.weather_wind = QLabel()
        self.weather_sun = QLabel()

    def _clickMethod(self):
        if self.number_of_days == 1:
            city = self.display.text()
            city = 'Rivne'
            resource = requests.get('http://api.openweathermap.org/data/2.5/weather?', {'q':city, 'appid':'a5c5f26e7e133daa411606be2347d43c', 'lang':'ua'})
            print(resource.json())
            self._add_QLabels()
            for item in resource.json().keys():
                if item == 'weather':
                    self.weather.setText(f"Weather condition: {resource.json()[item][0]['main']}")
                #     print(f"Condition description: {resource.json()[item][0]['description']}")
                # if item == 'main':
                #     print(f"Temperature: {resource.json()[item]['temp']}")
                #     print(f"Feels like: {resource.json()[item]['feels_like']}")
                #     print(f"Min temperature: {resource.json()[item]['temp_min']}")
                #     print(f"Max temperature: {resource.json()[item]['temp_max']}")
                #     print(f"Pressure: {resource.json()[item]['pressure']}")
                #     print(f" Humidity: {resource.json()[item]['humidity']}")
                # if item == 'wind':
                #     print("Wind:")
                #     print(f"\tSpeed: {resource.json()[item]['speed']}")
                #     print(f"\tDegree: {resource.json()[item]['deg']}")
                # if item == 'sys':
                #     print(f"Sunrise: {resource.json()[item]['sunrise']}")
                #     print(f"Sunset: {resource.json()[item]['sunset']}")


        else:    
            city = self.display.text()
            city = 'Rivne'
            self.resource = requests.get('http://api.openweathermap.org/data/2.5/forecast?', {'q':city, 'appid':'a5c5f26e7e133daa411606be2347d43c', 'lang':'ua'})
            self.setFixedSize(500, 500)
            print(self.resource.json())

def main_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main_window()        