from db import MainDB
from typing import List
from .types import Billing,BillingCreationInput

def get_all_billings_from_database()->List[dict]:
    db = connect_to_database_collection_billings()
    return db.read_all()

def get_billing_from_database(invoice_num:str)->dict:
    db = connect_to_database_collection_billings()
    billing = db.read({'invoice_num':invoice_num})
    if not billing:
        raise ValueError(f'Invoice {invoice_num} not found!')
    return billing

def add_billing_to_database(data:BillingCreationInput)->dict:
    db = connect_to_database_collection_billings()
    if db.read({'invoice_num':data.invoice_num}):
        raise ValueError(f'Billing {data.invoice_num} already existed in database')
    return db.create(data.jsonify())

def connect_to_database_collection_billings()->MainDB:
    db:MainDB = MainDB() # Instatiates database connection
    db.create_collection('billings') # Will create new collection if it doesnt exist yet
    db.to_collection('billings') # Then connects to the collection
    return db