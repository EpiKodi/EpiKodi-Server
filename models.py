from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


friend_table = db.Table('friends',
                        db.Column('user_id_1', db.Text, db.ForeignKey('users.id')),
                        db.Column('user_id_2', db.Text, db.ForeignKey('users.id'))
                        )

pending_friend_table = db.Table('pending_friends',
                                db.Column('user_id_1', db.Text, db.ForeignKey('users.id')),
                                db.Column('user_id_2', db.Text, db.ForeignKey('users.id'))
                                )


class User(db.Model):
    """Model for the User table"""
    __tablename__ = 'users'

    id = db.Column(db.Text, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    friends = db.relationship('User',
                              secondary=friend_table,
                              primaryjoin=friend_table.c.user_id_1 == id,
                              secondaryjoin=friend_table.c.user_id_2 == id)

    pending_friends = db.relationship('User',
                                      secondary=pending_friend_table,
                                      primaryjoin=pending_friend_table.c.user_id_1 == id,
                                      secondaryjoin=pending_friend_table.c.user_id_2 == id)

    files = db.relationship('File')
    stream_id = db.Column(db.Text)

    def __repr__(self):
        return '<User %r>' % self.username


class File(db.Model):
    """Model for the Files table"""
    __tablename__ = 'files'

    id = db.Column(db.Text, primary_key=True)
    user_id = db.Column(db.Text, db.ForeignKey('users.id'))
    filename = db.Column(db.Text, nullable=False)
    user = db.Column(db.Text, nullable=False)
    extension = db.Column(db.String(20), nullable=False)
