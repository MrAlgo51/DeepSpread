import sqlite3
from modules.config import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Step 0: Drop old backup if it exists
cursor.execute("DROP TABLE IF EXISTS mempool_logs_old")

# Step 1: Rename existing table
cursor.execute("ALTER TABLE mempool_logs RENAME TO mempool_logs_old")

# Step 2: Create new table without bucket columns
cursor.execute("""
CREATE TABLE mempool_logs (
    timestamp TEXT PRIMARY KEY,
    unconfirmed_tx INTEGER,
    mempool_size INTEGER,
    median_fee REAL
)
""")

# Step 3: Copy clean data into new table
cursor.execute("""
INSERT INTO mempool_logs (timestamp, unconfirmed_tx, mempool_size, median_fee)
SELECT timestamp, unconfirmed_tx, mempool_size, median_fee
FROM mempool_logs_old
""")

# Step 4: Drop backup
cursor.execute("DROP TABLE mempool_logs_old")

conn.commit()
conn.close()
print("✅ Buckets dropped and mempool_logs rebuilt")
