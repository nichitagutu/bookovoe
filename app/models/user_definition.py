from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class UserDefinition(Base):
    __tablename__ = 'user_definitions'

    user_definition_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    definition_id = Column(Integer, ForeignKey('definitions.definition_id'), nullable=False)

    user = relationship('User', back_populates='user_definitions')
    definition = relationship('Definition', back_populates='user_definitions')


