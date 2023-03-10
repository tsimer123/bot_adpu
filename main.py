import sys
from sql.scheme import create_db
from bot.start_bot import run_bot
from services.user import get_user_info, create_user, get_user_id
from services.log import create_log
from services.equipment import get_equipment_info


def first_start():
    create_db()


def start_bot():
    run_bot()


if __name__ == "__main__":
    input_flags = sys.argv

    try:
        if input_flags[1] == '-help':
            print(
                '-help - help\n-start_b - start bot\n-crt_db  - create db'
            )
        
        if input_flags[1] == '-start_b':    
            start_bot()

        if input_flags[1] == '-crt_db':    
            first_start()
    except:
        print(
                '-help - help\n-start_b - start bot\n-crt_db  - create db'
            )
