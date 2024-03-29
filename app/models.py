from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    alias = Column(String, nullable=False)

    def __repr__(self):
        return f'<File {self.name}>'


class StorageLastUpdate(Base):
    __tablename__ = 'storage_last_update'

    id = Column(Integer, primary_key=True)
    value = Column(Integer, default=0, nullable=False)

    def __repr__(self):
        return f'<StorageLastUpdate {self.value}>'
