from __init__ import CURSOR, CONN

class Magazine:
    def __init__(self, id, name, category):
        self._id = id
        self._name = name
        self._category = category

    def __repr__(self):
        return f'<Magazine {self._name}>'

    @property
    def magazines_id(self):
        return self._id

    @magazines_id.setter
    def magazine_id(self, value):
        if not isinstance(value, int):
            raise valueError("id must be an integer")
        self._id = value

    @property
    def magazine_name(self):
        return self._name

    @magazine_name.setter
    def magazine_name(self, value):
        if not isinstance(value, str) or not (2 <= len(name) <= 16):
            raise valueError("name should string between 2 to 16 characters")
        self._name = value 

    @property
    def magazine_category(self):
        return self._category

    @magazine_category.setter
    def magazine_category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise valueError("category must be string with more than zero characters")
        self._category = value 


    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Magazine instances """
        sql = """
            CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL
            );
        """
        CURSOR.execute(sql)
        CONN.commit() 

    @classmethod
    def execute_query(cls, query):
        CURSOR.execute(query)
        result = CURSOR.fetchall()
        return result

    @classmethod
    def articles(cls, magazine_id):
        query = f"""
        SELECT articles.* FROM articles
        INNER JOIN magazines ON articles.magazine_id = magazines.id
        WHERE magazines.id = {magazine_id};
        """
        return cls.execute_query(query)

    @classmethod
    def contributors(cls, magazine_id):
        query = f"""
        SELECT DISTINCT authors.* FROM authors
        INNER JOIN articles ON authors.id = articles.author_id
        INNER JOIN magazines ON articles.magazine_id = magazines.id
        WHERE magazines.id = {magazine_id};
        """
        return cls.execute_query(query) 

    @classmethod
    def article_titles(cls, magazine_id):
        query = f"""
        SELECT articles.title FROM articles
        INNER JOIN magazines ON articles.magazine_id = magazines.id
        WHERE magazines.id = {magazine_id};
        """
        result = cls.execute_query(query)
        
        # Check if any articles were found
        if not result:
            return None
        
        # Extract titles from the result and return as a list
        titles = [row[0] for row in result]
        return titles 

    @classmethod
    def contributing_authors(cls, magazine_id):
        # Count the number of articles per author for the magazine
        count_query = f"""
        SELECT authors.id, COUNT(*) as article_count FROM authors
        INNER JOIN articles ON authors.id = articles.author_id
        INNER JOIN magazines ON articles.magazine_id = magazines.id
        WHERE magazines.id = {magazine_id}
        GROUP BY authors.id;
        """
        counts = cls.execute_query(count_query)
        
        # Filter authors with more than 2 publications
        threshold = 2
        qualifying_counts = [(count[0], count[1]) for count in counts if count[1] > threshold]

        #  Retrieve the details of qualifying authors
        if not qualifying_counts:
            return None

        author_ids = [qualifying_count[0] for qualifying_count in qualifying_counts]
        detail_query = f"""
        SELECT * FROM authors WHERE id IN ({', '.join(map(str, author_ids))});
        """
        authors_details = cls.execute_query(detail_query)

        # Return the list of qualifying authors
        return authors_details       
       

Magazine.create_table()

#example
# Get all articles of a magazine with ID 1
articles = Magazine.articles(1)
for article in articles:
    print(article)

# Get all authors of a magazine with ID 2
contributors = Magazine.contributors(2)
for contributor in contributors:
    print(contributor)

 # Get all article titles of a magazine with ID 1
titles = Magazine.article_titles(1)
if titles is None:
    print("No articles found.")
else:
    for title in titles:
        print(title) 

# Get all contributing authors of a magazine with ID 1
authors = Magazine.contributing_authors(1)
if authors is None:
    print("No authors found with more than 2 publications.")
else:
    for author in authors:
        print(author)

                      
