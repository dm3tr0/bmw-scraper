import sqlite3
from scrapy.exceptions import DropItem


class SQLitePipeline:
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
        
        # checks if car exist in db
        if self.curr.rowcount == 0:
            spider.logger.info(f"Duplicate skipped: {item.get('registration')} already in database.")
        else:
            self.conn.commit()
            spider.logger.info(f"Saved new car: {item.get('registration')} - {item.get('name')}")
        return item

    def close_spider(self, spider):
        self.conn.close()


class DataCleaningPipeline:
    def process_item(self, item, spider):
        required_fields = ['model', 'name', 'registration']
        for field in required_fields:
            if not item.get(field):
                spider.logger.warning(f"Dropped item due to missing {field}: {item.get('link')}")
                raise DropItem(f"Missing required field: {field}")

        if item.get('mileage'):
            try:
                clean_mileage = str(item['mileage']).replace(',', '')
                item['mileage'] = int(clean_mileage)
            except ValueError:
                item['mileage'] = None 

        if item.get('fuel'):
            item['fuel'] = str(item['fuel']).lower()

        return item