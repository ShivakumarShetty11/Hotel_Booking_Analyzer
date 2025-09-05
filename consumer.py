from kafka import KafkaConsumer
from hdfs import InsecureClient

# === HDFS settings ===
HDFS_URL = "http://localhost:9870"   # WebHDFS or NameNode HTTP address
HDFS_USER = "hdfs"                   # HDFS user
CSV_PATH = "/hotel_booking.csv"

# === Column headers ===
HEADERS = (
    "hotel,is_canceled,lead_time,arrival_date_year,arrival_date_month,"
    "arrival_date_week_number,arrival_date_day_of_month,stays_in_weekend_nights,"
    "stays_in_week_nights,adults,children,babies,meal,country,market_segment,"
    "distribution_channel,is_repeated_guest,previous_cancellations,"
    "previous_bookings_not_canceled,reserved_room_type,assigned_room_type,"
    "booking_changes,deposit_type,agent,company,days_in_waiting_list,customer_type,"
    "adr,required_car_parking_spaces,total_of_special_requests,reservation_status,"
    "reservation_status_date"
)

# === HDFS client ===
client = InsecureClient(HDFS_URL, user=HDFS_USER)

# === Kafka consumer ===
consumer = KafkaConsumer(
    "local-to-hdfs",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",     # start from beginning if no offset
    enable_auto_commit=True,
    group_id="hdfs-writer-group",
    value_deserializer=lambda v: v.decode("utf-8")
)

print("Listening to Kafka and appending rows into HDFS CSV...")

# === Ensure headers exist in HDFS file ===
try:
    if not client.status(CSV_PATH, strict=False):
        # File doesn't exist → create and write headers
        with client.write(CSV_PATH, encoding="utf-8") as writer:
            writer.write(HEADERS + "\n")
        print(f"[INIT] Created {CSV_PATH} with headers")
except Exception as e:
    print(f"[WARN] Could not check/create CSV file: {e}")

# === Stream records from Kafka into HDFS ===
for message in consumer:
    row = message.value.strip()

    try:
        with client.write(CSV_PATH, encoding="utf-8", append=True) as writer:
            writer.write(row + "\n")

        print(f"[APPENDED] {row}")
    except Exception as e:
        print(f"[ERROR] Failed to append row: {e}")
