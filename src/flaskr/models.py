from flaskr import db


class MedicalTerms(db.Model):

    __table_args__ = {"schema": "public"}
    __tablename__ = "medicalterms"
    index = db.Column(db.Integer, primary_key=True)
    medical_term = db.Column(db.String)
