#%%
import sqlite3
import pandas as pd

# Define the database name
DB_NAME = 'wechat_articles.db'

def setup_database():
    """Initializes the SQLite database and creates the articles table if it doesn't exist."""
    conn = None
    try:
        # Connect to the database (creates the file if it doesn't exist)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Create the articles table
        # Use TEXT for all columns as requested
        # Add IF NOT EXISTS to avoid errors if the script is run multiple times
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_scraped TEXT NOT NULL,
            article_title TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE, -- Added UNIQUE constraint to prevent duplicate URLs
            scraped_at TIMESTAMP DEFAULT (datetime('now', '+8 hours')) -- 使用北京时间 (UTC+8)
        )
        """)

        print(f"Database '{DB_NAME}' initialized and table 'articles' created successfully.")

        # Commit the changes
        conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        if conn:
            conn.close()

def read_articles_to_dataframe():
    """Reads the articles table from the database into a pandas DataFrame."""
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        # SQL query to select all data from the articles table
        query = "SELECT * FROM articles"
        # Use pandas to read the SQL query into a DataFrame
        df = pd.read_sql_query(query, conn)
        print("Successfully read 'articles' table into DataFrame.")
        return df
    except sqlite3.Error as e:
        print(f"An error occurred while reading the database: {e}")
        return None
    except pd.io.sql.DatabaseError as e: # Handle pandas specific SQL errors
        print(f"An error occurred with pandas reading SQL: {e}")
        return None
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    setup_database()
    # Read the articles table into a DataFrame and print it
    articles_df = read_articles_to_dataframe()
    if articles_df is not None:
        print("\nArticles DataFrame:")
        print(articles_df) 