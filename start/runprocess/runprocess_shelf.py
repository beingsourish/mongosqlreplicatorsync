import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from start.config import SQL_SERVER_URI


from start.model.models import Equipment,Base

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
            equipment = Equipment(
                id=str(doc["_id"]),
                name=doc.get("name"),
                type=doc.get("type"),
                partnum=doc.get("partnum")
            )
            session.merge(equipment)
            session.commit()
            logger.info(f"Inserted or updated person: {equipment.id}")

        elif operation == "update":
            doc_id = str(change["documentKey"]["_id"])
            updates = change["updateDescription"]["updatedFields"]
            equipment = session.query(Equipment).filter_by(id=doc_id).first()
            if equipment:
                for key, value in updates.items():
                    setattr(equipment, key, value)
                session.commit()
                logger.info(f"Updated person: {doc_id}")

        elif operation == "delete":
            doc_id = str(change["documentKey"]["_id"])
            equipment = session.query(Equipment).filter_by(id=doc_id).first()
            if equipment:
                session.delete(equipment)
                session.commit()
                logger.info(f"Deleted person: {doc_id}")

    except Exception as e:
        logger.error(f"Error processing {operation}: {e}", exc_info=True)

    finally:
        session.close()