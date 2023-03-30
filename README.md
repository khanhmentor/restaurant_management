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

#### `a = {'MAIN COURSES': [["Shepherd's Pie with Garden Salad", 'Ground beef, lamb & vegetables crowned with potatoes', '16.99'], ["Beef Pasties with Garden Salad", 'Flakey pastry pies filled with ground beef, vegetables & potatoes served with a side salad & choice of dressing', '11.99'],["Spareribs Platter", 'Served with corn on the cob and roasted potatoes', '19.99'], ["Smoked Turkey Leg", 'Served with wedge fries', '16.49'], ["Fish and Chips", 'Fresh north Atlantic cod battered & fried with chips and tartar sauce', '16.99'], ["Rotisserie Smoked Chicken", 'Served with corn on the cob and roasted potatoes', '15.49'], ["Chicken and Ribs Platter", 'Served with corn on the cob and roasted potatoes', '18.49'], ["Mushroom Pie Platter", 'Stewed jackfruit and mushroom pie served with a cucumber, tomato side salad with lemon Thyme vinaigrette dressing', '16.99']], 'SALADS': [['Soup & Salad Combo', 'Leek & Potato or Split Pea & Ham Soup. Side salad and choice of dressing', '11.99'], ['Soup', 'Leek & Potato or Split Pea & Ham Soup', '5.99'], ['Rotisserie Smoked Chicken Salad', 'Over a bed of fresh greens with choice of dressing', '12.49']], "CHILDREN'S MENU": [['Fish & Chips', 'includes chips and grapes', '7.49'], ['Chicken Legs', '', '7.49'], ['Chicken Fingers', '', '7.49'], ['Macaroni Cheese', '', '7.49']], 'SIDE ITEMS': [['Roasted Potatoes', 'garlic herb roasted', '4.49'], ['Corn on the Cob', '', '4.49'], ['Fresh Garden Salad', 'with choice of dressing', '6.99'], ['Baked Potato', 'topped with butter & sour cream', '4.49'], ['Seasoned Wedge Fries', '', '4.49'], ['Fruit Cup', '', '4.49']], 'DESSERTS': [['Butterbeer™ Potted Cream', 'garlic herb roasted', '5.49'], ['Cup of Ice Cream', 'Strawberry and Peanut Butter, Vanilla or Chocolate', '5.49'], ['Chocolate Trifle', 'Layered chocolate cake with fresh berries & cream', '4.99'], ['Butterbeer™ Ice Cream', '', '5.99'], ['Freshly Baked Apple Pie', '', '4.49']], 'BEVERAGES': [['Souvenir Butterbeer™', 'A non-alcoholic sweet drink reminiscent of shortbread and butterscotch, served in a souvenir cup', '12.49'], ['Souvenir Frozen Butterbeer™', 'A non-alcoholic sweet drink reminiscent of shortbread and butterscotch, served in a souvenir cup', '13.49'], ['Hot Butterbeer™', '', '7.99'], ['Pumpkin Fizz', '', '4.99'], ['Cider (Non-Alcoholic)', 'Apple or Pear', '4.29'], ['Gillywater', '', '5.50'], ['Hot Beverages', 'coffee, hot tea, hot cocoa', '3.49'], ['Butterbeer™', 'A non-alcoholic sweet drink reminiscent of shortbread and butterscotch', '7.99'], ['Frozen Butterbeer™', 'A non-alcoholic sweet drink reminiscent of shortbread and butterscotch', '7.99'], ['Pumpkin Juice™', '', '4.49'], ['Lemonade', '', '4.29'], ['Iced Tea', 'Sweet, Unsweetened, Raspberry, Lemonade Mix', '4.29'], ['Sparkling Water', '', '5.50'], ['Milkr', '', '2.29']], 'DRAUGHT BEERS': [['Draught Beer', "Hog's Head™ Brew or Dragon Scale", '12.00']]}`

#### `for type in a:`
####    `menu_type = MenuType(name=type)`
####    `menu_type.save()`
####    `lst = a[type]`
####    `for item in lst:`
####        `menu_item = MenuItem(name=item[0], type=menu_type, description=item[1], price=item[2], photo=item[0]+'.jpg')`
####        `menu_item.save()`

- ### `py manage.py runserver` (`python3 manage.py runserver`)
- ### the site is now listening at [http://localhost:8000](http://localhost:8000)
- ### use these pre-established accounts for authentication or you can modify the code above to create any account you want

## If you have any issue with session use the following code in shell to modify or event delete existing session:

#### `from django.contrib.sessions.models import Session`

#### `Session.objects.all()`: to get all existing session and modify them (`.delete()` to remove them)