import json
import urllib
import requests
import psycopg2
import os.path
import sys

from os import path
from typing import Dict, List, Union, Optional, NoReturn
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QHBoxLayout,
                             QVBoxLayout,
                             QMainWindow,
                             QPushButton,
                             QLineEdit,
                             QLabel,
                             QSizePolicy)

country: str = ''

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs) -> NoReturn:
        super().__init__(*args, **kwargs)
        self.widget = QWidget()
        self.results_existance = 0
        self.widget.setStyleSheet("color:white; background-color: black;")
        self.setCentralWidget(self.widget)
        self.setWindowTitle("World Weather")
        self.height = 100
        self.setFixedSize(500, self.height)
        self.mainLayout = QVBoxLayout()
        self._horizontal_layout = QHBoxLayout()
        self.mainLayout.addLayout(self._horizontal_layout)
        self.widget.setLayout(self.mainLayout)
        self.display = QLineEdit(self)
        self.weather_in_capital = QLabel(self)
        self.OkButton = QPushButton('OK', self)
        self.OkButton.setStyleSheet("color:black; background-color: white;")
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('COUNTRY: ')
        self.OkButton.resize(50, 32)
        self.display.resize(250, 30)
        self._horizontal_layout.addWidget(self.nameLabel)
        self._horizontal_layout.addWidget(self.display)
        self._horizontal_layout.addWidget(self.OkButton)
        self.OkButton.clicked.connect(self._clickMethod_single_country)

    def _clear_all_data(self):
        self.weather_in_capital.clear()

    def _clickMethod_single_country(self) -> NoReturn:
        if self.results_existance != 0:
            self._clear_all_data()
            self.results_existance = 0
            self.height += 10
        country = self.display.text()
        main_body_function()
        connection = psycopg2.connect(host='localhost', database='postgres', port=5432, user='postgres', password='1111')
        inserting_weather_to_capital(connection, country)
        cursor = connection.cursor()
        cursor.execute('select weather_in_capital.capitalname, weather_in_capital.weather_description, weather_in_capital.temperature from weather_in_capital left join countries on weather_in_capital.capitalname = countries.capitalname')
        correct = cursor.fetchall()
        connection.commit()
        cursor.close()
        try:
            self.weather_in_capital.setText(f"""
                                                Country: {country},
                                                Capital: {correct[0][0]},
                                                Weather: {correct[0][1]},
                                                Temperature: {correct[0][2]}""")
        except Exception:
            self.weather_in_capital.setText(f"{country} doesn't exist in Universe")
        self.mainLayout.addWidget(self.weather_in_capital)
        self.weather_in_capital.show()        

def create_countries_table(connection) -> NoReturn:
    if path.exists("capitals.json"):
        json_file = open("capitals.json")
        data: Dict = json.load(json_file)
    else:
        source = urllib.request.urlopen("http://techslides.com/demos/country-capitals.json")
        data = json.loads(source.read())
        with open('capitals.json', 'w') as f:
            json.dump(data, f, indent=4)
    try: 
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE countries(capitalname varchar(40) primary key, countryname varchar(40))')
        print("countries created")
        for item in data:
            if item['CapitalName'] not in ('N/A','Jerusalem', 'Kingston', 'Washington'):
                cursor.execute("INSERT INTO countries(countryname, capitalname) VALUES(%s, %s)", (item['CountryName'], item['CapitalName']))
                connection.commit()
        print("countries added")
        cursor.close()
    except Exception as e:
        print(e)
        print('database is created already')
        cursor.close()
        connection.rollback()

def create_list_of_capitals(connection) -> NoReturn:
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE weather_in_capital(capitalname varchar(40), foreign key(capitalname) references countries(capitalname), weather_description varchar(40), temperature integer)')
    cursor.close()
    connection.commit()
    print("capitals created")

def inserting_weather_to_capital(connection, country) -> NoReturn:
    cursor = connection.cursor()
    print(f"country = {country}")
    cursor.execute(f"select countries.capitalname from countries where countries.countryname = '{country}'")
    cities: List = cursor.fetchall()
    try:
        database_weather = requests.get('http://api.openweathermap.org/data/2.5/weather?',
                                        {'q': cities[0][0], 
                                        'units': 'metric',
                                        'appid':'a5c5f26e7e133daa411606be2347d43c',
                                        'lang':'ua'})
        database_weather = database_weather.json()
        cursor.execute("insert into weather_in_capital (capitalname, weather_description, temperature) values (%s, %s, %s)", (cities[0][0], database_weather['weather'][0]['description'], database_weather['main']['temp']))
        connection.commit()
    except Exception:
        pass
    finally:
        cursor.close()

def main_body_function() -> NoReturn:
    connection = psycopg2.connect(host='localhost', database='postgres', port=5432, user='postgres', password='1111')
    cursor = connection.cursor()
    print('Connection established')
    cursor.execute('DROP TABLE IF EXISTS weather_in_capital')
    cursor.execute('DROP TABLE IF EXISTS countries')
    create_countries_table(connection)
    create_list_of_capitals(connection)  
    connection.close()

def main_window() -> NoReturn:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main_window()



# COMING SOON

# def inserting_weather_to_capitals_all(connection) -> NoReturn:
#     cursor = connection.cursor()
#     cursor.execute('select capitalname from countries')
#     cities = cursor.fetchall()
#     print(f"cities: {cities}")
#     for item in cities:
#         if item not in ('N/A','Jerusalem'):
#             try:
#                 database_weather = requests.get('http://api.openweathermap.org/data/2.5/weather?',
#                                                 {'q': item,
#                                                 'units': 'metric',
#                                                 'appid':'a5c5f26e7e133daa411606be2347d43c',
#                                                 'lang':'ua'})
#                 database_weather = database_weather.json()
#                 cursor.execute(f"insert into weather_in_capital (capitalname, weather_description, temperature) values (%s, %s, %s)", (item, database_weather['weather'][0]['description'], database_weather['main']['temp']))
#                 connection.commit()
#             except Exception:
#                 continue
#     cursor.close()

