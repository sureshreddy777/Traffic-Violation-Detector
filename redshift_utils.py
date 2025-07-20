import os
import psycopg2
import uuid
from datetime import datetime
from dotenv import load_dotenv
import traceback

# Load environment variables from .env
load_dotenv()

def insert_violation(username, license_plate, violation_type, description):
    try:
        print("🔌 Connecting to Redshift...")

        # Extract connection details
        redshift_host = os.getenv("REDSHIFT_HOST")  # Should NOT include port or /dev
        redshift_db = os.getenv("REDSHIFT_DB")
        redshift_user = os.getenv("REDSHIFT_USER")
        redshift_password = os.getenv("REDSHIFT_PASSWORD")
        redshift_port = int(os.getenv("REDSHIFT_PORT"))

        # Print host info for verification (optional)
        print(f"Host: {redshift_host}, DB: {redshift_db}, Port: {redshift_port}, User: {redshift_user}")

        # Connect to Redshift
        conn = psycopg2.connect(
            host=redshift_host,
            dbname=redshift_db,
            user=redshift_user,
            password=redshift_password,
            port=redshift_port
        )

        cur = conn.cursor()

        # Generate UUID and timestamp
        violation_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()

        print("📥 Inserting data into traffic_violations table...")
        print(f"ID: {violation_id}, User: {username}, Plate: {license_plate}, Type: {violation_type}, Time: {timestamp}")

        # Insert the violation data
        cur.execute("""
            INSERT INTO traffic_violations (
                id, username, license_plate, violation_type, description, timestamp
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            violation_id,
            username,
            license_plate,
            violation_type,
            description,
            timestamp
        ))

        conn.commit()
        print("✅ Data inserted successfully!")

        cur.close()
        conn.close()

    except Exception as e:
        print("❌ Error inserting into Redshift:", e)
        traceback.print_exc()
