"""File upload endpoints"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.file_storage import FileStorageService

router = APIRouter(prefix="/files", tags=["Files"])


@router.post("/upload/image")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """Upload an image file"""
    try:
        file_path = await FileStorageService.save_image(file)
        return {
            "file_path": file_path,
            "filename": file.filename,
            "content_type": file.content_type
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload file"
        )


@router.post("/upload/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload user avatar"""
    try:
        # Delete old avatar if exists
        if hasattr(current_user, 'avatar_url') and current_user.avatar_url:
            FileStorageService.delete_file(current_user.avatar_url)

        # Save new avatar
        file_path = await FileStorageService.save_avatar(file)

        # Update user avatar
        current_user.avatar_url = file_path
        db.commit()

        return {
            "file_path": file_path,
            "filename": file.filename
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload avatar"
        )


@router.post("/upload/document")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """Upload a document file"""
    try:
        file_path = await FileStorageService.save_document(file)
        return {
            "file_path": file_path,
            "filename": file.filename,
            "content_type": file.content_type
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload document"
        )
