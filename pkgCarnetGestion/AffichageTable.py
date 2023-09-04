from PyQt6.QtGui import QStandardItemModel, QStandardItem


"""
headers = ["Nom", "Prenom", "Tele", "Mail"]
rows = [("Lu", "Guangyin", "514-553-9986", "luguangyin.mtl@gmail.com"),
        ("Guerrero", "Claudia", "514-888-7799", "claudia@gmail.com"),
        ("Cazeau", "Lynn", "438-654-9977", "Lynn@gmail.com"),
        ("Babari", "Raouf", "438-987-2288", "raouf@gmail.com")]
"""


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


