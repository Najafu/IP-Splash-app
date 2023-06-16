import sqlite3
from contextlib import contextmanager


class Model:
    def __init__(self, database="test.db") -> None:

        self.database = database
        self.connection = None
        self.cursor = None
        self._create_table()

    @contextmanager
    def db_control(self):
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        yield
        self.connection.commit()
        self.connection.close()

    def _create_table(self):
        # "name", "ip_address", "subnet_mask", "gateway", "id"
        with self.db_control():
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS ipsplash (name TEXT NOT NULL, ip_address TEXT NOT NULL, subnet_mask TEXT NOT NULL, gateway TEXT NOT NULL, id INTEGER PRIMARY KEY AUTOINCREMENT)"
            )

    def fetch_all_data(self):
        with self.db_control():
            self.cursor.execute("SELECT * FROM ipsplash")
            result = self.cursor.fetchall()
        return result

    def fetch_filtered_data(self, order_by=None, search_value=None):
        with self.db_control():
            if order_by and search_value:
                self.cursor.execute(f"SELECT * FROM ipsplash WHERE name LIKE '%' || ? || '%' OR ip_address LIKE '%' || ? || '%' ORDER BY {order_by[0]} {order_by[1]};",(search_value, search_value))  # i know!!
            elif order_by:
                self.cursor.execute(
                    f"SELECT * FROM ipsplash ORDER BY {order_by[0]} {order_by[1]};"
                )
            else:
                self.cursor.execute("SELECT * FROM ipsplash WHERE name LIKE '%' || ? || '%' OR ip_address LIKE '%' || ? || '%'",(search_value, search_value))
            result = self.cursor.fetchall()
        return result

    def insert(self, values):
        with self.db_control():
            self.cursor.execute(
                "INSERT INTO ipsplash (name, ip_address, subnet_mask, gateway) VALUES (?,?,?,?)",
                values,
            )

    def delete(self, item_id):
        with self.db_control():
            self.cursor.execute("DELETE FROM ipsplash WHERE id=?", (item_id,))

    def update(self, values):
        with self.db_control():
            self.cursor.execute(
                "UPDATE ipsplash SET name=?, ip_address=?, subnet_mask=?, gateway=? WHERE id=?",
                values,
            )
