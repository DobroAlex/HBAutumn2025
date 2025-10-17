"""
test_2 won't ever work properly if test_1 either wasn't executed or failed to create a DB.

Running this test with two workers ( n >= 2) will produce flaky results
"""

import contextlib
import sqlite3
from pathlib import Path

ORDER_DEPENDANT_DB_NAME = Path(__file__).parent / "order_dependant_db.sql"
# Remove this file before running this test file
# I can't be bothered with


def test_order_dependant_1():
    with contextlib.closing(sqlite3.connect(ORDER_DEPENDANT_DB_NAME)) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute("DROP TABLE IF EXISTS RECORDS")
            cursor.execute("CREATE TABLE IF NOT EXISTS RECORDS ( Person VARCHAR(255) NOT NULL) ")
            cursor.execute("INSERT INTO RECORDS (Person) VALUES ('Alice')")
            connection.commit()


def test_order_dependant_2():
    with contextlib.closing(sqlite3.connect(ORDER_DEPENDANT_DB_NAME)) as connection:
        with contextlib.closing(connection.cursor()) as cursor:
            assert cursor.execute("SELECT Person FROM RECORDS").fetchall() == [('Alice',)]
