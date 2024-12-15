import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine
from database.connection import get_db_connection

class TestModels(unittest.TestCase):
    def test_author_creation(self):
        author = Author(1, "John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        with get_db_connection() as conn:
        # Reset the database
            conn.execute("DELETE FROM authors")
            conn.execute("DELETE FROM magazines")
            conn.execute("DELETE FROM articles")
        
            # Insert data into authors and magazines with category
            conn.execute("INSERT INTO authors (id, name) VALUES (1, 'John Doe')")
            conn.execute("INSERT INTO magazines (id, name, category) VALUES (1, 'Tech Weekly', 'Technology')")
        
        # Create and test the article
        article = Article(1, "Test Title", "Test Content", 1, 1)
        self.assertEqual(article.title, "Test Title")
        self.assertEqual(article.content, "Test Content")
        self.assertEqual(article.author_id, 1)
        self.assertEqual(article.magazine_id, 1)


    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly")
        self.assertEqual(magazine.name, "Tech Weekly")

if __name__ == "__main__":
    unittest.main()
