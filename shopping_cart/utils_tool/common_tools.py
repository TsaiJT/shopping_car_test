# built-in
import time, sys


##############
# FUNCTION
##############
def log_msg(msg):
    pass


def return_message(is_ok, msg):

    return {
        "ok": is_ok,
        "msg": msg,
        "timestamp": int(time.time())
    }