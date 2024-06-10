from database.connection import get_db_connection
from models.article import Article

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'<Author {self.name}>'

    @property
    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE author_id = ?', (self.id,))
        articles_data = cursor.fetchall()
        conn.close()
        articles = [Article(article['id'], article['title'], article['content'], article['author_id'], article['magazine_id'])
                    for article in articles_data]
        return articles