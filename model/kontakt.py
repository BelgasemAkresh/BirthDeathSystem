class Kontakt:
    def __init__(self, employee, visaNumber, vorname, nachname,
                 passport, profession, visaIss, duration, visaValid, entriesNumber, entryFee,
                 visaArt, port, work, note, image_data, id=None):
        self.id = id
        self.employee = employee
        self.visaNumber = visaNumber
        self.visaArt = visaArt
        self.vorname = vorname
        self.nachname = nachname
        self.passport = passport
        self.profession = profession
        self.visaIss = visaIss
        self.duration = duration
        self.visaValid = visaValid
        self.entriesNumber = entriesNumber
        self.entryFee = entryFee
        self.port = port
        self.work = work
        self.note = note
        self.image_data = image_data


    def __getitem__(self, key):
        return getattr(self, key, None)

