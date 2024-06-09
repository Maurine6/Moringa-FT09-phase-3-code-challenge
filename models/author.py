
from __init__ import CURSOR, CONN

from magazine import Magazine

class Author:
    def __init__(self, id, name):
        self._id = id
        self._name = name

    def __repr__(self):
        return f'<Author {self._name}>'

    @property
    def id(self):
        return self._id 

    @id.setter
    def id(self, value):
        if not isinstance(value):
            raise valueError("name must be an integer")
        self._id = value 

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value) or len(value) == 0:
            raise valueError("name must be string")
        self._name = value 

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Author instances """
        sql = """
            CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
            );
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        """ Insert a new row with the name and id values of the current author instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO authors(name)
            VALUES (?,?)
        """

        CURSOR.execute(sql,(self.name))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
    
    @classmethod
    def create(cls, id,name):
        """ Initialize a new author instance and save the object to the database """
        author = cls(id,name)
        author.save()
        return author

    def update(self):
        """Update the table row corresponding to the current author instance."""
        sql = """
            UPDATE authors
            SET name = ?, 
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name))
        CONN.commit()
    

    @classmethod
    def execute_query(cls, query):
        CURSOR.execute(query)
        result = CURSOR.fetchall()
        return result

    @classmethod
    def articles(cls, author_id):
        query = f"""
        SELECT articles.* FROM articles
        INNER JOIN authors ON articles.author_id = authors.id
        WHERE authors.id = {author_id};
        """
        return cls.execute_query(query)

    @classmethod
    def magazines(cls, author_id):
        query = f"""
        SELECT DISTINCT magazines.* FROM magazines
        INNER JOIN articles ON magazines.id = articles.magazine_id
        INNER JOIN authors ON articles.author_id = authors.id
        WHERE authors.id = {author_id};
        """
        return cls.execute_query(query)    

Author.create_table()

#examples
#create a new author
new_author = Author.create(1, "John Doe")
print(f"Created author: {new_author}")
# Get all magazines of an author with ID 2
magazines = Author.magazines(2)
for magazine in magazines:
    print(magazine)    


    