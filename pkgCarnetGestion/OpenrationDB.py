import sqlite3

from pkgCarnetGestion.AffichageTable import Tri_sortie_DB


def CreerTable(nomTable):
    conn = sqlite3.connect("tp2.db")
    cur = conn.cursor()

    MaRequeteCreateTable = "CREATE TABLE IF NOT EXISTS "
    MaRequeteCreateTable = MaRequeteCreateTable + str(nomTable)
    MaRequeteCreateTable = MaRequeteCreateTable + """ ("ID"    INTEGER,"Nom"  TEXT,"Prenom"  TEXT,"Tel" TEXT,
        "Mail" TEXT, PRIMARY KEY("ID" AUTOINCREMENT)
    );"""
    cur.execute(MaRequeteCreateTable)
    conn.commit()

def DropTable(nomTable):
    MaRequeteSupprimer = 'Drop table {}'.format(nomTable)
    conn = sqlite3.connect("tp2.db")
    cur = conn.cursor()
    cur.execute(MaRequeteSupprimer)
    conn.commit()

def AjouterEnregistrement(nomTable, nom, prenom, tel, mail):
    MaRequeteInserer = "INSERT INTO {0}  (Nom,Prenom,Tel,Mail) VALUES ('{1}','{2}','{3}','{4}');".format(nomTable, nom, prenom, tel, mail)
    conn = sqlite3.connect("tp2.db")
    cur = conn.cursor()
    cur.execute(MaRequeteInserer)
    conn.commit()

def ModifierEnregistrement(nomTable, nom, prenom, tel, mail, nom_old, prenom_old):
    MaRequeteModifier = "UPDATE {0} SET (Nom,Prenom,Tel,Mail) = ('{1}','{2}','{3}','{4}') WHERE Nom = '{5}' AND Prenom = '{6}';".format(nomTable, nom, prenom, tel, mail, nom_old, prenom_old)
    conn = sqlite3.connect("tp2.db")
    cur = conn.cursor()
    cur.execute(MaRequeteModifier)
    conn.commit()

def SupprimerEnregistrement(nomTable, nom, prenom):
    MaRequeteSupprimer = "DELETE FROM {0} WHERE Nom = '{1}' AND Prenom = '{2}';".format(nomTable, nom, prenom)
    conn = sqlite3.connect("tp2.db")
    cur = conn.cursor()
    cur.execute(MaRequeteSupprimer)
    conn.commit()

def LireEnregistrement(nomTable, **arg):
    MaRequeteAfficher =""
    if len(arg) == 0:
        MaRequeteAfficher = "SELECT * FROM {} ;".format(nomTable)
    elif len(arg) == 1:
        MaRequeteAfficher = "SELECT * FROM {0} WHERE UPPER({1}) LIKE UPPER('%{2}%');".format(nomTable, list(arg)[0], list(arg.values())[0])
    elif len(arg) ==2:
        MaRequeteAfficher = "SELECT * FROM {0} WHERE UPPER({1}) LIKE UPPER('%{2}%') AND UPPER({3}) LIKE UPPER('%{4}%');".format(nomTable, list(arg)[0], list(arg.values())[0], list(arg)[1], list(arg.values())[1])
    conn = sqlite3.connect("tp2.db")
    cur = conn.cursor()

    MaRequeteCreateTable = "CREATE TABLE IF NOT EXISTS "
    MaRequeteCreateTable = MaRequeteCreateTable + str(nomTable)
    MaRequeteCreateTable = MaRequeteCreateTable + """ ("ID"    INTEGER,"Nom"  TEXT,"Prenom"  TEXT,"Tel" TEXT,
        "Mail" TEXT, PRIMARY KEY("ID" AUTOINCREMENT)
    );"""
    cur.execute(MaRequeteCreateTable)

    cur.execute(MaRequeteAfficher)
    data = cur.fetchall()
    data_head=[]
    for field in cur.description:
        data_head.append(field[0])
    conn.commit()
    data_head.pop(0)
    data = Tri_sortie_DB(data)

    data_affichage = []
    for x in data:
        str_tel = str(x[3]).replace('-', '').strip()
        if len(str_tel) == 10:
            str_tel_1 = str_tel[-4:]
            str_tel_2 = str_tel[-7:-4]
            str_tel_3 = str_tel[-10:-7]
            tel_new_str = str(str_tel_3 + '-' + str_tel_2 + '-' + str_tel_1)
            data_affichage.append([x[0], x[1], x[2], tel_new_str, x[4]])
        elif 14 > len(str_tel) > 10:
            str_tel_1 = str_tel[-4:]
            str_tel_2 = str_tel[-7:-4]
            str_tel_3 = str_tel[-10:-7]
            str_tel_4 = str_tel[:-10]
            tel_new_str = str('(+' + str_tel_4 + ')' + str_tel_3 + '-' + str_tel_2 + '-' + str_tel_1)
            data_affichage.append([x[0], x[1], x[2], tel_new_str, x[4]])

    return data_affichage, data_head



