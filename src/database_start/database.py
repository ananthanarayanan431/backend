import sqlite3

from .models import (ShipmentCreate, ShipmentRead, ShipmentStatus,
                     ShipmentUpdate)


class Database:

    def __init__(self) -> None:
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """creating a table"""
        self.cur.execute(
            """ 
            CREATE TABLE IF NOT EXISTS shipment (
                id INTEGER PRIMARY KEY,
                content TEXT,
                weight REAL,
                destination TEXT,
                status TEXT
            )
        """
        )

    def create(self, shipment: ShipmentCreate) -> int:
        """create a new shipment data"""

        self.cur.execute("SELECT MAX(id) from shipment")
        result = self.cur.fetchone()
        new_id = 1 if result is None or result[0] is None else int(result[0]) + 1
        self.cur.execute(
            """ 
           INSERT INTO shipment 
           VALUES (:id, :content, :weight, :destination, :status)
        """,
            {
                "id": new_id,
                "content": shipment.content,
                "weight": shipment.weight,
                "destination": shipment.destination,
                "status": "placed",
            },
        )
        self.conn.commit()
        return new_id

    def get(self, id: int) -> ShipmentRead | None:
        """get the shipment details for given ID"""

        self.cur.execute(
            """ 
            SELECT id, content, weight, destination, status from shipment
            where id = ?
        """,
            (id,),
        )
        row = self.cur.fetchone()

        if not row:
            return None

        return ShipmentRead(
            content=row[1],
            weight=row[2],
            destination=row[3] or "",
            status=ShipmentStatus(row[4]),
        )

    def update(self, id: int, shipment: ShipmentUpdate) -> ShipmentRead | None:
        """Update the shipment data"""

        self.cur.execute(
            """ 
            UPDATE shipment SET status = :status
            WHERE id = :id
        """,
            {"id": id, "status": shipment.status.value},
        )
        self.conn.commit()
        result = self.get(id)
        if result is None:
            raise ValueError(f"Shipment with id {id} not found after update")
        return ShipmentRead(
            content=result.content,
            weight=result.weight,
            destination=result.destination,
            status=result.status,
        )

    def delete(self, id: int):
        """delete the data item in the table"""
        self.cur.execute(
            """
            DELETE FROM shipment
            where id = ?
        """,
            (id,),
        )
        self.conn.commit()

    def close(self):
        """close the connection"""
        self.conn.close()
