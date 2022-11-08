from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config.db import Base


class Users(Base):
    __tablename__ = 'users_test'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(255))
    email = Column('email', String(255))
    password = Column('password', String(255))
    profile_image = Column('profile_image', String(255))

    note = relationship('Notes', back_populates="item")

