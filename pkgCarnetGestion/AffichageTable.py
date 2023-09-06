from PyQt6.QtGui import QStandardItemModel, QStandardItem
import re


def Afficher_Carnet_DB(headers, rows):
        countRow = len(rows)
        countColumn = len(headers)
        model = QStandardItemModel(countRow, countColumn)

        model.setHorizontalHeaderLabels(headers)

        for x in range(countRow):
            for y in range(countColumn):
                item = QStandardItem(rows[x][y+1])
                model.setItem(x, y, item)
        return model

def Tri_sortie_DB(rows):
    for i in range(len(rows)-1):
        for j in range(len(rows)-i-1):
            if str(rows[j][1]).strip().lower() > str(rows[j + 1][1]).strip().lower():
                rows[j], rows[j+1] = rows[j+1], rows[j]
            elif str(rows[j][1]).strip().lower() == str(rows[j+1][1]).strip().lower() and str(rows[j][2]).strip().lower() > (rows[j + 1][2]).strip().lower():
                rows[j], rows[j + 1] = rows[j + 1], rows[j]
    return rows

def Verifier_Tel(tel_number):
    pattern = r'^([1-9]\d{9,12})$'
    return re.match(pattern, tel_number)

def Verifier_Mail(email):
    pattern = r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$'
    return re.match(pattern, email)

