import sqlite3

conn = sqlite3.connect("image_features.db")
cursor = conn.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_image TEXT,
    keypoints BLOB,
    descriptors BLOB
)
"""
,)

conn.commit()
