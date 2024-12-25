from sqlalchemy import String, Column, ForeignKey, Integer, Boolean, Float
from sqlalchemy.orm import relationship
from app.database import Base


class Layer(Base):
    __tablename__ = "layer"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    abstract = Column(String, nullable=True)
    queryable = Column(Integer, nullable=True)
    opaque = Column(Integer, nullable=True)
    west_bound_longitude = Column(Float, nullable=True)
    east_bound_longitude = Column(Float, nullable=True)
    south_bound_latitude = Column(Float, nullable=True)
    north_bound_latitude = Column(Float, nullable=True)

    # Relationship with Keyword table
    keywords = relationship("Keyword", back_populates="layer", cascade="all, delete-orphan") 
    crss = relationship("Crs", back_populates="layer", cascade="all, delete-orphan")


class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True)
    layer_id = Column(Integer, ForeignKey("layer.id", ondelete="CASCADE"), nullable=False)
    keyword = Column(String, nullable=False)

    # Relationship back to Layer
    layer = relationship("Layer", back_populates="keywords")

class Crs(Base):
    __tablename__ = "crss"

    id = Column(Integer, primary_key=True)
    layer_id = Column(Integer, ForeignKey("layer.id", ondelete="CASCADE"), nullable=False)
    crs = Column(String, nullable=False)

    # Relationship back to Layer
    layer = relationship("Layer", back_populates="crss")

class MapFormat(Base):
    __tablename__ = "map_formats"

    id = Column(Integer, primary_key=True)
    format = Column(String, nullable=False)
