from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ("Pending", "Pending"),
    ("Shipped", "Shipped"),
    ("Out for Delivery", "Out for Delivery"),
    ("Delivered", "Delivered"),
    ("Cancelled", "Cancelled"),
    ("Returned", "Returned"),
)


CATEGORY_CHOICES = [
    ('reusable', 'Reusable Products'),
    ('zero_waste', 'Zero-Waste Products'),
    ('home_garden', 'Home and Garden'),
    ('cleaning', 'Eco-friendly Cleaning Products'),
    ('office_school', 'Office & School'),
]


STATE_CHOICES = [
    ('AP', 'Andhra Pradesh'),
    ('AR', 'Arunachal Pradesh'),
    ('AS', 'Assam'),
    ('BR', 'Bihar'),
    ('CT', 'Chhattisgarh'),
    ('GA', 'Goa'),
    ('GJ', 'Gujarat'),
    ('HR', 'Haryana'),
    ('HP', 'Himachal Pradesh'),
    ('JK', 'Jammu and Kashmir'),
    ('JH', 'Jharkhand'),
    ('KA', 'Karnataka'),
    ('KL', 'Kerala'),
    ('MP', 'Madhya Pradesh'),
    ('MH', 'Maharashtra'),
    ('MN', 'Manipur'),
    ('ML', 'Meghalaya'),
    ('MZ', 'Mizoram'),
    ('NL', 'Nagaland'),
    ('OR', 'Odisha'),
    ('PB', 'Punjab'),
    ('RJ', 'Rajasthan'),
    ('SK', 'Sikkim'),
    ('TN', 'Tamil Nadu'),
    ('TS', 'Telangana'),
    ('TR', 'Tripura'),
    ('UP', 'Uttar Pradesh'),
    ('UK', 'Uttarakhand'),
    ('WB', 'West Bengal'),
    ('AN', 'Andaman and Nicobar Islands'),
    ('CH', 'Chandigarh'),
    ('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('LD', 'Lakshadweep'),
    ('DL', 'Delhi'),
    ('PY', 'Puducherry'),
    ('LA', 'Ladakh'),
]




# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255)  # Adjusted max_length to a more reasonable value
    selling_price = models.FloatField()
    discounted_price = models.FloatField()  # Fixed the typo "discountered_price"
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)  # Increased max_length to 20
    product_image = models.ImageField(upload_to='product')  # Fixed upload_to path for clarity

    def __str__(self):
        return self.title
    
# Choices for plastic types
PLASTIC_TYPE_CHOICES = [
    ('pet', 'PET (Polyethylene Terephthalate)'),
    ('hdpe', 'HDPE (High-Density Polyethylene)'),
    ('pvc', 'PVC (Polyvinyl Chloride)'),
    ('ldpe', 'LDPE (Low-Density Polyethylene)'),
    ('pp', 'PP (Polypropylene)'),
    ('ps', 'PS (Polystyrene)'),
    ('other', 'Other Plastics'),
]

# Create your models here
class PlasticItem(models.Model):
    type = models.CharField(choices=PLASTIC_TYPE_CHOICES, max_length=20)
    basic_quantity = models.FloatField(help_text="Basic quantity in kilograms or appropriate units")
    supercoins_for_basic_quantity = models.FloatField(help_text="Supercoins awarded for the basic quantity")
    plastic_image = models.ImageField(upload_to='plastic_items', blank=True, null=True)


    def __str__(self):
        return f"{self.get_type_display()} - {self.basic_quantity} grams"
    def supercoins_for_quantity(self, quantity):
        return (self.supercoins_for_basic_quantity / self.basic_quantity) * quantity
    
class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality =models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    mobile=models.IntegerField(default=0)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=100)
    def __str__(self):
        return self.name
    

"""class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
        
        
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    plastic_item = models.ForeignKey(PlasticItem, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        if self.product:
            print(f"Product found: {self.product.title}, Price: {self.product.discounted_price}, Quantity: {self.quantity}")
            return self.quantity * self.product.discounted_price
        elif self.plastic_item:
            print(f"Plastic Item found: {self.plastic_item.get_type_display}, Quantity: {self.quantity}")
            return 0  # Assuming no cost for plastic items
        return 0

    @property
    def total_supercoins(self):
        if self.plastic_item:
            print(f"Plastic Item Supercoins: {self.plastic_item.supercoins_for_basic_quantity}, Quantity: {self.quantity}")
            return self.quantity * self.plastic_item.supercoins_for_basic_quantity
        return 0
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    plastic_item = models.ForeignKey(PlasticItem, null=True, blank=True, on_delete=models.CASCADE)
    
    # Set the quantity field with validation
    quantity = models.PositiveIntegerField(default=1)

    def clean(self):
        # Validate quantity to be between 1 and 1000 grams for plastic items
        if self.plastic_item and not (1 <= self.quantity <= 1000):
            raise ValidationError('Quantity must be between 1 and 1000 grams for plastic items.')

    @property
    def total_cost(self):
        if self.product:
            print(f"Product found: {self.product.title}, Price: {self.product.discounted_price}, Quantity: {self.quantity}")
            return self.quantity * self.product.discounted_price
        elif self.plastic_item:
            print(f"Plastic Item found: {self.plastic_item.get_type_display}, Quantity: {self.quantity}")
            return 0  # Assuming no cost for plastic items
        return 0

    @property
    def total_supercoins(self):
        if self.plastic_item:
            # Calculate supercoins based on quantity
            supercoins_per_gram = self.plastic_item.supercoins_for_basic_quantity / self.plastic_item.basic_quantity
            print(f"Plastic Item Supercoins per gram: {supercoins_per_gram}, Quantity: {self.quantity}")
            return supercoins_per_gram * self.quantity
        return 0

    def save(self, *args, **kwargs):
        self.clean()  # Call clean to enforce validation before saving
        super().save(*args, **kwargs)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)  # Marks if the payment was successful or not
    
    def __str__(self):
        return f"Payment({self.user}, {self.amount}, Paid: {self.paid})"


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    plastic_item = models.ForeignKey(PlasticItem, on_delete=models.CASCADE, blank=True, null=True)  # Optional for plastic items
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")
    supercoins_used = models.PositiveIntegerField(default=0)

    @property
    def total_cost(self):
        if self.product:
            return self.quantity * self.product.discounted_price
        elif self.plastic_item:
            return 0
        return 0

    @property
    def final_cost(self):
        total = self.total_cost
        return total - self.supercoins_used if total > 0 else 0

    def __str__(self):
        return f"Order({self.user}, {self.product or self.plastic_item}, Status: {self.status})"

