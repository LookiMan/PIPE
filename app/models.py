from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin


Base = declarative_base()


class File(Base, SerializerMixin):
    __tablename__ = 'files'

    serialize_only = ('id', 'name')

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)

    def __repr__(self):
        return f'<File {self.name}>'
