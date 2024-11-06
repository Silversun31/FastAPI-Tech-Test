from fastapi import HTTPException
from starlette import status

COMMENT_NOT_FOUND_EXCEPTION = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
TAG_NOT_FOUND_EXCEPTION = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
POST_NOT_FOUND_EXCEPTION = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
NOT_POST_OWNER_EXCEPTION = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not post's owner")
DUPLICATED_TAG_NAME = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag name already exists")
