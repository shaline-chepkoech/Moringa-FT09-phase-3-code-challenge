from database.connection import get_db_connection

class Author:
    def __init__(self, id=None, name=None):
        if id is not None and not isinstance(id, int):
            raise TypeError("id must be of type int")
        if name is not None and not isinstance(name, str):
            raise TypeError("name must be of type str")
        if name and len(name) == 0:
            raise ValueError("name must be longer than 0 characters")
        
        self._id = id
        self._name = name
        
        if name and id is None:
            self.create_in_database()
               
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise TypeError("id must be of type int")
        self._id = value

    @property
    def name(self):
        if self._name is None:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('SELECT name FROM authors WHERE id = ?', (self._id,)) 
                    result = cursor.fetchone()
                    if result:
                         self._name = result["name"]
                except Exception as e:
                    print(f"Error fetching name from database: {e}")
        return self._name
    
    @name.setter
    def name(self, value):
        if hasattr(self, "_name") and self._name is not None:
            raise AttributeError("Cannot change name after it is set")
        if not isinstance(value, str):
            raise TypeError("name must be of type str")
        if len(value) == 0:
            raise ValueError("name must be longer than 0 characters")
        self._name = value                
                   
            
    def _create_in_database(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()        
            try:
                cursor.execuye('INSERT INTO authors (name) VALUES (?)', (self.name,))
                self.id = cursor.lastrowid 
                conn.commit()            
            except Exception as e:
                print(f"Error inserting author into the database: {e}")  
    def articles(self):
         from models.article import Article
         
         articles = []
         with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    SELECT a.id, a.title, a.author_id, a.magazine_id
                    FROM articles a
                    WHERE a.author_id = ?
                    """,
                    (self._id,),
                )
                rows = cursor.fetchall()
                for row in rows:
                    articles.append(Article(id=row["id"], title=row["title"], author=self, magazine=row["magazine_id"]))
            except Exception as e:
                print(f"Error fetching articles for author: {e}")
         return articles

    def magazines(self):
        """
        Returns all magazines the author has contributed to.
        """
        from models.magazine import Magazine

        magazines = []
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    (self._id,),
                )
                rows = cursor.fetchall()
                for row in rows:
                    magazines.append(Magazine(id=row["id"], name=row["name"], category=row["category"]))
            except Exception as e:
                print(f"Error fetching magazines for author: {e}")
        return magazines 
                   
                        
    def __repr__(self):
         return f"<Author id={self.id}, name='{self.name}'>" 
     
               
        
        
        

   
