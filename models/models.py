from sqlalchemy import MetaData, Table, Column, Integer, String, JSON, TIMESTAMP, ForeignKey
from datetime import datetime

metadata = MetaData()

roles = Table(
    "roles",
    metadata,
    Column('id', Integer, primary_key=True),  # unique key
    Column('name', String, nullable=False),  # can't be empty/null
    Column('permissions', JSON),

)

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String ,nullable=False),
    Column('username', String, nullable=False),
    Column('password', String, nullable=False),
    Column('registered_at', TIMESTAMP, default=datetime.utcnow()),
    Column('role_id', Integer, ForeignKey("roles.id")), # referring to roles table's 'id' 
   
)