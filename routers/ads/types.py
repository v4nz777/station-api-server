from typing import List,Any,Optional
from strawberry.file_uploads import Upload
import strawberry
import datetime

@strawberry.type
class VersionDetail:
    
    pricing:str
    price:float
    spot_duration_seconds:int
    spots_per_day:int
    aob_per_day:int|None = None
    tc_per_day:int|None = None
    ss_per_day:int|None = None
    spots_schedule:List[str]
    aob_schedule:List[str]|None = None
    tc_schedule:List[str]|None = None
    ss_schedule:List[str]|None = None
    
    starts:datetime.datetime|None = None
    ends:datetime.datetime|None = None
    account_executive:str|None = None
    version:int
    ex_deal:bool
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
class AdsDetailsInput:
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


@strawberry.input
class AdCreationInput:
    title:str
    contract:str
    bo:str|None = None
    type:str = 'local'
    details:AdsDetailsInput

    def jsonify(self)->dict:
        return {
            'title':self.title,
            'contract':self.contract,           
            'bo':self.bo,
            'type':self.type,
            'details':{
                'ex_deal':self.details.ex_deal,
                'pricing':self.details.pricing,
                'price':self.details.price,
                'starts':datetime.datetime.fromisoformat(self.details.starts) if self.details.starts else None,
                'ends':datetime.datetime.fromisoformat(self.details.ends) if self.details.ends else None,
                'spot_duration_seconds':self.details.spot_duration_seconds,
                'spots_per_day':self.details.spots_per_day,
                'aob_per_day':self.details.aob_per_day,
                'tc_per_day':self.details.tc_per_day,
                'ss_per_day':self.details.ss_per_day,
                'spots_schedule':self.details.spots_schedule,
                'aob_schedule':self.details.aob_schedule,
                'tc_schedule':self.details.tc_schedule,
                'ss_schedule':self.details.ss_schedule,
                'account_executive':self.details.account_executive,
                'materials': self.details.materials,
                'display': self.details.display,

            }
        }



