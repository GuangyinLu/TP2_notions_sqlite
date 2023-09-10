import sys
from pathlib import Path

from PyQt6 import QtGui

from PyQt6.QtGui import *
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMainWindow, QVBoxLayout, QTableView, \
    QHBoxLayout, QComboBox, QLineEdit, QHeaderView, QAbstractItemView, QMessageBox

from pkgCarnetGestion.OperationDB import *

class CarnetGestion(QMainWindow):
    def __init__(self):
        super(CarnetGestion, self).__init__()

        self.long = 600
        self.high = 500
        self.high_up = int(self.high * 0.8)
        self.high_down = int(self.high * 0.2)
        self.xy_size = self.geometry()

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
        self.setWindowIcon(QtGui.QIcon('./images/cat.png'))
        self.show()

    def initAffichage(self):
        def row_click():
            i_click = self.tableView.selectedIndexes()
            self.nom_click = i_click[0].data()
            self.prenom_click = i_click[1].data()
            self.tel_click = i_click[2].data()
            self.mail_click = i_click[3].data()
            self.btn_modifier.setVisible(True)

            self.le_nom_modifier.setText(self.nom_click)
            self.le_prenom_modifier.setText(self.prenom_click)
            self.le_tel_modifier.setText(self.tel_click)
            self.le_mail_modifier.setText(self.mail_click)

        def modifier():
            self.win_rechercher.hide()
            self.win_ajouter.hide()
            self.win_modifier.show()
            self.win_about.hide()
            self.btn_ajouter.setVisible(False)
            self.btn_rechercher.setVisible(False)
            self.btn_initialiser.setVisible(False)

        def initialiser():
            rec_code = QMessageBox.question(self, "Confirmer", "Ça va supprimer toutes les données dans votre carnet!",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)

            if rec_code != 65536:
                DropTable('carnet')
                CreerTable('carnet')
                self.actualiser_Table()

        self.win_affichage = QWidget(parent = self)
        self.win_affichage.setProperty('name', 'table')
        self.btn_initialiser = QPushButton("Initialiser Carnet")
        self.btn_initialiser.setProperty('name', 'menu_btn')
        self.btn_initialiser.setIcon(QIcon('./images/refresh.png'))
        self.btn_rechercher = QPushButton("Rechercher")
        self.btn_rechercher.setProperty('name', 'menu_btn')
        self.btn_rechercher.setIcon(QIcon('./images/recherch.png'))
        self.btn_ajouter = QPushButton("Ajouter")
        self.btn_ajouter.setProperty('name', 'menu_btn')
        self.btn_ajouter.setIcon(QIcon('./images/ajoute.png'))
        self.btn_modifier = QPushButton("Modifier")
        self.btn_modifier.setProperty('name', 'menu_btn')
        self.btn_modifier.setIcon(QIcon('./images/modifier.png'))
        self.btn_modifier.setVisible(False)

        self.btn_initialiser.clicked.connect(initialiser)
        self.btn_rechercher.clicked.connect(self.rechercher)
        self.btn_ajouter.clicked.connect(self.ajouter)
        self.btn_modifier.clicked.connect(modifier)

        hbox = QHBoxLayout()
        hbox.addWidget(self.btn_initialiser)
        hbox.addStretch(1)
        hbox.addWidget(self.btn_rechercher)
        hbox.addWidget(self.btn_ajouter)
        hbox.addWidget(self.btn_modifier)

        win_menu_btn = QWidget()
        win_menu_btn.setProperty('name','menu')
        win_menu_btn.setLayout(hbox)

        vbox_menu = QVBoxLayout()
        vbox_menu.addWidget(win_menu_btn)

        vbox = QVBoxLayout()
        vbox.addLayout(vbox_menu)


        data = LireEnregistrement('carnet')
        self.headers = data[1]
        self.rows = data[0]
        self.model1 =self.Afficher_Carnet_DB(self.headers, self.rows)

        self.tableView = QTableView()
        self.tableView.setModel(self.model1)

        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableView.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableView.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        self.tableView.clicked.connect(row_click)

        vbox.addWidget(self.tableView)

        self.win_affichage.setLayout(vbox)

        self.win_affichage.move(self.xy_size.x(), self.xy_size.y())
        self.win_affichage.setFixedSize(self.long, self.high_up)
        self.win_affichage.show()

    def initAjouter(self):
        self.win_ajouter = QWidget(parent = self)

        def nouvell_Ajouter():
            nomTable = 'carnet'
            nom = str(self.le_nom_ajouter.text()).strip()
            prenom = self.le_prenom_ajouter.text().strip()
            tel = self.le_tel_ajouter.text().replace('-', '').replace('(', '').replace(')', '').lstrip('+').strip()
            mail = self.le_mail_ajouter.text().strip()
            if verifier_personne_exsist('carnet', nom, prenom):
                if Verifier_Tel(tel) and Verifier_Mail(mail):
                    AjouterEnregistrement(nomTable, nom, prenom, tel, mail)
                    self.win_rechercher.hide()
                    self.win_ajouter.hide()
                    self.win_modifier.hide()
                    self.win_about.show()
                    self.actualiser_Table()
                    self.initialiser_LE()
                elif Verifier_Tel(tel):
                    QMessageBox.warning(self, 'Attention', 'Mail: Erreur!!!', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
                elif Verifier_Mail(mail):
                    QMessageBox.warning(self, 'Attention', 'Tel: Erreur!!!', QMessageBox.StandardButton.Ok,  QMessageBox.StandardButton.Ok)
                else:
                    QMessageBox.warning(self, 'Attention', 'Tel: Erreur!!!\nMail: Erreur!!!', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            else:
                QMessageBox.warning(self, 'Attention', 'Cette personne est déjà dans la liste!!!', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)

        label_nom = QLabel("Nom:")
        label_nom.setFixedWidth(30)
        self.le_nom_ajouter = QLineEdit(self)
        label_prenom = QLabel("Prenom:")
        label_prenom.setFixedWidth(50)
        self.le_prenom_ajouter = QLineEdit(self)
        label_tel = QLabel("Tel:")
        label_tel.setFixedWidth(30)
        self.le_tel_ajouter = QLineEdit(self)
        label_mail = QLabel("Mail:")
        label_mail.setFixedWidth(30)
        self.le_mail_ajouter = QLineEdit(self)
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
        hbox_nom.addWidget(self.le_nom_ajouter)
        hbox_nom.addWidget(label_prenom)
        hbox_nom.addWidget(self.le_prenom_ajouter)
        vbox.addLayout(hbox_nom)
        hbox_tel = QHBoxLayout()
        hbox_tel.addWidget(label_tel)
        hbox_tel.addWidget(self.le_tel_ajouter)
        vbox.addLayout(hbox_tel)
        hbox_mail = QHBoxLayout()
        hbox_mail.addWidget(label_mail)
        hbox_mail.addWidget(self.le_mail_ajouter)
        vbox.addLayout(hbox_mail)

        vbox.addLayout(hbox)

        self.win_ajouter.setLayout(vbox)
        self.win_ajouter.move(self.xy_size.x(), self.xy_size.y() + self.high_up)
        self.win_ajouter.setFixedSize(self.long, self.high_down)

    def initModifier(self):
        def save_modifier():
            nomTable = 'carnet'
            nom = self.le_nom_modifier.text()
            prenom = self.le_prenom_modifier.text()
            tel = self.le_tel_modifier.text().replace('-', '').replace('(', '').lstrip('+').replace(')', '').strip()
            mail = self.le_mail_modifier.text()
            if Verifier_Tel(tel) and Verifier_Mail(mail):
                nom_old = self.nom_click
                prenom_old = self.prenom_click
                ModifierEnregistrement(nomTable, nom, prenom, tel, mail, nom_old, prenom_old)
                self.actualiser_Table()
                self.initialiser_LE()
            elif Verifier_Tel(tel):
                QMessageBox.warning(self, 'Warning', 'Mail: Erreur!!!', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            elif Verifier_Mail(mail):
                QMessageBox.warning(self, 'Warning', 'Tel: Erreur!!!', QMessageBox.StandardButton.Ok,  QMessageBox.StandardButton.Ok)
            else:
                QMessageBox.warning(self, 'Warning', 'Tel: Erreur!!!\nMail: Erreur!!!', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)

        def delete_modifier():
            nomTable = 'carnet'
            nom = self.le_nom_modifier.text()
            prenom = self.le_prenom_modifier.text()
            SupprimerEnregistrement(nomTable, nom, prenom)
            self.actualiser_Table()
            self.initialiser_LE()

        self.win_modifier = QWidget(parent = self)

        label_nom = QLabel("Nom:")
        label_nom.setFixedWidth(30)
        self.le_nom_modifier = QLineEdit(self)
        label_prenom = QLabel("Prenom:")
        label_prenom.setFixedWidth(50)
        self.le_prenom_modifier = QLineEdit(self)
        label_tel = QLabel("Tel:")
        label_tel.setFixedWidth(30)
        self.le_tel_modifier = QLineEdit(self)
        label_mail = QLabel("Mail:")
        label_mail.setFixedWidth(30)
        self.le_mail_modifier = QLineEdit(self)
        btn_save = QPushButton("Sauvegarder")
        btn_cancel = QPushButton("Annuler")
        btn_delete = QPushButton("Supprimer")

        btn_save.clicked.connect(save_modifier)
        btn_cancel.clicked.connect(self.annuler)
        btn_delete.clicked.connect(delete_modifier)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn_save)
        hbox.addWidget(btn_cancel)
        hbox.addWidget(btn_delete)

        vbox = QVBoxLayout()

        hbox_nom = QHBoxLayout()
        hbox_nom.addWidget(label_nom)
        hbox_nom.addWidget(self.le_nom_modifier)
        hbox_nom.addWidget(label_prenom)
        hbox_nom.addWidget(self.le_prenom_modifier)
        vbox.addLayout(hbox_nom)

        hbox_tel = QHBoxLayout()
        hbox_tel.addWidget(label_tel)
        hbox_tel.addWidget(self.le_tel_modifier)
        vbox.addLayout(hbox_tel)

        hbox_mail = QHBoxLayout()
        hbox_mail.addWidget(label_mail)
        hbox_mail.addWidget(self.le_mail_modifier)
        vbox.addLayout(hbox_mail)

        vbox.addLayout(hbox)

        self.win_modifier.setLayout(vbox)
        self.win_modifier.move(self.xy_size.x(), self.xy_size.y() + self.high_up)
        self.win_modifier.setFixedSize(self.long, self.high_down)

    def initRechercher(self):
        def refresh_table_rechercher():
            option = str(self.qcomb_choix.currentText())
            text_rechercher = str("{0}".format(self.le_chercher.text())).strip()
            if option == 'Nom':
                data = LireEnregistrement('carnet', nom = text_rechercher)
            elif option == 'Prenom':
                data = LireEnregistrement('carnet', prenom = text_rechercher)
            elif option == 'Tel':
                data = LireEnregistrement('carnet', tel = text_rechercher)
            elif option == 'Mail':
                data = LireEnregistrement('carnet', mail = text_rechercher)

            self.headers = data[1]
            self.rows = data[0]
            self.model2 = self.Afficher_Carnet_DB(self.headers, self.rows)
            self.tableView.setModel(self.model2)
            self.tableView.update()

        self.win_rechercher = QWidget(parent = self)

        self.qcomb_choix = QComboBox()
        self.qcomb_choix.addItems(["Nom", "Prenom", "Tel", "Mail"])
        self.le_chercher = QLineEdit(self)
        btn_cancel = QPushButton("Annuler")

        self.le_chercher.textChanged.connect(refresh_table_rechercher)
        self.qcomb_choix.currentIndexChanged.connect(refresh_table_rechercher)
        btn_cancel.clicked.connect(self.annuler)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn_cancel)

        vbox = QVBoxLayout()

        hbox_cherche = QHBoxLayout()
        hbox_cherche.addWidget(self.qcomb_choix)
        hbox_cherche.addWidget(self.le_chercher)
        vbox.addLayout(hbox_cherche)
        vbox.addLayout(hbox)

        self.win_rechercher.setLayout(vbox)

        self.win_rechercher.move(self.xy_size.x(), self.xy_size.y() + self.high_up)
        self.win_rechercher.setFixedSize(self.long, self.high_down)

    def initAbout(self):
        self.win_about = QWidget(parent = self)

        label_about_a = QLabel("Lu-Ly-Cla's Address Book!")
        label_about_a.setProperty('name', 'abouta')

        label_about_b = QLabel('Lynn Cazeau\nClaudia Guerrero\nGuangyin Lu')
        label_about_b.setProperty('name', 'aboutb')

        vbox = QVBoxLayout()
        vbox.addWidget(label_about_a)
        vbox.addWidget(label_about_b)

        label_carnet = QLabel(self)
        pixmap = QPixmap('./images/carnet.png')
        label_carnet.setPixmap(pixmap)
        label_carnet.setScaledContents(True)
        label_carnet.setFixedWidth(100)
        vbox_image_carnet = QVBoxLayout()
        vbox_image_carnet.addWidget(label_carnet)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox_image_carnet)
        hbox.addLayout(vbox)

        self.win_about.setLayout(hbox)

        self.win_about.move(self.xy_size.x(), self.xy_size.y() + self.high_up)
        self.win_about.setFixedSize(self.long, self.high_down)
    def rechercher(self):
        self.win_rechercher.show()
        self.win_ajouter.hide()
        self.win_modifier.hide()
        self.win_about.hide()

        self.btn_modifier.setVisible(False)
        self.btn_ajouter.setVisible(False)
        self.btn_initialiser.setVisible(False)

    def ajouter(self):
        self.win_rechercher.hide()
        self.win_ajouter.show()
        self.win_modifier.hide()
        self.win_about.hide()

        self.btn_modifier.setVisible(False)
        self.btn_rechercher.setVisible(False)
        self.btn_initialiser.setVisible(False)

    def annuler(self):
        self.win_rechercher.hide()
        self.win_ajouter.hide()
        self.win_modifier.hide()
        self.win_about.show()

        self.btn_modifier.setVisible(False)
        self.btn_initialiser.setVisible(True)
        self.btn_ajouter.setVisible(True)
        self.btn_rechercher.setVisible(True)
        self.initialiser_LE()

        self.actualiser_Table()

    def initialiser_LE(self):
        self.le_nom_ajouter.setText("")
        self.le_prenom_ajouter.setText("")
        self.le_tel_ajouter.setText("")
        self.le_mail_ajouter.setText("")
        self.le_nom_modifier.setText("")
        self.le_prenom_modifier.setText("")
        self.le_tel_modifier.setText("")
        self.le_mail_modifier.setText("")
        self.le_tel_modifier.setText("")

    def actualiser_Table(self):
        data = LireEnregistrement('carnet')
        self.headers = data[1]
        self.rows = data[0]
        self.model2 = self.Afficher_Carnet_DB(self.headers, self.rows)
        self.tableView.setModel(self.model2)
        self.tableView.update()

    def Afficher_Carnet_DB(self, headers, rows):
        countRow = len(rows)
        countColumn = len(headers)
        model = QStandardItemModel(countRow, countColumn)

        model.setHorizontalHeaderLabels(headers)

        for x in range(countRow):
            for y in range(countColumn):
                item = QStandardItem(rows[x][y + 1])
                model.setItem(x, y, item)

        return model

app = QApplication(sys.argv)
app.setStyleSheet(Path('./style.qss').read_text())
win = CarnetGestion()
win.show()
sys.exit(app.exec())

