from services.sims import get_sim_number_tel, get_sim_iccid, get_count_sims,\
check_iccid, check_number_tel, SimInfo

def input_data(message_text: list) -> SimInfo:   
    
    if message_text[0] == 'tel':
        if count_sims_in_db() > 0:
            return hanler_number_tel(message_text[1])
        else:
            "Error DB, no sims in table"
    
    if message_text[0] == 'iccid':
        if count_sims_in_db() > 0:
            return handler_iccid(message_text[1])
        else:
            "Error DB, no sims in table"

    return 'Not valid imput command'


def hanler_number_tel(input_data: str) -> SimInfo:

    sim_info = SimInfo()
    
    if check_number_tel(input_data):
       response_db = get_sim_number_tel(input_data)
       if response_db['sims_id'] != 0:
           return response_db
       else:
           response_db['description'] = 'Not sim in DB'
           return response_db
    else:
        sim_info['sims_id'] = 0
        sim_info['description'] = 'Not valid number tel'
   
    return sim_info


def handler_iccid(input_data: str) -> SimInfo:

    sim_info = SimInfo()

    if check_iccid(input_data):        
        response_db = get_sim_iccid(input_data)
        if response_db['sims_id'] != 0:
            return response_db
        else:
            response_db['description'] = 'Not sim in DB'
            return response_db
    else:
        sim_info['sims_id'] = 0
        sim_info['description'] = 'Not valid iccid'

    return sim_info


def count_sims_in_db() -> int:

    result_count = get_count_sims()

    return result_count
            
            