from __init__ import CURSOR, CONN
from author import Author
from magazine import Magazine

class Article:

    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self._title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f'<Article {self._title}>'

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self,value):
        if not isinstance(value,str) or not (5 <= len(value) <= 50):
            raise valueError("title must be a string between 5 to 50 characters")
        self._title = value  

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Article instances """
        sql = """
            CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            FOREIGN KEY(author_id) REFERENCES authors(id),
            FOREIGN KEY(magazine_id) REFERENCES magazines(id)
            );
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def execute_query(cls,query):
        CURSOR.execute(query)
        result = CURSOR.fetchall()  

    @classmethod
    def get_author_by_article_id(cls, article_id):
        query = f"""
        SELECT authors.name FROM authors
        INNER JOIN articles ON authors.id = articles.author_id
        WHERE articles.id = {article_id};
        """
        return cls.execute_query(query)

    @classmethod
    def get_magazine_by_article_id(cls, article_id):
        query = f"""
        SELECT magazines.name FROM magazines
        INNER JOIN articles ON magazines.id = articles.magazine_id
        WHERE articles.id = {article_id};
        """
        return cls.execute_query(query)  

Article.create_table()

#example
# get author name based on article
author_name = Article.get_author_by_article_id(1)
print(f"Author of article 1: {author_name}") 

magazine_name = Article.get_magazine_by_article_id(2)
print(f"Magazine of article 2: {magazine_name}")

