from app.extensions import db

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return self.name

db.create_all()
if not City.query.all():
    db.session.add(City(name='Salvador'))
    db.session.commit()