import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from start.config import MONGO_URI, MONGO_DB, MONGO_COLLECTION, SQL_SERVER_URI


from start.models import Base,Slot

logger = logging.getLogger(__name__)

# MongoDB setup


# SQL Server setup
engine = create_engine(SQL_SERVER_URI, echo=False)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def process_change(collection,change):
    session = Session()
    operation = change["operationType"]
    logger.info(f"Received {operation} operation: {change}")

    try:
        if operation == "insert":
            doc = change["fullDocument"]
            slot = Slot(
                id=str(doc["_id"]),
                slot_name=doc.get("slot_name"),
                slot_type=doc.get("slot_type"),
                shelf_id=doc.get("shelf_id")
            )
            session.merge(slot)
            session.commit()
            logger.info(f"Inserted or updated person: {slot.id}")

        elif operation == "update":
            doc_id = str(change["documentKey"]["_id"])
            updates = change["updateDescription"]["updatedFields"]
            equipment = session.query(Slot).filter_by(id=doc_id).first()
            if equipment:
                for key, value in updates.items():
                    setattr(equipment, key, value)
                session.commit()
                logger.info(f"Updated person: {doc_id}")

        elif operation == "delete":
            doc_id = str(change["documentKey"]["_id"])
            equipment = session.query(Slot).filter_by(id=doc_id).first()
            if equipment:
                session.delete(equipment)
                session.commit()
                logger.info(f"Deleted person: {doc_id}")

    except Exception as e:
        logger.error(f"Error processing {operation}: {e}", exc_info=True)

    finally:
        session.close()