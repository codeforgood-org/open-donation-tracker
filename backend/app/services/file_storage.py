"""File storage service for uploads"""
import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile
from PIL import Image
import magic


class FileStorageService:
    """Service for handling file uploads"""

    UPLOAD_DIR = Path("uploads")
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    ALLOWED_DOCUMENT_TYPES = ["application/pdf", "application/msword",
                              "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]

    @classmethod
    def initialize(cls):
        """Create upload directories"""
        (cls.UPLOAD_DIR / "images").mkdir(parents=True, exist_ok=True)
        (cls.UPLOAD_DIR / "documents").mkdir(parents=True, exist_ok=True)
        (cls.UPLOAD_DIR / "avatars").mkdir(parents=True, exist_ok=True)

    @staticmethod
    async def save_image(
        file: UploadFile,
        max_width: int = 1920,
        max_height: int = 1080,
        quality: int = 85
    ) -> str:
        """Save and optimize an image"""
        # Validate file type
        content = await file.read()
        mime = magic.from_buffer(content, mime=True)

        if mime not in FileStorageService.ALLOWED_IMAGE_TYPES:
            raise ValueError(f"Invalid file type: {mime}")

        if len(content) > FileStorageService.MAX_FILE_SIZE:
            raise ValueError("File too large")

        # Generate unique filename
        ext = Path(file.filename).suffix
        filename = f"{uuid.uuid4()}{ext}"
        filepath = FileStorageService.UPLOAD_DIR / "images" / filename

        # Open and optimize image
        image = Image.open(file.file)

        # Convert RGBA to RGB if necessary
        if image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background

        # Resize if needed
        if image.width > max_width or image.height > max_height:
            image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

        # Save optimized image
        image.save(filepath, quality=quality, optimize=True)

        return f"/uploads/images/{filename}"

    @staticmethod
    async def save_avatar(file: UploadFile, size: int = 256) -> str:
        """Save user avatar (square, optimized)"""
        content = await file.read()
        mime = magic.from_buffer(content, mime=True)

        if mime not in FileStorageService.ALLOWED_IMAGE_TYPES:
            raise ValueError(f"Invalid file type: {mime}")

        # Generate unique filename
        filename = f"{uuid.uuid4()}.jpg"
        filepath = FileStorageService.UPLOAD_DIR / "avatars" / filename

        # Open and process image
        image = Image.open(file.file)

        # Convert to RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Create square crop
        width, height = image.size
        min_dimension = min(width, height)
        left = (width - min_dimension) // 2
        top = (height - min_dimension) // 2
        right = left + min_dimension
        bottom = top + min_dimension

        image = image.crop((left, top, right, bottom))
        image = image.resize((size, size), Image.Resampling.LANCZOS)

        # Save avatar
        image.save(filepath, quality=90, optimize=True)

        return f"/uploads/avatars/{filename}"

    @staticmethod
    async def save_document(file: UploadFile) -> str:
        """Save a document file"""
        content = await file.read()
        mime = magic.from_buffer(content, mime=True)

        if mime not in FileStorageService.ALLOWED_DOCUMENT_TYPES:
            raise ValueError(f"Invalid file type: {mime}")

        if len(content) > FileStorageService.MAX_FILE_SIZE:
            raise ValueError("File too large")

        # Generate unique filename
        ext = Path(file.filename).suffix
        filename = f"{uuid.uuid4()}{ext}"
        filepath = FileStorageService.UPLOAD_DIR / "documents" / filename

        # Save file
        with open(filepath, "wb") as f:
            f.write(content)

        return f"/uploads/documents/{filename}"

    @staticmethod
    def delete_file(file_path: str):
        """Delete a file"""
        try:
            full_path = FileStorageService.UPLOAD_DIR / file_path.lstrip("/uploads/")
            if full_path.exists():
                full_path.unlink()
        except Exception as e:
            print(f"Error deleting file {file_path}: {str(e)}")


# Initialize upload directories
FileStorageService.initialize()
