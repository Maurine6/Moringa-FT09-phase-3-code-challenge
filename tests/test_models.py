import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine

class TestModels(unittest.TestCase):
    def test_author_creation(self):
        author = Author(1, "John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        article = Article(1, "Test Title", "Test Content", 1, 1)
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly", "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")

    def test_author_articles(self):
        author = Author(1, "John Doe")
        articles = author.articles
        self.assertIsInstance(articles, list)
        self.assertTrue(all(isinstance(article, Article) for article in articles))

    def test_magazine_contributing_authors(self):
        magazine = Magazine(1, "Tech Weekly", "Technology")
        authors = magazine.contributing_authors
        self.assertIsInstance(authors, list)
        self.assertTrue(all(isinstance(author, Author) for author in authors))

if __name__ == "__main__":
    unittest.main()