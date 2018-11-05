from sqlalchemy import Column, Integer, String
from src import db


class Page(db.Model):
    __tablename__ = 'page'
    id = Column(Integer, nullable=False, primary_key=True)
    chapter = Column(Integer)
    page_no = Column(Integer)
    url = Column(String)

    def __init__(self, chapter, page_no, url):
        self.chapter = chapter
        self.page_no = page_no,
        self.url = url
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"page object <{self.chapter} - {self.page_no}>"
