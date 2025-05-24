from start.sync import start_sync,stop_sync
import time
if __name__ == "__main__":
    start_sync()
    print("🔁 Real-time sync started. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🧹 Gracefully stopping sync...")
        stop_sync()
        print("✅ Sync stopped.")