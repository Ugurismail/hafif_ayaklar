"""
File and Image validators for uploaded content
"""
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


def validate_image_file(image):
    """
    Validate uploaded image files
    - Check file size (max 5MB)
    - Check file extension
    - Check if it's actually an image
    - Check dimensions (max 4000x4000)
    """
    # Maximum file size: 5MB
    max_size_mb = 5
    max_size_bytes = max_size_mb * 1024 * 1024

    if image.size > max_size_bytes:
        raise ValidationError(f'Dosya boyutu çok büyük. Maksimum {max_size_mb}MB olabilir.')

    # Valid image extensions
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    ext = image.name.lower().split('.')[-1]
    if f'.{ext}' not in valid_extensions:
        raise ValidationError(f'Geçersiz dosya formatı. İzin verilen formatlar: {", ".join(valid_extensions)}')

    # Check actual image dimensions
    try:
        width, height = get_image_dimensions(image)
        if width is None or height is None:
            raise ValidationError('Dosya geçerli bir resim dosyası değil.')

        # Maximum dimensions
        max_dimension = 4000
        if width > max_dimension or height > max_dimension:
            raise ValidationError(f'Resim boyutları çok büyük. Maksimum {max_dimension}x{max_dimension} piksel olabilir.')
    except Exception as e:
        raise ValidationError('Dosya geçerli bir resim dosyası değil.')

    return image


def validate_file_size(file, max_mb=10):
    """
    Generic file size validator
    """
    max_bytes = max_mb * 1024 * 1024
    if file.size > max_bytes:
        raise ValidationError(f'Dosya boyutu çok büyük. Maksimum {max_mb}MB olabilir.')
    return file
