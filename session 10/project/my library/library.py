class Library:
    def __init__(self, name="My Library"):
        self.name = name
        self.books = {}

    def add_book(self, title, author):
        if title in self.books:
            print(f"This {title} is already in the library!")

        else:
            self.books[title] = author
            print(f"{title} by {author} added")
        
    def remove_book(self, title):
        if title in self.books:
            del self.books[title]
            print(f"{title} removed")

        else:
            print(f"{title} not found!")

    def search_book(self, title):
        if title in self.books:
            author = self.books[title]
            print(f"Book found: {title} by {author}")
            return {"title": title, "author": author}
        else:
            print(f"{title} not found!")
            return None
    def show_books(self):
        if not self.books:
            print("Library is empty!")

        else:
            print(f"{self.name}")

            for i, (title, author) in enumerate(self.books.items(), 1):
                print(f"{i}. '{title}' by {author}")
            print(f"Totally: {len(self.books)}\n")




        