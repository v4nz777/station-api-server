from strawberry.file_uploads import Upload
import strawberry
import datetime

@strawberry.type
class Billing:
    _id:str
    author:str
    invoice_num:str
    invoice_date:datetime.datetime
    created:datetime.datetime
    amount:int
    or_num:str|None = None
    or_date:str|None = None
    deposit_proof:Upload|None = None

@strawberry.input
class BillingCreationInput:
    author:str
    invoice_num:str
    invoice_date:str
    amount:int
    
    def jsonify(self):
        return {
            'author':self.author,
            'invoice_num':self.invoice_num,
            'invoice_date':datetime.datetime.fromisoformat(self.invoice_date),
            'amount':self.amount,
            'created': datetime.datetime.now(),
            'or_num':None,
            'or_date':None,
            'deposit_proof':None,
        }


    