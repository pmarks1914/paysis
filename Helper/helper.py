from datetime import datetime
import random
import uuid

def generate_random_id():
    random_id = uuid.uuid4().hex[:11].upper()
    return f"TRA{random_id}"

# get otp code 
def generate_random_code():
    code_gene = str(random.randint(100000, 999999))
    return code_gene

def generate_transaction_referance():
    date_current = datetime.utcnow()
    code_short = str(random.randint(1000, 9999))
    date_current = date_current.timestamp()
    return f"TRA{str(date_current).split('.')[0]}{str(code_short)}"
# print(generate_transaction_referance())

 