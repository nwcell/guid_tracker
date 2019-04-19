from datetime import datetime, timedelta
import sqlalchemy


def _default_expire():
    return datetime.now() + timedelta(days=30)


# Database table definitions.
metadata = sqlalchemy.MetaData()

guid_tracker = sqlalchemy.Table(
    "guid_tracker",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("expire", sqlalchemy.DateTime),
)
