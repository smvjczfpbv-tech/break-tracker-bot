import aiosqlite
from datetime import datetime

DB_NAME = "break_tracker.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS breaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT,
            comment TEXT
        )
        """)

        await db.commit()


async def get_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )
        return await cursor.fetchone()


async def add_user(user_id, name):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO users (user_id, name) VALUES (?, ?)",
            (user_id, name)
        )
        await db.commit()


async def start_break(user_id):
    now = datetime.now().strftime("%H:%M")

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT INTO breaks (user_id, start_time)
            VALUES (?, ?)
            """,
            (user_id, now)
        )
        await db.commit()

    return now


async def get_active_break(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT id, start_time
            FROM breaks
            WHERE user_id = ?
            AND end_time IS NULL
            ORDER BY id DESC
            LIMIT 1
            """,
            (user_id,)
        )

        return await cursor.fetchone()


async def finish_break(user_id, comment):
    now = datetime.now().strftime("%H:%M")

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            UPDATE breaks
            SET end_time = ?, comment = ?
            WHERE user_id = ?
            AND end_time IS NULL
            """,
            (now, comment, user_id)
        )

        await db.commit()

    return now


async def get_today_breaks(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT start_time, end_time, comment
            FROM breaks
            WHERE user_id = ?
            AND end_time IS NOT NULL
            """,
            (user_id,)
        )

        return await cursor.fetchall()


async def clear_breaks(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "DELETE FROM breaks WHERE user_id = ?",
            (user_id,)
        )
        await db.commit()
