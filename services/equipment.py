from sqlalchemy.orm import Session, sessionmaker

from sql.engine import engine
from sql.scheme import Equipments

Session = sessionmaker(engine)

session = Session()

def get_equipment_info():

    list_equipment = []

    equipment_info = session.query(
        Equipments.equipments_id,
        Equipments.yoda_networkequipments_id,
        Equipments.number_equipment,
        Equipments.type_equipment,
        Equipments.model_equipment,
        Equipments.latitude,
        Equipments.longitude).all()   
    
    if len(equipment_info) != 0:
        for line_equipment_info in equipment_info:
            dict_equipment_info = {
                "equipments_id": line_equipment_info.equipments_id,
                "networkequipments_id": line_equipment_info.yoda_networkequipments_id,
                "number_equipment": line_equipment_info.number_equipment,
                "type_equipment": line_equipment_info.type_equipment,
                "model_equipment": line_equipment_info.model_equipment,
                "latitude": line_equipment_info.latitude,
                "longitude": line_equipment_info.longitude            
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
                "longitude": ''
            } 
        list_equipment.append(dict_equipment_info)   
    
    return list_equipment