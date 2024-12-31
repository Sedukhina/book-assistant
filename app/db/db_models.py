from sqlalchemy import Column, Integer, String, Text, Date, Numeric, ForeignKey, TIMESTAMP, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class BookBase(Base):
    __tablename__ = 'books'

    id = Column(Text, primary_key=True)
    title = Column(Text)
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

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "author": self.author.name if self.author else None,
            "publisher_id": self.publisher_id,
            "published_date": self.published_date.isoformat() if self.published_date else None,
            "category": self.category,
            "cover": self.cover,
            "ratings_count": float(self.ratings_count) if self.ratings_count else None,
        }
    def to_preview(self):
        return {
            "id": self.id,
            "title": self.title,
            "author_id":self.author.author_id if self.author else None,
            "author": self.author.name if self.author else None,
            "publishDate": int(self.published_date.year) if self.published_date else None,
            "categories": self.category.strip().split('&') if self.category else [],
            "cover": self.cover,
        }

class AuthorBase(Base):
    __tablename__ = 'authors'

    author_id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)

    books = relationship("BookBase", back_populates="author")

# Table for author/book relashionships normalization
book_author_association = Table('book_author', Base.metadata, 
                                Column('book_id', Text, ForeignKey('books.id'), primary_key=True), 
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
    book_id = Column(Text, ForeignKey('books.id'))
    user_id = Column(Text)
    review_helpfulness = Column(String(20))
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


