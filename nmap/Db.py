import mysql.connector as mysql

class Db():
    def __init__(self):
        self.db = mysql.connect(host="localhost", user="root", passwd="", database="rpi")
        if not self.db.is_connected():print("pas connecté")

    def exec(self, commande, insertId=False):
        """Execute une commande"""
        cursor = self.db.cursor()
        cursor.execute(commande)
        self.db.commit()
        if insertId:
            return cursor.lastrowid

    def getSession(self):
        """Retourne l'ip et la date de la session"""
        cursor = self.db.cursor()
        cursor.execute("SELECT max(Date), ip FROM session")
        result = cursor.fetchall()[0]
        return result[1], result[0]
