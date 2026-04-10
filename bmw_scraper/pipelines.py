import logging
import sqlite3

class SQLitePipeline:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def open_spider(self, spider):
        self.conn = sqlite3.connect('bmw_cars.db')
        self.curr = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.curr.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                registration TEXT PRIMARY KEY NOT NULL,
                link TEXT NOT NULL,
                model TEXT NOT NULL,
                name TEXT NOT NULL,
                mileage INTEGER,
                registered TEXT,
                engine TEXT,
                range TEXT,
                exterior TEXT,
                fuel TEXT,
                transmission TEXT,
                upholstery TEXT
            )
        """)

    def process_item(self, item, spider):
        self.curr.execute("""
            INSERT OR IGNORE INTO cars VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            item.get('registration'), item.get('link'), item.get('model'), item.get('name'),
            item.get('mileage'), item.get('registered'), item.get('engine'),
            item.get('range'), item.get('exterior'), item.get('fuel'),
            item.get('transmission'), item.get('upholstery'),
        ))
        self.conn.commit()
        self.logger.info(f"Saved car {item.get('registration')} - {item.get('name')}")
        return item

    def close_spider(self, spider):
        self.conn.close()