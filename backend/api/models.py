from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=300, blank=True)
    cover_image = models.ImageField(upload_to='restaurants/', null=True, blank=True)

    def __str__(self):
        return self.name

class MenuCategory(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    photo = models.ImageField(upload_to='menu_items/', null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    def __str__(self): return self.name
    def formatted_price(self): return f"{self.price} Kč"

class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    party_size = models.PositiveIntegerField()
    datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self): return f"{self.name} @ {self.datetime}"
