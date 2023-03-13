import re
import math

from services.equipment import get_equipment_info

def serch_uspd(dict_coords):    

    result = {
        "networkequipments_id": '',
        "dist": 0.123,
        "status": '',
        "descriprion": ''

    }  

    valid_coord_sourse = check_coords(dict_coords)

    if valid_coord_sourse:
        equipment = get_equipment_info()

        if equipment[0]['equipments_id'] != 0:

            for line_equipment in equipment:           
                
                temp_result = calc_one_eqp(line_equipment, dict_coords)

                if temp_result['networkequipments_id'] != 'not valid coord eqp from db':

                    if result['dist'] == 0.123:
                        result['networkequipments_id'] = temp_result['networkequipments_id']
                        result['dist'] = temp_result['dist']

                    try:
                        if temp_result['dist'] < result['dist']:
                            result['networkequipments_id'] = temp_result['networkequipments_id']
                            result['dist'] = temp_result['dist']                            
                    except:
                        print(type(temp_result['dist']))
                        print(temp_result['dist'])

                        print(type(result['dist']))
                        print(result['dist'])
            if result['dist'] > 500.00:
                result['status'] = False
                result['descriprion'] = "Dist more than 500 m, no ZB network connection"

        else:
            result['status'] = False
            result['descriprion'] = "Error DB, no equipment in table"

    else:
        result['status'] = False
        result['descriprion'] = "No valid source coordinates"

    if result['dist'] == 0.123 and result['status'] == '':
        result['status'] = False
        result['descriprion'] = "Error DB, not valid uquipment"

    if result['status'] == '':
        result['dist'] = normalized_dist(result['dist'])
        result = final_format(result, equipment)       

    return result
    

def check_coords(dict_coords):

    template_lat = r'^(\+|-)?(?:90(?:(?:\.0{4,6})?)|(?:[4-6][0-9])(?:(?:\.[0-9]{2,30})+))$'
    template_long = r'^(\+|-)?(?:180(?:(?:\.0{4,6})?)|(?:[3-5][0-9])(?:(?:\.[0-9]{2,30})+))$'
    # template_long = r'^(\+|-)?(?:180(?:(?:\.0{4,6})?)|(?:[3-5][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{2,30})+))$'
    
    check_lat = False
    check_long = False

    result_check_coord = False
    
    if re.fullmatch(template_lat, str(dict_coords['latitude'])):
        check_lat = True
        
    if re.fullmatch(template_long, str(dict_coords['longitude'])):
        check_long = True
    
    if check_lat and check_long:
        result_check_coord = True

    return result_check_coord


def dist_calc_coordinates(dict_coords):

    latitude_req = str(dict_coords['latitude_req'])
    longitude_req = str(dict_coords['longitude_req'])
    latitude_eqp = str(dict_coords['latitude_eqp'])
    longitude_eqp = str(dict_coords['longitude_eqp'])

    # pi - число pi, rad - радиус сферы (Земли)
    rad = 6372795
    
    # координаты двух точек
    llat1 = float(latitude_req)
    llong1 = float(longitude_req)    
    llat2 = float(latitude_eqp)
    llong2 = float(longitude_eqp)

    # в радианах
    lat1 = llat1 * math.pi / 180.
    lat2 = llat2 * math.pi / 180.
    long1 = llong1 * math.pi / 180.
    long2 = llong2 * math.pi / 180.

    # косинусы и синусы широт и разницы долгот
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    # вычисления длины большого круга
    y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = math.atan2(y, x)
    dist = ad * rad

    return dist


def normalized_dist(dist):

    div = dist / 1000
    result = 0.0

    if div >= 1:
        result = str(round(div, 2)) + " км"
    
    if div <= 1:
        result = str(round(dist, 0)) + " м"

    return result


def format_dict_coord_for_check(latitude, longitude):
    
    dict_coords = {
                "latitude": latitude,
                "longitude": longitude
            }
    
    return dict_coords


def format_dict_coord_for_calc(dict_req, dict_eqp):

    dict_coords = {
                "latitude_req": dict_req['latitude'],
                "longitude_req": dict_req['longitude'],
                "latitude_eqp": dict_eqp['latitude'],
                "longitude_eqp": dict_eqp['longitude']
            }
    
    return dict_coords


def calc_one_eqp(line_equipment, dict_coords):

    result = {
        "networkequipments_id": '',
        "dist": ''
    }

    dict_coords_eqp = format_dict_coord_for_check(
                line_equipment['latitude'],
                line_equipment['longitude'])

    valid_coord_equipmnt = check_coords(dict_coords_eqp)

    if valid_coord_equipmnt:

        if valid_coord_equipmnt:

            dict_coord_calc = format_dict_coord_for_calc(
                dict_coords,
                dict_coords_eqp
            )

            dist = dist_calc_coordinates(dict_coord_calc)

            result = {
                "networkequipments_id": line_equipment['networkequipments_id'],
                "dist": dist
            }
    else:
        result["networkequipments_id"] = 'not valid coord eqp from db'

    return result


def final_format(result, equipment):

    dict_final = {
        "status": True,
        "equipments_id": '',
        "networkequipments_id": '',
        "number_equipment": '',
        "type_equipment": '',
        "model_equipment": '',
        "latitude": '',
        "longitude": '',
        "dist": '',
        "descriprion": '',
        "number_sim": '',
        "iccid": '',
        "operator": '',
        "type_mode_modem": ''
    }

    dict_final['networkequipments_id'] = result['networkequipments_id']
    dict_final['dist'] = result['dist']

    count = 0

    while len(equipment) > count:
        if dict_final['networkequipments_id'] == equipment[count]['networkequipments_id']:
            dict_final['equipments_id'] = equipment[count]['equipments_id']
            dict_final['number_equipment'] = equipment[count]['number_equipment']
            dict_final['type_equipment'] = equipment[count]['type_equipment']
            dict_final['model_equipment'] = equipment[count]['model_equipment']
            dict_final['latitude'] = equipment[count]['latitude']
            dict_final['longitude'] = equipment[count]['longitude']
            dict_final['number_sim'] = equipment[count]['number_sim_1']
            dict_final['iccid'] = equipment[count]['iccid_1']
            dict_final['operator'] = equipment[count]['operator_1']
            dict_final['type_mode_modem'] = type_mode_modem(equipment[count]['type_equipment'])
            break
        else:
            count += 1
    
    return dict_final


def type_mode_modem(type_equipment):

    if type_equipment == 'Шлюз':
        return 'Клиент'    
    else:
        return 'Сервер'
    