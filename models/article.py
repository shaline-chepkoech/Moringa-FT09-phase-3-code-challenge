from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

class Article:
    def __init__(self, id=None, title=None, content=None, author_id=None, magazine_id=None):
        if title is not None and (not isinstance(title, str) or not (5 <= len(title) <= 50)):
            raise ValueError("Title must be a string between 5 and 50 characters.")
        if content is not None and not isinstance(content, str):
            raise ValueError("Content must be a string.")
        if author_id is not None and not isinstance(author_id, int):
            raise ValueError("Author ID must be an integer.")
        if magazine_id is not None and not isinstance(magazine_id, int):
            raise ValueError("Magazine ID must be an integer.")

        self._id = id
        self._title = title
        self._author_id = author_id
        self._magazine_id = magazine_id
        self._content = content
        
        if id is None and author_id and magazine_id:
            with get_db_connection() as conn:
                cursor = conn.execute(
                    "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                    (title, author_id, magazine_id),
                )
                self._id = cursor.lastrowid
        

    def __repr__(self):
        return f"<Article id={self.title}, title='{self.title}', author_id={self.author_id}, magazine_id={self.magazine_id}>"
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if hasattr(self, "_title"):
            raise AttributeError("Title cannot be changed after the article is created.")
        if not isinstance(value, str) or not (5 <= len(value) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters.")
        with get_db_connection() as conn:
            conn.execute("UPDATE articles SET title = ? WHERE id = ?", (value, self.id))
        self._title = value
        
    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            raise ValueError("Content must be a string.")
        self._content = value    

    @property
    def author_id(self):
        if self._author_id is None:
            raise ValueError("Author ID is not set.")
        return self._author_id
    
    @author_id.setter
    def author_id(self, value):
        if not isinstance(value, int):
            raise ValueError("Author ID must be an integer.")
        self._author_id = value

    @property
    def magazine_id(self):
        return self._magazine_id
    
    @magazine_id.setter
    def magazine_id(self, value):
        if not isinstance(value, int):
            raise ValueError("Magazine ID must be an integer.")
        self._magazine_id = value

    # Methods
    @classmethod
    def find_by_id(cls, article_id):
        """
        Fetches an article by its ID from the database.
        """
        with get_db_connection() as conn:
            cursor = conn.execute("""
                SELECT id, title, author_id, magazine_id FROM articles
                WHERE id = ?
            """, (article_id,))
            row = cursor.fetchone()
            if row:
                return cls(id=row[0], title=row[1], author_id=row[2], magazine_id=row[3])
        return None
