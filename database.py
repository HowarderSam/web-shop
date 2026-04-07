from sqlalchemy import create_engine, String, Float, Integer, ForeignKey, Boolean,func
from sqlalchemy.orm import Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy.orm import DeclarativeBase


engine = create_engine("sqlite:///shop.db", echo=True)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    def create_db(self):
        Base.metadata.create_all(engine)

    def drop_db(self):
        Base.metadata.drop_all(engine)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String(200)) 

    phone: Mapped[str] = mapped_column(String(20),nullable=True)
    address: Mapped[str] = mapped_column(String(30),nullable=True)

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(50))
    storage: Mapped[int] = mapped_column(Integer, nullable=False)
    color: Mapped[str] = mapped_column(String(30), nullable=False)

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="product")

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'),nullable = False)
    product: Mapped["Product"] = relationship("Product", back_populates="orders")
    user: Mapped['User'] = relationship("User", back_populates='orders')


def init_db():
    base = Base()
    base.create_db() 

    with Session() as session:
        products = [
            Product(name='Iphone 17 Pro', 
                    description='Innovative design for ultimate perfomance and battery life',
                      price='1299',
                      image='https://www.mp.cz/media/photos/2025/09/09/204902-1.avif',
                      category='phone',
                      storage='512',
                      color='Orange'),
            
            Product(name='Iphone 15 Pro Max',
                    description='Old but gold, optimal perfomance for its price',
                    price='599',
                    image='https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-15-pro-max-1.jpg',
                    category='phone',
                    storage='256',
                    color='Titanium'),
            
            Product(name='Ipad Pro',
                    description='The ultimate iPad experience with the most advanced technology.',
                    price='1199',
                    image='https://images.mironet.cz/foto/w3/83702468/1.jpg.add.webp',
                    category='ipad',
                    storage='512',
                    color='Black'),

            Product(name='Ipad Air',description='Serious performance in a thin and light design.',
                    price='599',
                    image='https://doc.smarty.cz/pic/EN84000J01-600-600.webp',
                    category='ipad',
                    storage='128',
                    color='Blue')
        ]

        session.add_all(products)
        session.commit()



# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
# RUN ONLY AFTER YOU ADD NEW PRODUCTS INTO THE CODE ABOVE !
# init_db() RUN ONCE! 



def get_products():
    with Session() as session:
            products = session.query(Product).all()
    return products


def get_product(id):
    with Session() as session:
            product = session.query(Product).filter_by(id=id).first()
    return product


def add_user(username,password):
    with Session() as session:
        new_user = User(
            username=username,
            password=password,
        )
        session.add(new_user)
        session.commit()


def add_order(product_id, user_id):
    with Session() as session:
        new_order = Order(
            product_id = product_id,
            user_id = user_id
        )
        session.add(new_order)
        session.commit()


def get_users():
    with Session() as session:
            users = session.query(User).all()
    return len(users)



def get_user(username):
    with Session() as session:
            user = session.query(User).filter_by(username=username).first()
    return user

def get_user_by_id(user_id:int):
    with Session() as session:
        user = session.query(User).filter_by(id=user_id).first()
    return user

def get_orders(user_id):
    with Session() as session:
            orders = session.query(Order).filter_by(user_id=user_id).all()
            products = []
            for order in orders:
                 if order.product:
                      products.append({'id':order.product.id,'name':order.product.name, 
                                       'price':order.product.price ,'desc':order.product.description,
                                       'img':order.product.image,'category':order.product.category,
                                       'storage':order.product.storage,'color':order.product.color})
                    
    return orders, products


def upd_password(user_id, new_hashed_password):
    with Session() as session:
        user = session.query(User).filter_by(id=user_id).first()
        user.password = new_hashed_password
        session.add(user)
        session.commit()


def get_products_by_category(category=None):
    with Session() as session:
        if category:
            products = session.query(Product).filter(
                Product.category.ilike(category)
            ).all()
        else:
            products = session.query(Product).all()
    return products