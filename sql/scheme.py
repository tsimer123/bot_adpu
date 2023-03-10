from sqlalchemy.orm import DeclarativeBase
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String, ForeignKey, DateTime, Text, BigInteger

from datetime import datetime

from .engine import engine


class Base(DeclarativeBase):
     pass

class Users(Base):
     __tablename__ = "users"

     users_id: Mapped[int] = mapped_column(primary_key=True)
     user_id_tg: Mapped[int] = mapped_column(BigInteger)
     tg_name: Mapped[str] = mapped_column(String(100))
     full_name: Mapped[str] = mapped_column(String(100))
     created_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)
     update_on: Mapped[Optional[datetime]] = mapped_column(DateTime(), default=datetime.now, onupdate=datetime.now)
     
     logmessages: Mapped[List["LogMessage"]] = relationship(back_populates="users")

class LogMessage(Base):
     __tablename__ = "logmessage"

     logmessage_id:Mapped[int] = mapped_column(primary_key=True)
     users_id = mapped_column(ForeignKey("users.users_id"))
     created_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)
     type_message: Mapped[str] = mapped_column(String(10))
     message: Mapped[str] = mapped_column(Text())

     users: Mapped[List["Users"]] = relationship(back_populates="logmessages")

class Contracts(Base):
     __tablename__ = "contracts"

     contracts_id: Mapped[int] = mapped_column(primary_key=True)
     yoda_contract_id: Mapped[str] = mapped_column(String(36))
     name_contract: Mapped[str] = mapped_column(Text())

class Equipments(Base):
     __tablename__ = "equipments"

     equipments_id: Mapped[int] = mapped_column(primary_key=True)
     yoda_networkequipments_id: Mapped[str] = mapped_column(String(36))
     yoda_task_id: Mapped[str] = mapped_column(String(36))
     number_equipment: Mapped[str] = mapped_column(String(30))
     type_equipment: Mapped[str] = mapped_column(String(30))
     model_equipment: Mapped[str] = mapped_column(String(150))
     latitude: Mapped[str] = mapped_column(String(20))
     longitude: Mapped[str] = mapped_column(String(20))


def create_db():
     Base.metadata.create_all(engine)     
