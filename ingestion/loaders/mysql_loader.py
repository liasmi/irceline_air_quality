import pandas as pd
import sqlalchemy as sa
import logging
from sqlalchemy import create_engine
from ingestion.config import mysql_config

logger = logging.getLogger(__name__)

def get_mysql_engine():
    """Create and return MySQL database engine"""
    connection_string = f"mysql+pymysql://{mysql_config.username}:{mysql_config.password}@{mysql_config.host}:{mysql_config.port}/{mysql_config.database}"
    return create_engine(connection_string)

def load_to_mysql(df, table_name):
    """Load DataFrame to MySQL table"""

    logger.info(f"Loading {len(df)} rows to table {table_name}")
    # Check if dataframe is empty
    if df.empty:
        logger.warning(f"Skipping {table_name}: DataFrame is empty")
        print(f"⚠️  Skipping {table_name}: DataFrame is empty")
        return

    try:
        engine = get_mysql_engine()

        # Create table if it doesn't exist, or replace if it does
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',
            index=False
        )

        logger.info(f"Successfully loaded {len(df)} rows into {table_name}")
        print(f"✅ Loaded {len(df)} rows into {table_name}")

    except Exception as e:
        logger.error(f"Failed to load {table_name}: {e}")
        print(f"❌ Error loading {table_name}: {e}")
        raise