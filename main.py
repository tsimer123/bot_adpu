from sql.scheme import create_db
from bot.start_bot import run_bot
from services.user import get_user_info, create_user, get_user_id
from services.log import create_log
from services.equipment import get_equipment_info

dict_user = {
        "tg_id": '444238478',
        "tg_name": '@etsimerman',
        "full_name": 'Евгений Цимерман'        
    }

dict_user_info = {
            "users_id": 1,
            "user_id_tg": 444238478,
            "tg_name": '@etsimerman',
            "full_name": 'Евгений Цимерман'
        } 

def first_start():
    create_db()

def start_bot():
    run_bot()

def add_user():    
    create_user(dict_user)
    
def select_user():    
    get_user_info('444238478')

def add_log():
     type = 'input'
     message = '/coord 55.663918, 37.998710'
     create_log(dict_user_info, type, message)

def get_equipment():
    get_equipment_info()

if __name__ == "__main__":
    start_bot()
