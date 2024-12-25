from sqlalchemy.orm import Session
from sqlalchemy import func

from . import models

def get_layers(db: Session):
    return db.query(models.Layer).all()

def get_map_formats(db: Session):
    return db.query(models.MapFormat).all()