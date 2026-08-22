class UserRoles:
    CONSUMER = 'CONSUMER'
    BRAND_OWNER = 'BRAND_OWNER'
    ADMIN = 'ADMIN'

    CHOICES = [
        (CONSUMER, 'Consumer'),
        (BRAND_OWNER, 'Brand Owner'),
        (ADMIN, 'Platform Admin'),
    ]

# Common layout constraints
MAX_IMAGE_SIZE_MB = 5
MAX_IMAGE_SIZE_BYTES = MAX_IMAGE_SIZE_MB * 1024 * 1024
