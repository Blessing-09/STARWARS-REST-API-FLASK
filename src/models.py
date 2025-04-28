from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Enum
import enum
#from enum import Enum
#from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column
from typing import List, Optional
from sqlalchemy.orm import relationship

db = SQLAlchemy()
#class favorite_type(Enum):
#type: Mapped[favorite_type] = mapped_column(SQLAlchemyEnum(favorite_type), unique=True, nullable=False)
class favorite_type(enum.Enum):
    PEOPLE = "people"
    PLANET = "planet"

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    #age: Mapped[int] = mapped_column(Integer(), unique=False, nullable=False)
    #password: Mapped[str] = mapped_column(String(120), nullable=False)


      # relationship with favourites
    favorites: Mapped[List["Favorite"]] = relationship("Favorite", back_populates="user")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
            #"email": self.email,
            # do not serialize the password, its a security breach
        }
    def __repr__(self):
        return self.name

class People(db.Model):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    birth_year: Mapped[str] = mapped_column(String(120), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(120), nullable=False)
    #gender: Mapped[str] = mapped_column(String(120), nullable=True)

    # relationship with favourites
    favorites: Mapped[List["Favorite"]] = relationship("Favorite", back_populates="people")

    #ser¡alize
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color
        }

class Planet(db.Model):
    __tablename__ = "planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    diameter: Mapped[str] = mapped_column(String(120), nullable=False)
    rotation_period: Mapped[str] = mapped_column(String(120), nullable=False)
    orbital_period: Mapped[str] = mapped_column(String(120), nullable=False)

     # relationship with favourites
    favorites: Mapped[List["Favorite"]] = relationship("Favorite", back_populates="planet")

    #serialize
    def serialize(self): #converts the object into a dictionary, JSON, or some other simplified structure. This allows you to store or transmit the object in a simpler format.
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter
        }

class Favorite(db.Model):
    __tablename__ = "favorites"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    type: Mapped[favorite_type] = mapped_column(Enum(favorite_type), nullable=False)
    people_id: Mapped[Optional[int]] = mapped_column(ForeignKey("people.id"), nullable=True)
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planet.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    # relationship with people, planet and user models
    people: Mapped["People"] = relationship("People", back_populates="favorites")
    planet: Mapped["Planet"]= relationship("Planet", back_populates="favorites")
    user: Mapped["User"] = relationship("User", back_populates="favorites")

    #serialize
    def serialize(self): 
         return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "type": self.type.value
        }