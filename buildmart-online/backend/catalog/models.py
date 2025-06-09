from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children'
    )
    image_url = models.CharField(max_length=255, blank=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    logo_url = models.CharField(max_length=255, blank=True)
    website = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.CharField(max_length=255)
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.product.name} image"


class SpecificationType(models.Model):
    name = models.CharField(max_length=255)
    data_type = models.CharField(max_length=50)
    unit = models.CharField(max_length=50, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    specification_type = models.ForeignKey(SpecificationType, on_delete=models.CASCADE)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.specification_type.name}: {self.value}"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    variant_name = models.CharField(max_length=255)
    price_difference = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_quantity = models.IntegerField(default=0)
    sku = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.variant_name}"
