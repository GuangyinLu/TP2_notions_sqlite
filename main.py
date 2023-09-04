from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow, QVBoxLayout, QTableView, \
    QHBoxLayout, QComboBox, QLineEdit, QHeaderView, QAbstractItemView
import sys
from pkgCarnetGestion.AffichageTable import *
from pkgCarnetGestion.OpenrationDB import *

class CarnetGestion(QMainWindow):
    def __init__(self):
        super(CarnetGestion, self).__init__()
        self.model1 = None
        self.main_layout = QVBoxLayout()
        self.win_main = QWidget()
        self.win_main.setLayout(self.main_layout)

        self.long = 700
        self.high = 600
        self.hign_up = int(self.high * 0.8)
        self.high_down = int(self.high * 0.2)
        self.xy_size = self.geometry()

        data = LireEnregistrement('carnet')
        data[1].pop(0)
        self.headers = data[1]
        self.rows = data[0]

        self.initAffichage()
        self.initModifier()
        self.initAjouter()
        self.initRechercher()
        self.initAbout()

        self.win_affichage.show()
        self.win_ajouter.hide()
        self.win_modifier.hide()
        self.win_rechercher.hide()
        self.win_about.show()

        self.setFixedSize(self.long, self.high)
        self.setWindowTitle("Carnet d'Adresses")
        self.show()

    def initAffichage(self):
        self.win_affichage = QWidget(parent = self)

        btn_rechercher = QPushButton("Rechercher")
        btn_ajouter = QPushButton("Nouvelle")
        btn_modifier = QPushButton("Modifier")

        btn_rechercher.clicked.connect(self.rechercher)
        btn_ajouter.clicked.connect(self.ajouter)
        btn_modifier.clicked.connect(self.modifier)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn_rechercher)
        hbox.addWidget(btn_ajouter)
        hbox.addWidget(btn_modifier)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        self.model1 =Afficher_Carnet_DB(self.headers, self.rows)
        self.tableView = QTableView()
        self.tableView.setModel(self.model1)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        vbox.addWidget(self.tableView)

        self.win_affichage.setLayout(vbox)

        self.win_affichage.move(self.xy_size.x(), self.xy_size.y())
        self.win_affichage.setFixedSize(self.long, self.hign_up)
        self.win_affichage.show()

    def initAjouter(self):
        self.win_ajouter = QWidget(parent = self)

        def nouvell_Ajouter():
            nomTable = 'carnet'
            nom = str(le_nom.text())
            prenom = le_prenom.text()
            tel = le_tel.text()
            mail = le_mail.text()
            AjouterEnregistrement(nomTable, nom, prenom, tel, mail)

            self.win_rechercher.hide()
            self.win_ajouter.hide()
            self.win_modifier.hide()
            self.win_about.show()

            data = LireEnregistrement('carnet')
            data[1].pop(0)
            self.headers = data[1]
            self.rows = data[0]

            self.model2 = Afficher_Carnet_DB(self.headers, self.rows)
            self.tableView.setModel(self.model2)
            self.tableView.update()

        label_nom = QLabel("Nom:")
        le_nom = QLineEdit(self)
        label_prenom = QLabel("Prenom")
        le_prenom = QLineEdit(self)
        label_tel = QLabel("Tel:")
        le_tel = QLineEdit(self)
        label_mail = QLabel("Mail:")
        le_mail = QLineEdit(self)
        btn_save = QPushButton("Sauvegarder")
        btn_cancel = QPushButton("Annuler")

        btn_save.clicked.connect(nouvell_Ajouter)

        btn_cancel.clicked.connect(self.annuler)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn_save)
        hbox.addWidget(btn_cancel)

        vbox = QVBoxLayout()

        hbox_nom = QHBoxLayout()
        hbox_nom.addWidget(label_nom)
        hbox_nom.addWidget(le_nom)
        hbox_nom.addWidget(label_prenom)
        hbox_nom.addWidget(le_prenom)
        vbox.addLayout(hbox_nom)

        hbox_tel = QHBoxLayout()
        hbox_tel.addWidget(label_tel)
        hbox_tel.addWidget(le_tel)
        vbox.addLayout(hbox_tel)

        hbox_mail = QHBoxLayout()
        hbox_mail.addWidget(label_mail)
        hbox_mail.addWidget(le_mail)
        vbox.addLayout(hbox_mail)

        vbox.addLayout(hbox)

        self.win_ajouter.setLayout(vbox)
        self.win_ajouter.move(self.xy_size.x(), self.xy_size.y() + self.hign_up)
        self.win_ajouter.setFixedSize(self.long, self.high_down)

    def initModifier(self):
        self.win_modifier = QWidget(parent = self)

        label_nom = QLabel("Nom:")
        le_nom = QLineEdit(self)
        label_prenom = QLabel("Prenom:")
        le_prenom = QLineEdit(self)
        label_tel = QLabel("Tel:")
        le_tel = QLineEdit(self)
        label_mail = QLabel("Mail:")
        le_mail = QLineEdit(self)
        btn_save = QPushButton("Sauvegarder")
        btn_cancel = QPushButton("Annuler")
        btn_delete = QPushButton("Supprimer")

        btn_cancel.clicked.connect(self.annuler)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn_save)
        hbox.addWidget(btn_cancel)
        hbox.addWidget(btn_delete)

        vbox = QVBoxLayout()

        hbox_nom = QHBoxLayout()
        hbox_nom.addWidget(label_nom)
        hbox_nom.addWidget(le_nom)
        hbox_nom.addWidget(label_prenom)
        hbox_nom.addWidget(le_prenom)
        vbox.addLayout(hbox_nom)

        hbox_tel = QHBoxLayout()
        hbox_tel.addWidget(label_tel)
        hbox_tel.addWidget(le_tel)
        vbox.addLayout(hbox_tel)

        hbox_mail = QHBoxLayout()
        hbox_mail.addWidget(label_mail)
        hbox_mail.addWidget(le_mail)
        vbox.addLayout(hbox_mail)

        vbox.addLayout(hbox)

        self.win_modifier.setLayout(vbox)
        self.win_modifier.move(self.xy_size.x(), self.xy_size.y() + self.hign_up)
        self.win_modifier.setFixedSize(self.long, self.high_down)

    def initRechercher(self):
        self.win_rechercher = QWidget(parent = self)

        qcomb_choix = QComboBox()
        qcomb_choix.addItems(["Nom", "Prenom", "Tel", "Mail"])
        le_chercher = QLineEdit(self)
        btn_rechercher = QPushButton("Rechercher")
        btn_cancel = QPushButton("Annuler")

        btn_cancel.clicked.connect(self.annuler)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn_rechercher)
        hbox.addWidget(btn_cancel)

        vbox = QVBoxLayout()

        hbox_cherche = QHBoxLayout()
        hbox_cherche.addWidget(qcomb_choix)
        hbox_cherche.addWidget(le_chercher)
        vbox.addLayout(hbox_cherche)
        vbox.addLayout(hbox)

        self.win_rechercher.setLayout(vbox)

        self.win_rechercher.move(self.xy_size.x(), self.xy_size.y() + self.hign_up)
        self.win_rechercher.setFixedSize(self.long, self.high_down)

    def initAbout(self):
        self.win_about = QWidget(parent = self)

        label = QLabel("Bienvenu!")
        label.setFont(QFont('Arial', 40))
        label.setStyleSheet("color: rgb(255, 0, 0);")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        #self.win_about.setFixedSize(600, 250)
        self.win_about.setLayout(vbox)

        self.win_about.move(self.xy_size.x(), self.xy_size.y() + self.hign_up)
        self.win_about.setFixedSize(self.long, self.high_down)
    def rechercher(self):
        self.win_rechercher.show()
        self.win_ajouter.hide()
        self.win_modifier.hide()
        self.win_about.hide()

    def ajouter(self):
        self.win_rechercher.hide()
        self.win_ajouter.show()
        self.win_modifier.hide()
        self.win_about.hide()

    def modifier(self):
        self.win_rechercher.hide()
        self.win_ajouter.hide()
        self.win_modifier.show()
        self.win_about.hide()

    def annuler(self):
        self.win_rechercher.hide()
        self.win_ajouter.hide()
        self.win_modifier.hide()
        self.win_about.show()

app = QApplication(sys.argv)
ex = CarnetGestion()
ex.show()
sys.exit(app.exec())

