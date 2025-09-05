import argparse, os, sys
from sqlalchemy import create_engine
from dotenv import load_dotenv

def get_engine():
    load_dotenv()
    url = os.getenv("DATABASE_URL")
    if not url:
        print("DATABASE_URL not set. Create a .env file from .env.example.", file=sys.stderr)
        sys.exit(1)
    return create_engine(url, future=True)

def run_sql(engine, sql_text):
    with engine.begin() as conn:
        conn.exec_driver_sql(sql_text)

def init_db(engine):
    schema_path = os.path.join(os.path.dirname(__file__), "..", "sql", "schema.sql")
    with open(schema_path, "r") as f:
        schema_sql = f.read()
    run_sql(engine, schema_sql)
    print("Tables created or verified.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true", help="Create tables")
    args = parser.parse_args()

    engine = get_engine()
    if args.init:
        init_db(engine)

if __name__ == "__main__":
    main()
