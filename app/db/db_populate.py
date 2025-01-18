import csv
from db.db_models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from db.db_url import DATABASE_URL

def ParseDate(date_str):
    """Parses a date string with multiple supported formats."""
    formats = [
        "%Y-%m-%d",  # 2023-10-27
        "%Y",       # 2023
        "%Y-%m",    # 2005-02 (Added support)
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            pass  # Try the next format
    return None  # If no format matches


def AddRow(row, session):
                    # Authors are stored as a string in csv, so parsing it to get list 
                    # and using book_author_association table to normalize many-to-many relationship 
                    authors_str = row['authors'].strip("[]")
                    authors = [author.strip().strip("'").strip('"') for author in authors_str.split(",")]
                    for author_name in authors:
                        # Check if author exists or create a new one
                        author = session.query(AuthorBase).filter_by(name=author_name).first()
                        if not author:
                            author = AuthorBase(name=author_name)
                            session.add(author)
                            session.flush()  # Flush to get the author_id
                        #authors.append(author)
                    
                    
                    # Handle publishers
                    publisher_name = row['publisher'].strip()
                    publisher = session.query(PublisherBase).filter_by(name=publisher_name).first()
                    if not publisher:
                        publisher = PublisherBase(name=publisher_name)
                        session.add(publisher)
                        session.flush()  # Flush to get the publisher_id

                    category_name = row['categories'].strip()
                    category = session.query(BookCategoryBase).filter_by(name=category_name).first()
                    if not category:
                        category = BookCategoryBase(name=category_name)
                        session.add(category)
                        session.flush()

                    book = session.query(BookBase).filter_by(id=row['Id']).first()
                    if not book:
                    # Insert the book
                        book = BookBase(
                            id=row['Id'],
                            title=row['Title'].strip(),
                            description=row['description'].strip(),
                            author_id=author.author_id,
                            publisher_id=publisher.publisher_id,
                            published_date = ParseDate(row['publishedDate']) if row['publishedDate'] else None,
                            category_id=category.id,
                            ratings_count=float(row['ratingsCount']) if row['ratingsCount'] else None,
                            cover = row['image'] if row['image'] else None
                        )
                        session.add(book)
                        session.flush()  # Flush to get the book_id
                    
                    # Insert the review
                    review = AmazonReviewBase(
                        book_id=book.id,
                        user_id=row['User_id'],
                        review_helpfulness=row['review/helpfulness'],
                        review_score=float(row['review/score']) if row['review/score'] else None,
                        review_time=datetime.fromtimestamp(int(row['review/time'])) if row['review/time'] else None,
                        review_summary=row['review/summary'].strip(),
                        review_text=row['review/text'].strip(),
                    )
                    session.add(review)

def AddBatch(rows):
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        for row in rows:
            AddRow(row, session) 
        session.commit()  
    except Exception as e:
        print(f"Error processing batch: {e}")
        session.rollback()  
    finally:
        session.close()  

def Populate():
    books_csv = "/app/db/data/merged_df_cropped.csv"
    #books_csv = "/app/db/data/data_short.csv"
    with open(books_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        batch_size = 5000
        batches = [rows[i:i + batch_size] for i in range(0, len(rows), batch_size)]
        for batch in batches:
             AddBatch(batch)