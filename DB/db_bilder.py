import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker, declarative_base
import os

Base = declarative_base()


class Words(Base):
    __tablename__ = 'words'
    word_id = sql.Column(name='word_id', type_=sql.Integer, primary_key=True)
    word = sql.Column(name='word', type_=sql.String)

    def __int__(self, word_id, word):
        self.word_id = word_id
        self.word = word

    def __repr__(self):
        return f'{self.word_id} : {self.word_id}'


def words_insert():
    f = open('C:/Users/workc/PycharmProjects/admin/admine_bot/DB/bad_words.txt', 'r')
    text = f.read()
    words = text.split(', ')

    for word in words:
        session.add(Words(word=word))
        session.commit()
    return

db_path = 'C:/Users/workc/PycharmProjects/admin/admine_bot/DB/admin_bot.db'

if os.path.exists(db_path) is False:
    engine = sql.create_engine('sqlite:///C:/Users/workc/PycharmProjects/admin/admine_bot/DB/admin_bot.db', echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    words_insert()
else:
    engine = sql.create_engine('sqlite:///C:/Users/workc/PycharmProjects/admin/admine_bot/DB/admin_bot.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()