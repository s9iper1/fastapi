from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from config.db import Base


class Notes(Base):
    __tablename__ = "note"
    id = Column('id', Integer, primary_key=True)
    title = Column('title', String(255))
    description = Column('description', Text)
    read = Column('read', Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users_test.id'))

    item = relationship('Users', back_populates='note')