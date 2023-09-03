import sys

from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import *

headers = ["Nom", "Prenom", "Tele", "Mail"]
rows = [("Lu", "Guangyin", "514-553-9986", "luguangyin.mtl@gmail.com"),
        ("Guerrero", "Claudia", "514-888-7799", "claudia@gmail.com"),
        ("Cazeau", "Lynn", "438-654-9977", "Lynn@gmail.com"),
        ("Babari", "Raouf", "438-987-2288", "raouf@gmail.com")]

class Afficher_Carnet(QWidget):

    def __init__(self, headers, rows):
        super(Afficher_Carnet, self).__init__()
        self.headers = headers
        self.rows = rows

        countRow = len(self.rows)
        countColumn = len(self.headers)
        self.model = QStandardItemModel(countRow, countColumn)

        self.model.setHorizontalHeaderLabels(headers)

        for x in range(countRow):
            for y in range(countColumn):
                item = QStandardItem(rows[x][y])
                self.model.setItem(x, y, item)

        self.tableView = QTableView()
        self.tableView.setModel(self.model)

        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        vbox = QVBoxLayout()
        vbox.addWidget(self.tableView)
        self.setLayout(vbox)


"""
app = QApplication(sys.argv)
view = Afficher_Carnet(headers, rows)
view.show()
app.exec()

"""
