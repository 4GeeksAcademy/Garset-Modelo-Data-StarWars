from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    subscription_date: Mapped[datetime] = mapped_column(DateTime, default=datetime)
    profile_image: Mapped[str] = mapped_column(String(255), nullable=True)
    favorite_characters: Mapped[List['FavoriteCharacter']] = relationship(
        back_populates='user', cascade='all, delete-orphan')
    favorite_planets: Mapped[List['FavoritePlanet']] = relationship(
        back_populates='user', cascade='all, delete-orphan')
    favorite_vehicles: Mapped[List['FavoriteVehicle']] = relationship(
        back_populates='user', cascade='all, delete-orphan')

class Character(db.Model):
    __tablename__ = 'character'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    species: Mapped[str] = mapped_column(String(50))
    homeworld: Mapped[str] = mapped_column(String(50))
    gender: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(Text())
    image_url: Mapped[str] = mapped_column(String(255))
    favorited_by: Mapped[List['FavoriteCharacter']] = relationship(
        back_populates='character', cascade='all, delete-orphan')
    vehicles: Mapped[List['Vehicle']] = relationship(
        back_populates='pilot')

class Planet(db.Model):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    climate: Mapped[str] = mapped_column(String(50))
    terrain: Mapped[str] = mapped_column(String(50))
    population: Mapped[int] = mapped_column(Integer)
    diameter: Mapped[int] = mapped_column(Integer)  
    image_url: Mapped[str] = mapped_column(String(255))
    favorited_by: Mapped[List['FavoritePlanet']] = relationship(
        back_populates='planet', cascade='all, delete-orphan')
    residents: Mapped[List['Character']] = relationship(
        back_populates='homeworld_relation')

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    model: Mapped[str] = mapped_column(String(50))
    vehicle_class: Mapped[str] = mapped_column(String(50))
    manufacturer: Mapped[str] = mapped_column(String(50))
    length: Mapped[float] = mapped_column(Integer)  
    crew: Mapped[int] = mapped_column(Integer)
    passengers: Mapped[int] = mapped_column(Integer)
    image_url: Mapped[str] = mapped_column(String(255))
    favorited_by: Mapped[List['FavoriteVehicle']] = relationship(
        back_populates='vehicle', cascade='all, delete-orphan')
    pilot_id: Mapped[int] = mapped_column(ForeignKey('character.id'))
    pilot: Mapped['Character'] = relationship(
        back_populates='vehicles')

class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_character'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    character_id: Mapped[int] = mapped_column(ForeignKey('character.id'))
    date_added: Mapped[datetime] = mapped_column(DateTime, default=datetime)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    user: Mapped['User'] = relationship(back_populates='favorite_characters')
    character: Mapped['Character'] = relationship(back_populates='favorited_by')

class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'))
    date_added: Mapped[datetime] = mapped_column(DateTime, default=datetime)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    user: Mapped['User'] = relationship(back_populates='favorite_planets')
    planet: Mapped['Planet'] = relationship(back_populates='favorited_by')

class FavoriteVehicle(db.Model):
    __tablename__ = 'favorite_vehicle'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    vehicle_id: Mapped[int] = mapped_column(ForeignKey('vehicle.id'))
    date_added: Mapped[datetime] = mapped_column(DateTime, default=datetime)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    user: Mapped['User'] = relationship(back_populates='favorite_vehicles')
    vehicle: Mapped['Vehicle'] = relationship(back_populates='favorited_by')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
