import strawberry
import datetime


@strawberry.type
class AdsPackage:
    _id:str
    title:str
    created:datetime.datetime
    author:str

    price:int| None = None
    spot_duration_seconds:int| None = None
    spots_per_day:int| None = None
    aob_per_day:int| None = None
    tc_per_day:int| None = None
    ss_per_day:int| None = None
    broadcast_duration_count:int| None = None
    broadcast_duration_unit:str| None = None


@strawberry.input
class AdsPackageCreationInput:
    author:str
    title:str
    price:int | None = None
    spot_duration_seconds:int | None = None
    spots_per_day:int | None = None
    aob_per_day:int | None = None
    tc_per_day:int | None = None
    ss_per_day:int | None = None
    broadcast_duration_count:int | None = None
    broadcast_duration_unit:str | None = None

    def jsonify(self):
        return {
            'author':self.author,
            'title': self.title,
            'created':datetime.datetime.now(),
            'price':self.price,
            'spot_duration_seconds': self.spot_duration_seconds,
            'spots_per_day': self.spots_per_day,
            'aob_per_day': self.aob_per_day,
            'tc_per_day': self.tc_per_day,
            'ss_per_day': self.ss_per_day,
            'broadcast_duration_count': self.broadcast_duration_count,
            'broadcast_duration_unit': self.broadcast_duration_unit,
        }
        