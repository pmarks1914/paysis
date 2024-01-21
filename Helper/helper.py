import random
import uuid

def generate_random_id():
    # random_id = uuid.uuid4().hex[:11].upper()
    random_id = uuid.uuid4().hex[:11].upper()
    return f"TRA{random_id}"

# get otp code
def generate_random_code():
    code_gene = str(random.randint(100000, 999999))
    return code_gene
# print(generate_random_code())
