from pymongo import MongoClient

import logger
from concurrent.futures import ThreadPoolExecutor
import threading

from start.config import MONGO_COLLECTION, MONGO_URI, MONGO_DB
from start.runprocess import runprocess_shelf,runprocess_slot
from start import runprocess

logger=logger.get_logger(__name__)
executor = ThreadPoolExecutor(max_workers=3)
stop_event = threading.Event()
futures=[]
from start.runprocess.runprocess_shelf import *
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
def watch_changes(collection):
    print("watch_changes")

    try:
        with collection.watch(full_document='updateLookup') as stream:

            for change in stream:

                if stop_event.is_set():

                    logger.info("🛑 Stop signal received. Exiting watch loop.")
                    break

                logger.info("<UNK> Change stream: {}".format(change))
                #print(collection)
                if collection.name=='equipment':
                   runprocess_shelf.process_change(collection,change)
                if collection.name=='slot':
                   runprocess_slot.process_change(collection,change)

    except Exception as e:
        logger.exception("💥 Error in watch_changes: %s", e)


def start_sync():
    logger.info("🔄 Submitting watch_changes to thread pool")
    for collection_list in MONGO_COLLECTION:
        print(collection_list)

        collection = db[collection_list]
        future = executor.submit(watch_changes, collection)
        futures.append(future)
        logger.info(f"🔄 Started sync for {collection}")

def stop_sync():
    stop_event.set()
    logger.info("🧹 Stop signal sent")
    executor.shutdown(wait=True)
    logger.info("🧼 Thread pool shut down")