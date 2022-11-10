from db_connector import DAO
from user import User
from student import Student
from tutor import Tutor

db=DAO()

def new_user(id,email,password,name,account_type,career_id=0,tutor_c=0):
    tutor_code_exists=False
    print(id,email,password,name,account_type)
    user=User(int(id),email,password,name,int(account_type))
    db.newObject(0,user)
    if account_type==1:
        student=Student(5,career_id,id)
        db.newObject(1,student)
        return True
    elif account_type==2:
        tutor_codes=db.getTableInfo(8)
        for tutor_code in tutor_codes:
            if tutor_code[0]==int(tutor_c):
                tutor_code_exists=True
                break
        if tutor_code_exists:
            tutor=Tutor(id,5)
        else:
            tutor=None
            return False
        db.newObject(2,tutor)
        return True

def login(email,password):
    email_exists=False
    user_can_enter=False
    users=db.getTableInfo(0)
    for user in users:
        if user[1]==email:
            email_exists=True
            actual_password=db.get_password_by_email(email)
            if password==actual_password[0]:
                user_can_enter=True
                #return True
            #else:
                #return False
    return email_exists,user_can_enter

def get_table(num):
    lista=db.getTableInfo(num)
    return lista

def email_exists(email):
    email_db=db.get_email(email)
    if email_db is None:
        return False
    else:
        if email_db[0]==email:
            return True
        else:
            return False

def get_account_type_id_by_id(id):
    acc_type=db.get_account_type_id_by_user_id(id)
    return acc_type[0]

def get_id_by_email(email):
    id=db.get_id_by_email(email)
    return id[0]

def get_name_by_id(id):
    name=db.get_name_by_id(id)
    return name[0]

def get_subject_by_carrer_id(carrer_id):
    lista=db.get_subject_by_carrer_id(carrer_id)
    return lista

def get_users_by_type(type):
    lista=db.get_user_by_account_type(type)

    return lista