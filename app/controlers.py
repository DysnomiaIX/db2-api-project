from litestar import Controller, get, patch, post
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.exceptions import HTTPException, NotFoundException
from sqlalchemy import or_, func

from app.dtos import (
    AuthorReadDTO,
    AuthorReadFullDTO,
    AuthorUpdateDTO,
    AuthorWriteDTO,
    BookReadDTO,
    BookWriteDTO,
    BookUpdateDTO,
    ClientDTO,
    ClientWriteDTO,
    LibraryDTO,
    LibraryWriteDTO,
)
from app.models import Author, Book, Client, Library
from app.repositories import (
    AuthorRepository,
    BookRepository,
    ClientRepository,
    LibraryRepository,
    provide_authors_repo,
    provide_books_repo,
    provide_clients_repo,
    provide_library_repo,
)


class AuthorController(Controller):
    path = "/authors"
    tags = ["authors"]
    return_dto = AuthorReadDTO
    dependencies = {"authors_repo": Provide(provide_authors_repo)}

    @get()
    async def list_authors(self, authors_repo: AuthorRepository) -> list[Author]:
        return authors_repo.list()

    @post(dto=AuthorWriteDTO)
    async def create_author(self, data: Author, authors_repo: AuthorRepository) -> Author:
        return authors_repo.add(data)

    @get("/{author_id:int}", return_dto=AuthorReadFullDTO)
    async def get_author(self, author_id: int, authors_repo: AuthorRepository) -> Author:
        try:
         return authors_repo.get(author_id)
        except:
         raise NotFoundException("Autor no existente")
            

    @patch("/{author_id:int}", dto=AuthorUpdateDTO)
    async def update_author(
            self, author_id: int, data: DTOData[Author], authors_repo: AuthorRepository
        ) -> Author:
            
            try:
                author = authors_repo.get(author_id)
                author = data.update_instance(author)
                return authors_repo.update(author)
            except:
                raise NotFoundException("Autor no existente o no encontrado")

class BookController(Controller):
    path = "/books"
    tags = ["books"]
    return_dto = BookReadDTO
    dependencies = {"books_repo": Provide(provide_books_repo)}

    @get()
    async def list_books(self, books_repo: BookRepository) -> list[Book]:
        return books_repo.list()

    @post(dto=BookWriteDTO)
    async def create_book(self, data: Book, books_repo: BookRepository) -> Book:
        return books_repo.add(data)
    

    @get("/{book_id:int}", return_dto=BookReadDTO)
    async def get_book(self, book_id: int, books_repo: BookRepository) -> Book:
           try:
             return books_repo.get(book_id)
           except:
               raise NotFoundException("Libro no encontrado o no existente")

    @patch("/{book_id:int}", dto=BookUpdateDTO, return_dto=BookReadDTO)
    async def update_book(
        self, book_id: int, data: DTOData[Book], books_repo: BookRepository
    ) -> Book:
     try:
        book = books_repo.get(book_id)
        book = data.update_instance(book)
        return books_repo.update(book)
     except:
         raise NotFoundException("LIbro no encontrado o no existente")
    
    @get('/search')
    async def search_book(self, title: str, books_repo: BookRepository) -> list[Book]:
        session = books_repo.session
        result_search = session.query(Book).filter(func.lower(Book.title).like(f"%{title.lower()}")).all()

        if not result_search:
            raise HTTPException(status_code=404, detail="Libro no encontrado o no existente")

        return result_search

class ClientController(Controller):
    path = "/clients"
    tags = ["clients"]
    return_dto = ClientDTO
    dependencies = {"clients_repo": Provide(provide_clients_repo)}

    @get()
    async def list_clients(self, clients_repo: ClientRepository) -> list[Client]:
        return clients_repo.list()
    


    @post(dto=ClientWriteDTO)
    async def create_client(self, data: Client, clients_repo: ClientRepository) -> Client:
        return clients_repo.add(data)
    

    @get("/{client_id:int}", return_dto=ClientDTO)
    async def get_client(self, client_id: int, clients_repo: ClientRepository) -> Client:
        try:
            return clients_repo.get(client_id)
        except:
            raise NotFoundException("Cliente no encontrado")
        

class LibraryController(Controller):
    path= "/library"
    tags = ["library"]
    return_dto = LibraryDTO
    dependencies = {"books_repo": Provide(provide_books_repo), "library_repo": Provide(provide_library_repo)}



    @get("/rented")
    async def rent_list(self, library_repo: LibraryRepository) -> list[Library]:
        return library_repo.list()

    @post(dto=LibraryWriteDTO)
    async def rent_book(self, data: Library, library_repo: LibraryRepository, book_repo: BookRepository
    ) -> Library:
            library_repo.add(data)
            return data
            


    @post("/return")
    async def return_book(self, client_id: int, book_id:int, library_repo: LibraryRepository) -> Library:
        rented = library_repo.get_rented(client_id)
        
        try:
            library_repo.return_book(rented)
            return {"message": "Libro retornado"}
        
        except:
             raise NotFoundException("no encontrado")
        
    @patch("/EditRent", return_dto=LibraryWriteDTO)
    async def edit_rented_book(self, id_rented: int, data: Library, library_repo: LibraryRepository) -> Library:
        library= library_repo.get(id_rented)
        library= data.update_instance(library)
        return library_repo.update(library)
    
    @get("/{rented:int}", return_dto=LibraryDTO)
    async def get_info_rented(self, rented: int, library_repo: LibraryRepository) -> Library:
        try:
            return library_repo.get(rented)
        except:
            raise NotFoundException("no entcontrado o no existente")