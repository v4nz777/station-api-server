from jwt_auth import require_token
from .types import Billing,BillingCreationInput
from . import helpers
from typing import List
import strawberry


@strawberry.type
class Query:
    @strawberry.field
    @require_token
    def all_billings(self, info)->List[Billing]:
        all = helpers.get_all_billings_from_database()
        return [Billing(**billing) for billing in all]
    
    @strawberry.field
    @require_token
    def billing(self, info, invoice_no) -> Billing:
        billing = helpers.get_billing_from_database(invoice_no)
        return Billing(**billing)
