from django.db import models
from django.utils import timezone

# Create your models here.

class Employee(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    role = models.CharField(max_length=20)
    n_o_w = models.IntegerField(default=0)
    is_signed_in = models.BooleanField(default=False)
    sign_in_time = models.DateTimeField(null=True, blank=True)
    sign_out_time = models.DateTimeField(null=True, blank=True)
    session_id = models.CharField(max_length=32, null=True, blank=True)

    def sign_in(self, session_id):
        self.is_signed_in = True
        self.sign_in_time = timezone.now()
        self.session_id = session_id
        self.save()

    def sign_out(self):
        self.is_signed_in = False
        self.sign_out_time = timezone.now()
        self.session_id = None
        self.save()

    def __str__(self):
        return self.username

class Table(models.Model):
    number = models.IntegerField()
    is_using = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.number} - is_using {self.is_using}' 
    
class Customer(models.Model):
    name = models.CharField(max_length=200)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.customer.name} - Table {self.table.number}'

    def get_total_cost(self):
        total = sum(item.sub_total_cost for item in self.order_items.all() if item.status.name not in ['denied', 'waiting'])
        self.total_cost = total
        self.save()

class Emp_Order(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE)

class MenuType(models.Model):
    name = models.CharField(max_length=255)

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(MenuType, on_delete=models.CASCADE, default=0)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menu = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    note = models.CharField(max_length=255, default='None')
    sub_total_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.quantity} x {self.menu.name}'
    
    def get_subtotal_cost(self):
        sub_total = self.menu.price * self.quantity
        self.sub_total_cost = sub_total
        self.save()
