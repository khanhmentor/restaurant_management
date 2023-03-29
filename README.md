# Restaurant Management - Order Management System

## Do all the following to run the project:

- ### `py manage.py makemigrations order_management` (`python3 manage.py makemigrations order_management`)
- ### `py manage.py migrate` (`python3 manage.py migrate`)
- ### `py manage.py shell` (`python3 manage.py shell`)
- ### type the below in shell:

#### `from order_management.models import Employee, Status, MenuItem, Table`

#### `a = ['waiter', 'waiter1', 'cook', 'manager']`

#### `for i in a:`
####    `employee = Employee(username=i, password=i)`
####    `employee.save()`

#### `for i in range(1, 11):`
####    `table = Table(number=i, is_using=False)`
####    `table.save()`

#### `a = ['waiting', 'preparing', 'cooking', 'done', 'denied', 'stopped']`

#### `for i in a:`
####    `status = Status(name=i)`
####    `status.save()`

#### `a = ['THE GREAT FEAST', 'MAIN COURSES', 'SALADS', "CHILDREN'S MENU", 'SIDE ITEMS', 'DESSERTS', 'BEVERAGES', 'DRAUGHT BEERS']`

#### `for i in a:`
####    `menu_type = MenuType(name=i)`
####    `menu_type.save()`

#### `menu_item = MenuItem(name='cookie', description='delicious', price=5, is_available=True)`
#### `menu_item.save()`
#### `menu_item = MenuItem(name='biscuit', description='fantastic', price=12, is_available=True)`
#### `menu_item.save()`

- ### `py manage.py runserver` (`python3 manage.py runserver`)
- ### the site is now listening at [http://localhost:8000](http://localhost:8000)
- ### use these pre-established accounts for authentication or you can modify the code above to create any account you want

## If you have any issue with session use the following code in shell to modify or event delete existing session:

#### `from django.contrib.sessions.models import Session`

#### `Session.objects.all()`: to get all existing session and modify them (`.delete()` to remove them)