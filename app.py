from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database and create tables
    create_tables()

    while True:
        print("Choose an option:")
        print("1. Add an author, magazine, and article")
        print("2. Delete a magazine")
        print("3. View all data")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            # Collect user input
            author_name = input("Enter author's name: ")
            magazine_name = input("Enter magazine name: ")
            magazine_category = input("Enter magazine category: ")
            article_title = input("Enter article title: ")
            article_content = input("Enter article content: ")

            # Connect to the database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Create an author
            cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
            author_id = cursor.lastrowid  # Use this to fetch the id of the newly created author

            # Create a magazine
            cursor.execute('INSERT INTO magazines (name, category) VALUES (?,?)', (magazine_name, magazine_category))
            magazine_id = cursor.lastrowid  # Use this to fetch the id of the newly created magazine

            # Create an article
            cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                           (article_title, article_content, author_id, magazine_id))

            conn.commit()
            conn.close()

        elif choice == "2":
            # Delete a magazine
            magazine_id = int(input("Enter the ID of the magazine to delete: "))
            Magazine.delete_magazine(magazine_id)

        elif choice == "3":
            # Connect to the database
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM magazines')
            magazines = cursor.fetchall()

            cursor.execute('SELECT * FROM authors')
            authors = cursor.fetchall()

            cursor.execute('SELECT * FROM articles')
            articles = cursor.fetchall()

            conn.close()

            # Display results
            print("\nMagazines:")
            for magazine in magazines:
                print(Magazine(magazine["id"], magazine["name"], magazine["category"]))

            print("\nAuthors:")
            for author in authors:
                print(Author(author["id"], author["name"]))

            print("\nArticles:")
            for article in articles:
                print(Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]))

        elif choice == "4":
            break

if __name__ == "__main__":
    main()