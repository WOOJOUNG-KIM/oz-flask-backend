from flask_smorest import Blueprint , abort
from flask.views import MethodView
from schemas import BookSchema

blp = Blueprint("books", __name__, url_prefix="/books")

# 데이터 저장소
books = []
book_id_counter = 1 # 자동증가 ID

@blp.route("/")
class BookList(MethodView):
    @blp.response(200, BookSchema(many=True))
    def get(self):
        # 모든 책 조회
        return books
    
    @blp.arguments(BookSchema)
    @blp.response(201, BookSchema)
    def post(self, new_book):
        # 새로운 책 추가
        global book_id_counter
        new_book["id"] = book_id_counter
        book_id_counter += 1
        books.append(new_book)
        return new_book
    
@blp.route("/<int:book_id>")
class BookResource(MethodView):
    @blp.response(200, BookSchema)
    def get(self, book_id):
        # 특정 책 조회
        book = next((b for b in books if b["id"] == book_id), None)
        if not book:
            abort(404, message="Book not found")
        return book
    
    @blp.arguments(BookSchema)
    @blp.response(200, BookSchema)
    def put(self, updated_book, book_id):
        # 특정 책 정보 수정
        book = next((b for b in books if b["id"] == book_id), None)
        if not book:
            abort(404, message="Book not found")
        book.update(updated_book)
        return book
    
    @blp.response(204)
    def delete(self, book_id):
        # 특정 책 삭제
        global books
        books = [b for b in books if b["id"] != book_id]
        return ""

    