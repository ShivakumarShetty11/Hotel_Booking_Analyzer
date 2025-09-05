import time
import os
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from producer import KafkaProducer

# Directory to watch
WATCH_DIR = "/hotel_bookingd.csv"

# Kafka Producer setup
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: v.encode("utf-8")
)

print(f"🚀 Watching {WATCH_DIR} for new CSV files...")

class CSVHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            filepath = event.src_path
            print(f"[NEW FILE] {filepath}")
            self.process_csv(filepath)

    def process_csv(self, filepath):
        try:
            # Read CSV with pandas
            df = pd.read_csv(filepath)

            # Convert dataframe to list of rows (excluding header)
            for _, row in df.iterrows():
                csv_row = ",".join(map(str, row.values))
                producer.send("local-to-hdfs", value=csv_row)
                print(f"[SENT] {csv_row}")

            producer.flush()
            print(f"[DONE] Streamed {len(df)} rows from {filepath}")

        except Exception as e:
            print(f"[ERROR] Failed to process {filepath}: {e}")

# Setup watchdog
event_handler = CSVHandler()
observer = Observer()
observer.schedule(event_handler, WATCH_DIR, recursive=False)
observer.start()

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    observer.stop()
observer.join()
