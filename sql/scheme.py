from sqlalchemy.orm import DeclarativeBase
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String, ForeignKey, DateTime, Text, BigInteger, Boolean
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
     activity: Mapped[Optional[datetime]] = mapped_column(DateTime())
     traffic: Mapped[Optional[str]] = mapped_column(String(15))
     operator: Mapped[str] = mapped_column(String(20))
     imei: Mapped[Optional[str]] = mapped_column(String(20))
     hash_data: Mapped[str] = mapped_column(String(100))
     state_in_lk: Mapped[str] = mapped_column(String(15))
     last_upload: Mapped[datetime] = mapped_column(DateTime())
     created_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)
     update_on: Mapped[Optional[datetime]] = mapped_column(DateTime(), default=datetime.now, onupdate=datetime.now)

     updatesimlog: Mapped[List["UpdateSimLog"]] = relationship(back_populates="sims")


class ImportSimsLog(Base):
     __tablename__ = "importsimslog"

     importsimslog_id: Mapped[int] = mapped_column(primary_key=True)
     start_import: Mapped[str] = mapped_column(DateTime())
     name_file: Mapped[str] = mapped_column(Text())
     state: Mapped[Optional[str]] = mapped_column(String(20))
     count_import_sim: Mapped[Optional[int]]
     count_sim_file: Mapped[Optional[int]]
     description: Mapped[Optional[str]] = mapped_column(Text())
     error_import: Mapped[Optional[str]] = mapped_column(Text())
     created_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)

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
     state_in_lk: Mapped[Optional[str]] = mapped_column(String(15))
     created_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)


     sims: Mapped[List["Sims"]] = relationship(back_populates="updatesimlog")
     importsimslog: Mapped[List["ImportSimsLog"]] = relationship(back_populates="updatesimlog")


class Dirs(Base):
     __tablename__ = "dirs"

     dirs_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
     name_dir: Mapped[str]
     state: Mapped[Optional[str]] = mapped_column(String(50))
     created_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)
     update_on: Mapped[Optional[datetime]] = mapped_column(DateTime(), default=datetime.now, onupdate=datetime.now)

     contentsdirs: Mapped[List["ContentsDirs"]] = relationship(back_populates="dirs")


class ContentsDirs(Base):
     __tablename__ = "contentsdirs"

     contentsdirs_id: Mapped[int] = mapped_column(primary_key=True)
     dirs_id = mapped_column(ForeignKey("dirs.dirs_id"))
     name_obj: Mapped[str]
     additions: Mapped[Optional[str]]
     state: Mapped[Optional[str]] = mapped_column(String(50))
     created_on: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)
     update_on: Mapped[Optional[datetime]] = mapped_column(DateTime(), default=datetime.now, onupdate=datetime.now)

     dirs: Mapped[List["Dirs"]] = relationship(back_populates="contentsdirs")
    
class SimCards(Base):
     __tablename__ = "simcards"

     simcards_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
     operator: Mapped[str] = mapped_column(Text())
     iccid: Mapped[str] = mapped_column(Text())
     msisdn: Mapped[str] = mapped_column(Text())
     ip: Mapped[str | None] = mapped_column(Text())
     apn: Mapped[Optional[str]] = mapped_column(Text())
     apnusername: Mapped[Optional[str]] = mapped_column(Text())
     password: Mapped[Optional[str]] = mapped_column(Text())
     issued: Mapped[Optional[str]] = mapped_column(Text())
     date_receipt:Mapped[Optional[datetime]] = mapped_column(DateTime(), default=datetime.now, onupdate=datetime.now)

class Meter(Base):
     __tablename__ = "meter"

     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
     user_id: Mapped[int] = mapped_column(Text())
     username: Mapped[str | None] = mapped_column(Text())
     first_name: Mapped[str | None] = mapped_column(Text())
     last_name: Mapped[str | None] = mapped_column(Text())
     number_meter: Mapped[str] = mapped_column(Text())
     imei: Mapped[str] = mapped_column(Text())
     iccid1: Mapped[str] = mapped_column(Text())
     iccid2: Mapped[str | None] = mapped_column(Text())
     latitude: Mapped[str] = mapped_column(Text())
     longitude: Mapped[str] = mapped_column(Text())
     montag: Mapped[datetime] = mapped_column(
          DateTime(), default=datetime.now, onupdate=datetime.now
     )
     power: Mapped[Boolean] = mapped_column(Boolean())
     created_on: Mapped[datetime] = mapped_column(
        DateTime(), default=datetime.now, onupdate=datetime.now
     )
     state_meter: Mapped[str | None] = mapped_column(Text())

def create_db():
     Base.metadata.create_all(engine)     
