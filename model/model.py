import sqlite3
from typing import List, Optional
from model.kontakt import Kontakt

class Model:
    def __init__(self):
        self.connect()
        self.create_table()

    def connect(self):
        self.conn = sqlite3.connect("kontakt")
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS kontakt (
                id INTEGER PRIMARY KEY,
                employee TEXT,
                visaNumber TEXT,
                visaArt TEXT,
                vorname TEXT,
                nachname TEXT,
                passport TEXT,
                profession TEXT,
                visaIss DATE,
                duration INTEGER,
                visaValid DATE,
                entriesNumber TEXT,
                entryFee TEXT,
                port TEXT,
                work TEXT,
                note TEXT,
                image BLOB
            )
        ''')
        self.conn.commit()

    def add_kontakt(self, kontakt):
        self.cursor.execute('''
            INSERT INTO kontakt (employee, visaNumber, visaArt,
             vorname, nachname, passport, profession,
             visaIss, duration, visaValid,
              entriesNumber, entryFee, port, work, note, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
        kontakt.employee, kontakt.visaNumber, kontakt.visaArt,
        kontakt.vorname, kontakt.nachname, kontakt.passport, kontakt.profession,
        kontakt.visaIss, kontakt.duration,
        kontakt.visaValid, kontakt.entriesNumber, kontakt.entryFee,
        kontakt.port, kontakt.work, kontakt.note, kontakt.image_data))
        self.conn.commit()

    def search(self, employee: Optional[str] = None, passport: Optional[str] = None,
               date_from: Optional[str] = None,
               date_to: Optional[str] = None) -> List[Kontakt]:
        query = 'SELECT * FROM kontakt WHERE 1=1'
        params = []
        if employee:
            query += ' AND employee = ?'
            params.append(employee)
        if passport:
            query += ' AND passport = ?'
            params.append(passport)
        if date_from and date_to:
            query += ' AND visaIss BETWEEN ? AND ?'
            params.extend([date_from, date_to])

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        return self.row_to_kontakt(rows)

    def get_all_kontakte(self):
        self.cursor.execute("SELECT * FROM kontakt")
        rows = self.cursor.fetchall()
        return self.row_to_kontakt(rows)
    def row_to_kontakt(self, rows):
        kontakte = {}
        for row in rows:
            kontakt = Kontakt(
                id=row[0],
                employee=row[1],
                visaNumber=row[2],
                visaArt=row[3],
                vorname=row[4],
                nachname=row[5],
                passport=row[6],
                profession=row[7],
                visaIss=row[8],
                duration=row[9],
                visaValid=row[10],
                entriesNumber=row[11],
                entryFee=row[12],
                port=row[13],
                work=row[14],
                note=row[15],
                image_data=row[16]
            )
            kontakte[row[0]] = kontakt
        kontakte = {key: kontakte[key] for key in reversed(kontakte)}
        return kontakte
    def delete_kontakt(self, id):
        self.cursor.execute("DELETE FROM kontakt WHERE id = ?", (id,))
        self.conn.commit()

    def update_kontakt(self, id, kontakt):
        self.cursor.execute('''
            UPDATE kontakt SET
                employee = ?, visaNumber = ?, visaArt = ?,
                vorname = ?, nachname = ?, passport = ?, profession = ?,
                visaIss = ?, duration = ?, visaValid = ?,
                entriesNumber = ?, entryFee = ?, port = ?, work = ?, note = ?, image = ?
            WHERE id = ?
        ''',
                            (
            kontakt.employee, kontakt.visaNumber, kontakt.visaArt,
            kontakt.vorname, kontakt.nachname, kontakt.passport, kontakt.profession,
            kontakt.visaIss, kontakt.duration, kontakt.visaValid,
            kontakt.entriesNumber, kontakt.entryFee, kontakt.port,
            kontakt.work, kontakt.note, kontakt.image_data,
            id  # Use the explicitly passed ID for the update
        )
                            )
        self.conn.commit()

    def close(self):
        self.conn.close()
