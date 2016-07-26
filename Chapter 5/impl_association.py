from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import dautil as dl
import os


Base = declarative_base()

class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False, unique=True)
    links = relationship('Link', secondary='page_links')

    def __repr__(self):
        return "Id=%d filename=%s" %(self.id, self.filename)


class Link(Base):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return "Id=%d url=%s" %(self.id, self.url)

class PageLink(Base):
    __tablename__ = 'page_links'
    page_id = Column(Integer, ForeignKey('pages.id'), primary_key=True)
    link_id = Column(Integer, ForeignKey('links.id'), primary_key=True)
    page = relationship('Page', backref=backref('link_assoc'))
    link = relationship('Link', backref=backref('page_assoc'))

    def __repr__(self):
        return "page_id=%s link_id=%s" %(self.page_id, self.link_id)


def process_file(fname, session):
    with open(fname) as html_file:
        text = html_file.read()

        if dl.db.count_where(session, Page.filename, fname):
            # Cowardly refusing to continue
            return

        page = Page(filename=fname)
        hrefs = dl.web.find_hrefs(text)

        for href in set(hrefs):
            # Only saving http links
            if href.startswith('http'):
                if dl.db.count_where(session, Link.url, href):
                    continue

                link = Link(url=href)
                session.add(PageLink(page=page, link=link))

        session.commit()


def populate():
    dir = dl.data.get_data_dir()
    path = os.path.join(dir, 'crawled_pages.db')
    engine = create_engine('sqlite:///' + path)
    DBSession = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = DBSession()

    files  = ['460_cc_phantomjs.html', '468_live_phantomjs.html']

    for file in files:
        process_file(file, session)

    return session


if __name__ == "__main__":
    session = populate()
    printer = dl.log_api.Printer(nelems=3)
    pages = session.query(Page).all()
    printer.print('Pages', pages)

    links = session.query(Link).all()
    printer.print('Links', links)

    page_links = session.query(PageLink).all()
    printer.print('PageLinks', page_links)
