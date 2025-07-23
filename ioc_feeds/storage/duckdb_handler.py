import duckdb
from loguru import logger
from pathlib import Path
import pandas as pd


class DuckDBHandler:
    def __init__(self, db_path: str, csv_backup: str | None = None):
        self.db_path = db_path
        self.csv_backup = csv_backup
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(db_path)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ioc (
                type VARCHAR,
                value VARCHAR,
                source VARCHAR,
                threat_type VARCHAR,
                timestamp TIMESTAMP
            )
            """
        )

    def insert_many(self, records: list[dict]):
        if not records:
            logger.info("No records to insert")
            return
        df = pd.DataFrame(records)
        self.conn.execute("INSERT INTO ioc SELECT * FROM df")
        logger.info("Inserted {} records into DuckDB", len(records))
        if self.csv_backup:
            df.to_csv(self.csv_backup, mode="a", header=not Path(self.csv_backup).exists(), index=False)
            logger.info("Appended {} records to CSV backup", len(records))
