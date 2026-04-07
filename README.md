# web-shop
- Latest web-shop mini-project. 


- To successfully run the code please run init_db() first in database.py - it will generate the database
- If you want to add more products to your website please add them into def init() using same structure as products above.
- Then run Base.metadata.drop_all(engine) and Base.metadata.create_all(engine) to re-create the datavse - it will delete and create the database anew
- Then run init_db() to add the products into your newly created database
