import sqlite3


def init_db():
    conn = sqlite3.connect("database/pizza_shop.db")
    c = conn.cursor()

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS crust (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )"""
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS sauce (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )   
        """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS cheese (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS meat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS vegetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS additional (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS seasoning (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            pizza TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


def insert_ingredients(type_to_ingre: dict) -> None:
    conn = sqlite3.connect("database/pizza_shop.db")
    c = conn.cursor()
    for typ, ingredients in type_to_ingre.items():
        for ingre in ingredients:
            query = f"INSERT INTO {typ} (name) VALUES (?)"
            c.execute(query, (ingre,))
    conn.commit()
    conn.close()


def get_ingredients_by_type(typ: str) -> list:
    conn = sqlite3.connect("database/pizza_shop.db")
    c = conn.cursor()
    c.execute(f"SELECT * FROM {typ}")
    result = []
    for _, item in c.fetchall():
        result.append(item)
    conn.commit()
    conn.close()
    return result
