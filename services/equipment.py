from sqlalchemy.orm import Session, sessionmaker

from sql.engine import engine
from sql.scheme import Equipments

Session = sessionmaker(engine)

session = Session()

def get_equipment_info():

    list_equipment = []
    
    try:
        equipment_info = session.query(
            Equipments.equipments_id,
            Equipments.yoda_networkequipments_id,
            Equipments.number_equipment,
            Equipments.type_equipment,
            Equipments.model_equipment,
            Equipments.latitude,
            Equipments.longitude,
            Equipments.number_sim_1,
            Equipments.iccid_1,
            Equipments.operator_1,
            Equipments.number_sim_2,
            Equipments.iccid_2,
            Equipments.operator_2,
            Equipments.number_sim_3,
            Equipments.iccid_3,
            Equipments.operator_3).all()   
        
        if len(equipment_info) != 0:
            for line_equipment_info in equipment_info:
                dict_equipment_info = {
                    "equipments_id": line_equipment_info.equipments_id,
                    "networkequipments_id": line_equipment_info.yoda_networkequipments_id,
                    "number_equipment": line_equipment_info.number_equipment,
                    "type_equipment": line_equipment_info.type_equipment,
                    "model_equipment": line_equipment_info.model_equipment,
                    "latitude": line_equipment_info.latitude,
                    "longitude": line_equipment_info.longitude,
                    "number_sim_1": line_equipment_info.number_sim_1,
                    "iccid_1": line_equipment_info.iccid_1,
                    "operator_1": line_equipment_info.operator_1,
                    "number_sim_2": line_equipment_info.number_sim_2,
                    "iccid_2": line_equipment_info.iccid_2,
                    "operator_2": line_equipment_info.operator_2,
                    "number_sim_3": line_equipment_info.number_sim_3,
                    "iccid_3": line_equipment_info.iccid_3,
                    "operator_3": line_equipment_info.operator_3
                                
                } 
                list_equipment.append(dict_equipment_info)      
        else:
            dict_equipment_info = {
                    "equipments_id": 0,
                    "networkequipments_id": '',
                    "number_equipment": '',
                    "type_equipment": '',
                    "model_equipment": '',
                    "latitude": '',
                    "longitude": '',
                    "number_sim_1": '',
                    "iccid_1": '',
                    "operator_1": '',
                    "number_sim_2": '',
                    "iccid_2": '',
                    "operator_2": '',
                    "number_sim_3": '',
                    "iccid_3": '',
                    "operator_3": ''
                } 
            list_equipment.append(dict_equipment_info)   
    except Exception as ex:        
        raise ex
    finally:
        session.close()   
    
    return list_equipment