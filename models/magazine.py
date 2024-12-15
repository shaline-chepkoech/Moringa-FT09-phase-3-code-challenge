from database.connection import get_db_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        # Validate and set name and category if provided
        if name is not None and (not isinstance(name, str) or not (2 <= len(name) <= 16)):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        if category is not None and (not isinstance(category, str) or len(category) == 0):
            raise ValueError("Category must be a non-empty string.")
        
        self._id = id
        self._name = name
        self._category = category
        
        if id is None:
            with get_db_connection() as conn:
                cursor = conn.execute(
                    "INSERT INTO magazines (name, category) VALUES (?, ?)", (name, category)
                )
                self._id = cursor.lastrowid

    def __repr__(self):
        #return f'<Magazine {self.name}>'
        return f"Magazine(id={self.id}, name='{self.name}', category='{self.category}')"
    
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        with get_db_connection() as conn:
            conn.execute("UPDATE magazines SET name = ? WHERE id = ?", (value, self.id))
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string.")
        with get_db_connection() as conn:
            conn.execute("UPDATE magazines SET category = ? WHERE id = ?", (value, self.id))
        self._category = value
    def articles(self):
        """
        Returns a list of titles of all articles written for this magazine.
        """
        with get_db_connection() as conn:
            cursor = conn.execute("""
                SELECT title FROM articles
                WHERE magazine_id = ?
            """, (self.id,))
            return [row[0] for row in cursor.fetchall()]

    def contributors(self):
        """
        Returns a list of distinct authors who have written articles for this magazine.
        """
        with get_db_connection() as conn:
            cursor = conn.execute("""
                SELECT DISTINCT a.name FROM authors a
                JOIN articles ar ON a.id = ar.author_id
                WHERE ar.magazine_id = ?
            """, (self.id,))
            return [row[0] for row in cursor.fetchall()]

    def article_titles(self):
        """
        Returns a list of all article titles written for this magazine.
        Returns None if there are no articles.
        """
        titles = self.articles()
        return titles if titles else None

    def contributing_authors(self):
        """
        Returns a list of authors who have written more than 2 articles for this magazine.
        """
        with get_db_connection() as conn:
            cursor = conn.execute("""
                SELECT a.id, a.name FROM authors a
                JOIN articles ar ON a.id = ar.author_id
                WHERE ar.magazine_id = ?
                GROUP BY a.id
                HAVING COUNT(ar.id) > 2
            """, (self.id,))
            return [row[1] for row in cursor.fetchall()]
