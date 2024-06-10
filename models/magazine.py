from database.connection import get_db_connection
from models.author import Author

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f'<Magazine {self.name}>'

    @staticmethod
    def delete_magazine(magazine_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM articles WHERE magazine_id = ?', (magazine_id,))
        cursor.execute('DELETE FROM magazines WHERE id = ?', (magazine_id,))
        conn.commit()
        conn.close()

    @property
    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE magazine_id = ?', (self.id,))
        articles_data = cursor.fetchall()
        conn.close()
        articles = [Article(article['id'], article['title'], article['content'], article['author_id'], article['magazine_id'])
                    for article in articles_data]
        return articles

    @property
    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self.id,))
        authors_data = cursor.fetchall()
        conn.close()
        authors = [Author(author['id'], author['name']) for author in authors_data]
        return authors