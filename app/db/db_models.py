from sqlalchemy import Column, Integer, String, Text, Date, Numeric, ForeignKey, TIMESTAMP, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class BookBase(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(Text)
    author_id = Column(Integer, ForeignKey('authors.author_id'))
    publisher_id = Column(Integer, ForeignKey('publishers.publisher_id'))
    published_date = Column(Date)
    category = Column(Text)
    cover = Column(Text)
    ratings_count = Column(Numeric)

    author = relationship("AuthorBase", back_populates="books")
    publisher = relationship("PublisherBase", back_populates="books")
    reviews = relationship("AmazonReviewBase", back_populates="book")

class AuthorBase(Base):
    __tablename__ = 'authors'

    author_id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)

    books = relationship("BookBase", back_populates="author")

# Table for author/book relashionships normalization
book_author_association = Table('book_author', Base.metadata, 
                                Column('book_id', Integer, ForeignKey('books.id'), primary_key=True), 
                                Column('author_id', Integer, ForeignKey('authors.author_id'), primary_key=True)
)

class PublisherBase(Base):
    __tablename__ = 'publishers'

    publisher_id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)

    books = relationship("BookBase", back_populates="publisher")

class AmazonReviewBase(Base):
    __tablename__ = 'amazon_reviews'

    review_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    user_id = Column(Integer)
    review_helpfulness = Column(String(10))
    review_score = Column(Numeric)
    review_time = Column(TIMESTAMP)
    review_summary = Column(Text)
    review_text = Column(Text)

    book = relationship("BookBase", back_populates="reviews")

class UserBase(Base):
    __tablename__ = 'users'

    user_ID = Column(Integer, primary_key=True)
    email = Column(String(254), nullable=False, unique=True)
    username = Column(String(255), nullable=False)
    birthday = Column(Date, nullable=False)
    hashed_password = Column(String(300), nullable=False)


