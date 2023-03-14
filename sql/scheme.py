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
     number_sim_1: Mapped[Optional[str]] = mapped_column(String(11))
     iccid_1: Mapped[Optional[str]] = mapped_column(String(20))
     operator_1: Mapped[Optional[str]] = mapped_column(String(20))
     number_sim_2: Mapped[Optional[str]] = mapped_column(String(11))
     iccid_2: Mapped[Optional[str]] = mapped_column(String(20))
     operator_2: Mapped[Optional[str]] = mapped_column(String(20))
     number_sim_3: Mapped[Optional[str]] = mapped_column(String(11))
     iccid_3: Mapped[Optional[str]] = mapped_column(String(20))
     operator_3: Mapped[Optional[str]] = mapped_column(String(20))


class Sims(Base):
     __tablename__ = "sims"

     sims_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
     number_tel: Mapped[str] = mapped_column(String(11))
     iccid: Mapped[str] = mapped_column(String(20))
     apn: Mapped[Optional[str]] = mapped_column(Text())
     ip: Mapped[Optional[str]] = mapped_column(String(15))
     state: Mapped[str] = mapped_column(String(100))
     activity: Mapped[Optional[str]] = mapped_column(DateTime())
     traffic: Mapped[Optional[str]] = mapped_column(String(15))
     operator: Mapped[str] = mapped_column(String(20))
     created_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)
     update_on: Mapped[Optional[datetime]] = mapped_column(DateTime(), default=datetime.now, onupdate=datetime.now)

     updatesimlog: Mapped[List["UpdateSimLog"]] = relationship(back_populates="sims")

class ImportSimsLog(Base):
     __tablename__ = "importsimslog"

     importsimslog_id: Mapped[int] = mapped_column(primary_key=True)
     start_import: Mapped[str] = mapped_column(DateTime())
     name_file: Mapped[str] = mapped_column(Text())
     state: Mapped[str] = mapped_column(String(10))
     count_import_sim: Mapped[int]
     error_import: Mapped[Optional[str]] = mapped_column(Text())

     updatesimlog: Mapped[List["UpdateSimLog"]] = relationship(back_populates="importsimslog")


class UpdateSimLog(Base):
     __tablename__ = "updatesimlog"

     updatesimlog_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
     sims_id = mapped_column(ForeignKey("sims.sims_id"))
     importsimslog_id = mapped_column(ForeignKey("importsimslog.importsimslog_id"))
     number_tel: Mapped[Optional[str]] = mapped_column(String(11))
     iccid: Mapped[Optional[str]] = mapped_column(String(20))
     apn: Mapped[Optional[str]] = mapped_column(Text())
     ip: Mapped[Optional[str]] = mapped_column(String(15))
     state: Mapped[Optional[str]] = mapped_column(String(100))
     activity: Mapped[Optional[str]] = mapped_column(DateTime())
     traffic: Mapped[Optional[str]] = mapped_column(String(15))
     operator: Mapped[Optional[str]] = mapped_column(String(20))
     created_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)


     sims: Mapped[List["Sims"]] = relationship(back_populates="updatesimlog")
     importsimslog: Mapped[List["ImportSimsLog"]] = relationship(back_populates="updatesimlog")


def create_db():
     Base.metadata.create_all(engine)     
