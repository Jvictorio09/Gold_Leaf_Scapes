"""
Cloudinary utility functions for image upload and compression.
Handles WebP conversion, compression, and Cloudinary upload with multiple URL variants.
"""
import io
from pathlib import Path
from typing import Tuple, Dict, Optional
from PIL import Image, ImageOps
import cloudinary
import cloudinary.uploader
from cloudinary.exceptions import Error as CloudinaryError

# Cloudinary upload limits
MAX_BYTES = 10 * 1024 * 1024  # 10MB Cloudinary limit
TARGET_BYTES = int(MAX_BYTES * 0.93)  # 9.3MB target (safety margin)


def smart_compress_to_bytes(src_file) -> bytes:
    """
    Accepts a file-like object or path; returns compressed bytes <= TARGET_BYTES.
    
    Process:
    1. Load image with PIL/Pillow
    2. Auto-rotate based on EXIF data
    3. Determine optimal format (WebP for PNG/TIFF, JPEG for photos)
    4. Resize if width > 5000px
    5. Iteratively reduce quality until under TARGET_BYTES
    6. Return compressed bytes
    
    Args:
        src_file: File-like object (request.FILES['file']) or file path (str/Path)
    
    Returns:
        bytes: Compressed image data ready for upload
    """
    # Load into Pillow
    if isinstance(src_file, (str, Path)):
        im = Image.open(src_file)
    else:
        im = Image.open(src_file)

    with im:
        # Step 1: Auto-rotate based on EXIF orientation
        im = ImageOps.exif_transpose(im)
        
        # Step 2: Determine optimal output format
        fmt = (im.format or "JPEG").upper()
        prefer_webp = fmt in ("PNG", "TIFF")  # PNG/TIFF → WebP (better compression)
        out_fmt = "WEBP" if prefer_webp else ("JPEG" if fmt != "WEBP" else "WEBP")
        
        # Step 3: Cap extreme dimensions (resize if too large)
        max_w = 5000
        if im.width > max_w:
            im = im.resize(
                (max_w, int(im.height * (max_w / im.width))), 
                Image.LANCZOS  # High-quality resampling
            )
        
        # Step 4: Iterative quality reduction
        q = 82  # Start with high quality
        min_q = 50 if out_fmt == "JPEG" else 45  # Minimum quality thresholds
        step = 4  # Quality reduction step
        
        while True:
            buf = io.BytesIO()
            
            if out_fmt == "JPEG":
                # JPEG settings: progressive, optimized, chroma subsampling
                im.save(
                    buf, 
                    format="JPEG", 
                    quality=q, 
                    optimize=True, 
                    progressive=True, 
                    subsampling="4:2:0"
                )
            else:
                # WebP settings: method 6 (best compression)
                im.save(
                    buf, 
                    format="WEBP", 
                    quality=q, 
                    method=6
                )
            
            data = buf.getvalue()
            
            # Success condition: under target size OR at minimum quality
            if len(data) <= TARGET_BYTES or q <= min_q:
                return data
            
            # Reduce quality and try again
            q = max(min_q, q - step)


def upload_to_cloudinary(
    file_bytes: bytes, 
    folder: str, 
    public_id: str, 
    tags: Optional[list] = None
) -> Tuple[Dict, str, str]:
    """
    Upload image to Cloudinary and return multiple URL variants.
    
    Args:
        file_bytes: Compressed image bytes (from smart_compress_to_bytes)
        folder: Cloudinary folder path (e.g., "uploads/projects")
        public_id: Unique identifier (e.g., "dubai-hills-hero")
        tags: List of tags for organization (e.g., ["project", "hero"])
    
    Returns:
        tuple: (result_dict, web_url, thumb_url)
        - result_dict: Full Cloudinary API response
        - web_url: Optimized URL for web use (f_auto,q_auto)
        - thumb_url: Thumbnail URL (c_fill,g_face,w_480,h_320)
    """
    result = cloudinary.uploader.upload(
        file=io.BytesIO(file_bytes),  # Convert bytes to file-like object
        resource_type="image",
        folder=folder or "uploads",
        public_id=public_id,
        overwrite=True,  # Replace if exists (useful for updates)
        unique_filename=False,  # Use provided public_id exactly
        use_filename=False,  # Don't use original filename
        eager=[{
            "format": "webp",
            "quality": "auto",
            "fetch_format": "auto",
            "crop": "limit",
            "width": 2400
        }],  # Pre-generate WebP variant (eager transformation)
        tags=(tags or []),  # Organization tags
        timeout=120,  # 2 minute timeout for large files
    )
    
    # Extract base secure URL
    secure_url = result.get("secure_url", "")
    
    # Generate URL variants via URL manipulation (no re-upload needed)
    if "/upload/" in secure_url:
        # Web-optimized URL: auto format & quality
        web_url = secure_url.replace(
            "/upload/", 
            "/upload/f_auto,q_auto/"
        )
        # Thumbnail URL: smart crop with face detection
        thumb_url = secure_url.replace(
            "/upload/", 
            "/upload/c_fill,g_face,w_480,h_320/"
        )
    else:
        web_url = secure_url
        thumb_url = secure_url
    
    return result, web_url, thumb_url

