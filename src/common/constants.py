from fastapi import HTTPException, status

USERNAME_LENGTH = 20
BANK_COMMENT_LENGTH = 500
AMOUNT_ACCURANCY = (10, 2)
# ============= Exceptions ====================
USER_NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь с таким ID не найден")
USER_NOT_SELF_CHANGES = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Нельзя редактировать собственные данные"
)
