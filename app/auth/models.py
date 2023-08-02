from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, String, sql
from ..db import Base, get_session

class User(SQLAlchemyBaseUserTableUUID, Base):
    name = Column(
            String(length=100), # type: ignore
            server_default=sql.expression.literal("No name given"),
            nullable=False,
        )
    
async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User) ## type: ignore