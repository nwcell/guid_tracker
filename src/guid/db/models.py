"""Define tables."""
from datetime import datetime, timedelta
import sqlalchemy


# Database table definitions.
metadata = sqlalchemy.MetaData()

guid_tracker = sqlalchemy.Table(
    'guid_tracker',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.String, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String),
    sqlalchemy.Column('expire', sqlalchemy.DateTime),
)
