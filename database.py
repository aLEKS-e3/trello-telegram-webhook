import os
import asyncpg

from dotenv import load_dotenv


load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_NAME")


async def create_table() -> None:
    conn = await asyncpg.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )

    create_table_query = """
            CREATE TABLE IF NOT EXISTS telegram_users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                username VARCHAR(50) UNIQUE
            )
        """
    await conn.execute(create_table_query)
    await conn.close()


async def write_user_to_db(name: str, username: str) -> None:
    conn = await asyncpg.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )

    insert_query = """
        INSERT INTO telegram_users (name, username)
        VALUES ($1, $2)
        ON CONFLICT (username) DO UPDATE
        SET name = EXCLUDED.name;
    """
    await conn.execute(insert_query, name, username)
    await conn.close()
