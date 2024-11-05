from app.main import app
from . import user, post, tag, comment

urlpatterns = [
    app.include_router(user.router),
    app.include_router(post.router),
    app.include_router(tag.router),
    app.include_router(comment.router)
]
