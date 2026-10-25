"""A tiny SQLite-backed catalog seeded with fictional demo products."""
import sqlite3
from .models import Product

_SEED = [
    # name, category, store, price, brand, tags, distance_km, rating
    ("Long-grain rice 1kg", "rice", "FreshMart", 320, "Golden", "gluten-free", 2.0, 4.2),
    ("Basmati rice 1kg", "rice", "ValueBasket", 410, "Royal", "gluten-free", 6.5, 4.6),
    ("Brown rice 1kg", "rice", "GreenGrocer", 450, "Golden", "gluten-free,wholegrain", 11.0, 4.4),
    ("Whole milk 1L", "milk", "FreshMart", 290, "Pasture", "dairy", 2.0, 4.0),
    ("Oat milk 1L", "milk", "GreenGrocer", 520, "OatLand", "vegan", 11.0, 4.3),
    ("Skim milk 1L", "milk", "ValueBasket", 270, "Pasture", "dairy", 6.5, 3.8),
    ("Peanut butter 340g", "peanut butter", "FreshMart", 640, "Nutty", "nuts", 2.0, 4.5),
    ("Sunflower spread 340g", "peanut butter", "ValueBasket", 580, "Sunny", "seeds", 6.5, 3.9),
    ("Wheat bread loaf", "bread", "FreshMart", 180, "Hearth", "gluten", 2.0, 4.1),
    ("Gluten-free bread loaf", "bread", "GreenGrocer", 390, "PureBake", "gluten-free", 11.0, 4.0),
    ("Free-range eggs x10", "eggs", "ValueBasket", 560, "Farmhand", "eggs", 6.5, 4.7),
    ("Standard eggs x10", "eggs", "FreshMart", 470, "Farmhand", "eggs", 2.0, 4.0),
]


class Catalog:
    def __init__(self):
        self.db = sqlite3.connect(":memory:")
        self.db.execute(
            "CREATE TABLE p (name, category, store, price REAL, brand, tags, dist REAL, rating REAL)"
        )
        self.db.executemany("INSERT INTO p VALUES (?,?,?,?,?,?,?,?)", _SEED)

    def categories(self):
        return [r[0] for r in self.db.execute("SELECT DISTINCT category FROM p")]

    def by_category(self, category):
        rows = self.db.execute("SELECT * FROM p WHERE category = ?", (category,))
        return [
            Product(n, c, s, pr, b, frozenset(t.split(",")), d, r)
            for n, c, s, pr, b, t, d, r in rows
        ]
