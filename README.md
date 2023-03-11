# Test Test Task: Procurers ate my breakfast

This is a test test task representing a simple supplier-whoesaler-retailer chain.

The model is hierarchical:
* a Factory only provides stuff.
* a Wholesaler can procure stuff from Factory and sell it to Retailer. To sell, it must first procure.
* a Retailer can only procure stuff, both from Factory and Wholesaler.

Any Procurer can have one Supplier.
Due amount can only be changed from the admin panel, not via API.
Only active stuff members can access API.
Money is measured in kopecks/cents, as required by all payment APIs.
Only a business unit with no amount due can be deleted.

Docs on API are in Swagger: /api/schema/swagger-ui/
