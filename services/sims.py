from sqlalchemy import select, func, Result
from sqlalchemy.orm import Session, sessionmaker
from typing import TypedDict, Optional
from datetime import datetime
import re

from sql.engine import engine
from sql.scheme import Sims

Session = sessionmaker(engine)

session = Session()

class SimInfo(TypedDict):
     sims_id: int
     number_tel: Optional[str]
     iccid: Optional[str]
     apn: Optional[str]
     ip: Optional[str]
     state: Optional[str]
     activity: Optional[str]
     traffic: Optional[str]
     operator: Optional[str]
     imei: Optional[str]
     state_in_lk: Optional[str]
     last_upload: Optional[datetime]
     created_on: Optional[datetime]
     update_on: Optional[datetime]
     description: Optional[str]


def get_count_sims() -> int:

    try:
        count_sims = session.scalar(select(func.count()).select_from(Sims))              
    except Exception as ex:
        raise ex
    finally:
        session.close()

    return count_sims


def get_sim_number_tel(number_tel: str) -> SimInfo:

    try:
        sim_info = session.query(Sims).filter(Sims.number_tel == number_tel).first()
        sim_info_format = format_one_sim_info(sim_info)
    except Exception as ex:
        raise ex
    finally:
        session.close()

    return sim_info_format


def get_sim_iccid(iccid: str) -> SimInfo:

    try:
        sim_info = session.query(Sims).filter(Sims.iccid == iccid).first()
        sim_info_format = format_one_sim_info(sim_info)
    except Exception as ex:
        raise ex
    finally:
        session.close()

    return sim_info_format


def format_one_sim_info(sim_info) -> SimInfo:    

    if sim_info is not None:
        dict_sim_info = SimInfo(
            sims_id = sim_info.sims_id,
            number_tel = sim_info.number_tel,
            iccid = sim_info.iccid,
            apn = sim_info.apn,
            ip = sim_info.ip,
            state = sim_info.state,
            activity = sim_info.activity,
            traffic = sim_info.traffic,
            operator = sim_info.operator,
            imei = sim_info.imei,
            state_in_lk = sim_info.state_in_lk,
            last_upload = sim_info.last_upload,
            created_on = sim_info.created_on,
            update_on = sim_info.update_on

        )
    else:
        dict_sim_info = SimInfo(sims_id = 0)       

    return dict_sim_info


def check_number_tel(in_number_tel: str) -> bool:

    template_number_tel = r'^(7)([0-9]{10})$'

    check_number_tel = False

    if re.fullmatch(template_number_tel, str(in_number_tel)):
        check_number_tel = True

    return check_number_tel


def check_iccid(in_iccid: str) -> bool:

    template_iccid_megafon = r'^(8970)([0-9]{13})$'
    template_iccid_mts = r'^(8970)([0-9]{16})$'
    template_iccid_beeline = r'^(8970)([0-9]{15})$'

    check_iccid = False

    if str(in_iccid[4:7]) == '101':
        if re.fullmatch(template_iccid_mts, str(in_iccid)):
            check_iccid = True
    
    if str(in_iccid[4:7]) == '102':
        if re.fullmatch(template_iccid_megafon, str(in_iccid)):
            check_iccid = True

    if str(in_iccid[4:7]) == '199':
        if re.fullmatch(template_iccid_beeline, str(in_iccid)):
            check_iccid = True    

    return check_iccid
