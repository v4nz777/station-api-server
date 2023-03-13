from typing import List,Any,Optional
from strawberry.file_uploads import Upload
import strawberry
import datetime



@strawberry.type
class VersionDetail:
    ex_deal:bool
    pricing:str
    price:float
    starts:datetime.datetime|None = None
    ends:datetime.datetime|None = None
    spot_duration_seconds:int
    spots_per_day:int
    aob_per_day:int|None = None
    tc_per_day:int|None = None
    ss_per_day:int|None = None
    spots_schedule:List[str]
    aob_schedule:List[str]|None = None
    tc_schedule:List[str]|None = None
    ss_schedule:List[str]|None = None
    account_executive:str|None = None
    version:int
    stashed:datetime.datetime|None = None
    materials: List[str]|None = None
    hard_copies: List[str]|None = None
    display: str|None
    

@strawberry.type
class Advertisement:
    _id:str
    title:str
    contract:str
    bo:str|None = None
    type:str
    details: VersionDetail
    created:datetime.datetime|None = None
    updated:datetime.datetime|None = None
    prev_versions:List[VersionDetail]|None = None



@strawberry.input
class AdCreationInput:
    title:str
    contract:str
    bo:str|None = None
    type:str = 'local'
    ex_deal:bool = False
    pricing:str = 'fixed'
    price:float|None = None
    starts:str|None = None
    ends:str|None = None
    spot_duration_seconds:int|None = None
    spots_per_day:int|None = None
    aob_per_day:int|None = None
    tc_per_day:int|None = None
    ss_per_day:int|None = None
    spots_schedule:List[str]|None = None
    aob_schedule:List[str]|None = None
    tc_schedule:List[str]|None = None
    ss_schedule:List[str]|None = None
    account_executive:str|None = None
    materials: List[Upload]|None = None
    display:List[Upload]|None = None


    def jsonify(self)->dict:
        return {
            'title':self.title,
            'contract':self.contract,           
            'bo':self.bo,
            'type':self.type,
            'details':{
                'ex_deal':self.ex_deal,
                'pricing':self.pricing,
                'price':self.price,
                'starts':datetime.datetime.fromisoformat(self.starts) if self.starts else None,
                'ends':datetime.datetime.fromisoformat(self.ends) if self.ends else None,
                'spot_duration_seconds':self.spot_duration_seconds,
                'spots_per_day':self.spots_per_day,
                'aob_per_day':self.aob_per_day,
                'tc_per_day':self.tc_per_day,
                'ss_per_day':self.ss_per_day,
                'spots_schedule':self.spots_schedule,
                'aob_schedule':self.aob_schedule,
                'tc_schedule':self.tc_schedule,
                'ss_schedule':self.ss_schedule,
                'account_executive':self.account_executive,
                'materials': self.materials,
                'display': self.display,

            }
        }



