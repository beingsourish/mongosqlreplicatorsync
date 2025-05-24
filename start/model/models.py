from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class Equipment(Base):
    __tablename__ = 'equipment'

    id = Column(String(50), primary_key=True)
    name = Column(String(100))
    type = Column(Integer)
    partnum = Column(DateTime)

    @staticmethod
    def equipment(doc):
        return Equipment(
            id=str(doc["_id"]),
            name=doc.get("name"),
            type=doc.get("type"),
            partnum=doc.get("partnum")
        )


class Slot(Base):
    __tablename__ = 'slot'

    id = Column(String(50), primary_key=True)
    slot_name = Column(String(100))
    slot_type = Column(Integer)
    shelf_id = Column(DateTime)

    @staticmethod
    def slot(doc):
        return Equipment(
            id=str(doc["_id"]),
            slot_name=doc.get("slot_name"),
            slot_type=doc.get("slot_type"),
            shelf_id=doc.get("shelf_id")
        )
