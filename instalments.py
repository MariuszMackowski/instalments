import sys, os

from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication, QPushButton, QComboBox)
from bs4 import BeautifulSoup
import urllib.request as urllib2
import math


# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         # PyInstaller creates a temp folder and stores path in _MEIPASS
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#
#     return os.path.join(base_path, relative_path)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.number = QLabel('Id')
        self.price = QLabel('Cena')
        self.rata = QLabel('Rata')
        self.opis = QLabel("Opis")
        self.bn = QPushButton("Szukaj", self)
        self.bn.clicked.connect(self.buttonClicked)
        self.cb = QComboBox()
        self.cb.addItems(["Komputer", "Monitor", "Laptop"])

        self.numberEdit = QLineEdit()
        self.priceEdit = QLineEdit()
        self.rataEdit = QLineEdit()
        self.opisEdit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.number, 1, 0)
        grid.addWidget(self.numberEdit, 1, 1)
        grid.addWidget(self.bn, 1, 2)

        grid.addWidget(self.price, 2, 0)
        grid.addWidget(self.priceEdit, 2, 1)

        grid.addWidget(self.rata, 3, 0)
        grid.addWidget(self.rataEdit, 3, 1)

        grid.addWidget(self.opis, 4, 0)
        grid.addWidget(self.opisEdit, 4, 1, 1, 2)

        grid.addWidget(self.cb, 2, 2, 2, 1)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Leniuszek')
        self.show()

    def buttonClicked(self):
        dane = [["System operacyjny", "Procesor", "Pamięć", "Dysk", "Napęd optyczny", "Karta graficzna", "Porty"],
                ["Rozdzielczość", "Rozmiar matrycy", "Kontrast", "Czas reakcji", "Jasność", "Kąty widzenia", "Złącza"],
                ["System operacyjny", "Procesor", "Pamięć", "Dysk", "Napęd optyczny", "Matryca", "Karta graficzna",
                 "Zewnętrzne porty"]]

        product_Id = self.numberEdit.text()
        if product_Id == "":
            return
        url = "http://www.sck.com.pl/product/placeholder/?id=" + product_Id
        page = urllib2.urlopen(url)

        soup = BeautifulSoup(page, 'html.parser')
        cen = cena(soup)
        self.priceEdit.setText(cen)
        self.opisEdit.setText(spec(dane[self.cb.currentIndex()], soup))
        self.rataEdit.setText(str(raty(cen.split(",")[0].replace(" ", ""))))


def cena(soup):
    cena = soup.find('dt').contents[0]
    cena2 = cena.find_next('dt').contents[0]
    return cena + "/ " + cena2


def spec(konfig, soup):
    text = ""
    for x in soup.find_all('tr'):
        if x.contents[1].get_text() in konfig:
            text += str(x.contents[1].get_text() + ":  " + x.contents[3].get_text().strip() + "\n")
    return text


def raty(cena):
    a = [-86937393892191.5, 1309492221949.82, -4952359224.78583, 5688193.11588436, 6004.12765945273, 14.3158063240881]
    cena = int(cena)
    procent = 0
    for i in range(len(a)):
        procent += a[i] / math.pow(cena, len(a) - 1 - i)

    cena += cena * round(procent) / 1200

    return round(cena)



app = QApplication(sys.argv)
ex = Example()
sys.exit(app.exec_())
