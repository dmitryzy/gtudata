# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import Session
import os
from gtudata.items import SpecItem, GtudataItem
from scrapy.exceptions import DropItem



Base = declarative_base()

class SpecTable(Base):
    __tablename__ = 'specdata'
    id = Column(Integer, primary_key=True)
    spec = Column(String)
    spectitle = Column(String)

    def __init__(self, spec, spectitle):
        self.spec= spec
        self.spectitle = spectitle

    def __repr__(self):
        return "<Data %s, %s>" % (self.spec, self.spectitle)


class DataTable(Base):
    __tablename__ = 'gtudata'
    id = Column(Integer, primary_key=True)
    family = Column(String)
    name = Column(String)
    surname = Column(String)
    spec = Column(String)
    ball = Column(Integer)
    url = Column(String)
    pagespec = Column(String)

    def __init__(self, family, name, surname, spec, ball, url, pagespec):
        self.family = family
        self.name = name
        self.surname = surname
        self.spec = spec
        self.ball = ball
        self.url = url
        self.pagespec = pagespec

    def __repr__(self):
        return "<Data %s, %s, %s, %s, %s, %s, %s>" % \
               (self.family, self.name, self.surname, self.spec, self.ball, self.url, self.pagespec)


class GtudataPipeline(object):
    def __init__(self):
        basename = 'data_scraped'
        self.engine = create_engine("sqlite:///%s" % basename, echo=False)
        if not os.path.exists(basename):
            Base.metadata.create_all(self.engine)
        self.fio = set()

    def process_item(self, item, spider):
        if isinstance(item, GtudataItem):
            fio = item['family'] + item['name'] + item['surname']
            if fio not in self.fio:
                dt = DataTable(item['family'],item['name'], item['surname'], item['spec'], item['ball'], item['url'], item['pagespec'])
                self.fio.add(fio)
                self.session.add(dt)
        elif isinstance(item, SpecItem):
            dt = SpecTable(item['spec'],item['SpecName'])
            self.session.add(dt)
        return item

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def open_spider(self, spider):
        self.session = Session(bind=self.engine)


class DuplicatesPipeline(object):
    def __init__(self):
        self.fio = set()

    def process_item(self, item, spider):
        if isinstance(item, GtudataItem):
            fio = item['family'] + item['name'] + item['surname']
            if fio in self.fio:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.fio.add(item['id'])
                return item
        else:
            return item

