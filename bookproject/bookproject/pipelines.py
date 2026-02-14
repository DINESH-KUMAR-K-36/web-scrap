# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
import scrapy

class BookprojectPipeline:

    def __init__(self):
        self.conn = sqlite3.connect("books.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE,
                price REAL,
                rating TEXT
            )
        """)
        self.conn.commit()
        self.book_titles_seen = set()

    def process_item(self, item, spider):
         if spider.name == "books":
            if item["title"] in self.book_titles_seen:
                raise scrapy.exceptions.DropItem(f"Duplicate item: {item['title']}")
            self.book_titles_seen.add(item["title"])
            if item["title"]:
                item["title"] = item["title"].strip()
            if item["price"]:
                item["price"] = float(item["price"].replace("£", "").strip())
            if item["rating"]:
                item["rating"] = item["rating"].split()[-1]
            self.cursor.execute("INSERT OR IGNORE INTO books (title, price, rating) VALUES (?, ?, ?)",
                                (item["title"], item["price"], item["rating"]))
            self.conn.commit()
         elif spider.name =="quotes":
                if item["text"]:
                    item["text"] = item["text"].strip()
                if item["author"]:
                    item["author"] = item["author"].strip()
                item["tags"] = [tag.strip() for tag in item.get("tags", [])]     
                return item

    def close_spider(self, spider):
        self.conn.close()
