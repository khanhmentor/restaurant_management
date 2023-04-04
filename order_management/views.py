from .models import Employee, Table, Customer, Order, Emp_Order, MenuType, MenuItem, Status, OrderItem, TempItem
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib import messages

# Create your views here.

def insert(request, type_id, order, order_id):
    if request.method == 'POST':
        item_id = request.POST['item-id']
        quantity = int(request.POST['quantity'])
        note = request.POST['note']
        menu_item = get_object_or_404(MenuItem, id=item_id)
        status = get_object_or_404(Status, id=1)
        temp_items = TempItem.objects.create(order=order, menu=menu_item, quantity=quantity, note=note, status=status)
        temp_items.get_subtotal_cost()
        temp_items.save()
        return redirect('view_menu', type_id, order_id)

def view_menu(request, type_id, order_id):
    order = get_object_or_404(Order, id=order_id)
    emp_orders = Emp_Order.objects.all().filter(order=order)

    if request.session.session_key not in [emp_order.emp.session_id for emp_order in emp_orders if emp_order.emp.session_id != None]:
        return redirect('none_of_your_bussiness')
    
    starting_type = MenuType.objects.all()[0]
    starting_menu = MenuItem.objects.all().filter(type=starting_type, is_available=True)

    if type_id != 0:
        new_type = get_object_or_404(MenuType, id=type_id)
        new_menu = MenuItem.objects.all().filter(type=new_type, is_available=True)
        context = {
            'order_id': order_id,
            'menu_types': MenuType.objects.all(),
            'menu_items': new_menu,
            'current_type_id': type_id
        }
        insert(request, type_id, order, order_id)

        return render(request, 'view_menu.html', context)
    
    insert(request, type_id, order, order_id)

    context = {
        'order_id': order_id,
        'menu_types': MenuType.objects.all(),
        'menu_items': starting_menu,
        'current_type_id': starting_type.id
    }
    return render(request, 'view_menu.html', context)

def about(request, order_id):
    starting_type = MenuType.objects.all()[0]

    context = {
        'order_id': order_id,
        'current_type_id': starting_type.id
    }
    return render(request, 'about.html', context)

@csrf_exempt
def view_cart(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    emp_orders = Emp_Order.objects.all().filter(order=order)

    if request.session.session_key not in [emp_order.emp.session_id for emp_order in emp_orders if emp_order.emp.session_id != None]:
        return redirect('none_of_your_bussiness')

    starting_type = MenuType.objects.all()[0]
    temp_items = TempItem.objects.all().filter(order=order)
    available_temp_items = [item for item in temp_items if item.menu.is_available == True]

    if request.method == 'POST':
        if (request.POST['form_name'] == "Confirmed"):
            for temp_item in available_temp_items:
                order_item = OrderItem()
                order_item.order = temp_item.order
                order_item.menu = temp_item.menu
                order_item.quantity = temp_item.quantity
                order_item.note = temp_item.note
                order_item.status = temp_item.status
                order_item.get_subtotal_cost()
                order_item.save()
            temp_items.delete()
        else:
            item_id = request.POST['item-id']
            quantity = int(request.POST['quantity'])
            note = request.POST['note']
            temp_item = get_object_or_404(TempItem, id=item_id)
            temp_item.quantity = quantity
            temp_item.note = note
            temp_item.get_subtotal_cost()
            temp_item.save()

        return redirect('view_cart', order_id)    

    context = {
        'order': order,
        'temp_items': available_temp_items,
        'current_type_id': starting_type.id,
    }
    return render(request, 'view_cart.html', context)

def local_host(request):
    return redirect('home_page', 0)

def sign_in(request):
    if request.session.session_key:
        emp = get_object_or_404(Employee, session_id=request.session.session_key)
        return redirect('home_page', emp.id)
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            try:
                emp = Employee.objects.get(username=username, password=password)
                if emp.is_signed_in:       
                    messages.error(request, 'You are already signed in on another browser.')
                elif emp.n_o_w > 3:
                    messages.error(request, 'You have been BANNED PERMANENTLY! Please contact employee faculty if you think that there is something wrong')
                else:
                    if not request.session.session_key:
                        request.session.save()
                    session_key = request.session.session_key
                    emp.sign_in(session_key)
                    return redirect('home_page', emp.id)
            except Employee.DoesNotExist:
                messages.error(request, 'Invalid username or password.')
    
    return render(request, 'sign_in.html')

def sign_out(request, emp_id):
    try:
        emp = get_object_or_404(Employee, id=emp_id)
        if request.session.session_key == emp.session_id:
            emp.sign_out()
            request.session.flush()
            return redirect('sign_in')
        else:
            messages.error(request, 'You are not signed in on this browser.')
    except Employee.DoesNotExist:
        messages.error(request, 'Invalid employee ID.')
    
    return render(request, 'sign_out.html')

def home_page(request, emp_id):
    if emp_id == 0:
        return redirect('sign_in')
    else:
        emp = get_object_or_404(Employee, id=emp_id)

        if not emp.is_signed_in or request.session.session_key != emp.session_id:
            return redirect('none_of_your_bussiness')
        
    context = {
        'emp': emp
    }
    return render(request, 'home_page.html', context)

def new_order(request, emp_id):
    emp = Employee.objects.get(id=emp_id)
    if (emp.role not in ['waiter', 'manager']):
        return redirect('none_of_your_bussiness')
    if not emp.is_signed_in or request.session.session_key != emp.session_id:
        return redirect('none_of_your_bussiness')
    
    if request.method == 'POST':
        table = get_object_or_404(Table, id=request.POST['table_number_id'])
        if table.is_using == False:
            manager = Employee.objects.get(is_signed_in=True, role='manager')
            customer = Customer.objects.create(name=request.POST['customer_name'])
            order = Order.objects.create(customer=customer, table=table)
            if emp == manager:
                emp_order = Emp_Order.objects.create(order=order, emp=emp)
            else:
                emp_order = Emp_Order.objects.create(order=order, emp=emp)
                emp_order = Emp_Order.objects.create(order=order, emp=manager)
            table.is_using = True
            table.save()
            return redirect('order_detail', emp.id, order.id)
        else:
            messages.error(request, 'This table is already in use. Please choose another.')  
    
    context = {
        'tables': Table.objects.all()
    }
    return render(request, 'new_order.html', context)

def view_order(request, emp_id):
    emp = Employee.objects.get(id=emp_id)
    if (emp.role not in ['waiter', 'manager']):
        return redirect('none_of_your_bussiness')
    if not emp.is_signed_in or request.session.session_key != emp.session_id:
        return redirect('none_of_your_bussiness')

    emp_order = Emp_Order.objects.all().filter(emp=emp)
    orders = [emp_o.order for emp_o in emp_order]
    for order in orders:
        order.get_total_cost()

    if len(orders) < 1:
        messages.error(request, 'There is no order at all')
        
    context = {
        'emp': emp,
        'orders': orders,
    }
    return render(request, 'view_order.html', context)

def none_of_your_bussiness(request):
    emp = get_object_or_404(Employee, session_id=request.session.session_key)
    emp.n_o_w += 1
    emp.save()

    if emp.n_o_w > 1:
        if emp.n_o_w < 3:
            messages.error(request, 'Caution ' + emp.username + ', this is the SECOND warning! You will receive PERMANENT BAN after THREE-TIME WARNING')
        elif emp.n_o_w == 3:
            messages.error(request, 'Caution ' + emp.username + ', this is the FINAL warning! You will receive PERMANENT BAN after THREE-TIME WARNING')
        else:
            messages.error(request, 'You have been BANNED PERMANENTLY! Please contact employee faculty if you think that there is something wrong')
            emp.sign_out()
            request.session.flush()
            return redirect('sign_in')
    else:
        messages.error(request, 'Caution ' + emp.username + ', this is the FIRST warning! You will receive PERMANENT BAN after THREE-TIME WARNING')
    
    return render(request, 'none_of_your_bussiness.html')

def update_menu(request, emp_id):
    emp = get_object_or_404(Employee, id=emp_id)
    if (emp.role!='cook'):
        return redirect('none_of_your_bussiness')
    if not emp.is_signed_in or request.session.session_key != emp.session_id:
        return redirect('none_of_your_bussiness')
    
    if request.method == 'POST':
        item_id = request.POST['menu_item_id']
        # description = request.POST['item_description']
        # price = request.POST['price']
        is_available = request.POST['is_available']
        item = get_object_or_404(MenuItem, id=item_id)
        # item.description = description
        # item.price = price
        item.is_available = is_available
        item.save()
        messages.error(request, 'Update successfully!')
    
    context = {
        'menu_items': MenuItem.objects.all(),
    }

    return render(request, 'update_menu.html', context)

def order_detail(request, emp_id, order_id):
    emp = Employee.objects.get(id=emp_id)
    if (emp.role not in ['waiter', 'manager']):
        return redirect('none_of_your_bussiness')
    if not emp.is_signed_in or request.session.session_key != emp.session_id:
        return redirect('none_of_your_bussiness')

    order = get_object_or_404(Order, id=order_id)
    order_items = order.order_items.all()
    order.get_total_cost()

    for item in order_items:
        if item.menu.is_available == False and item.status.name == 'waiting':
            item.status = get_object_or_404(Status, name='denied')
            item.save()
              
    if len(order_items) == 0:
        if order.is_paid == False:
            return redirect('add_order_item', emp.id, order.id)
        else:
            emp_order = Emp_Order.objects.all().filter(order=order)
            emp_order.delete()
            order.delete()
            order.customer.delete()
            return redirect('home_page', emp.id)

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'order_detail.html', context)

def view_item(request, emp_id):
    emp = get_object_or_404(Employee, id=emp_id)
    if (emp.role!='cook'):
        return redirect('none_of_your_bussiness')
    if not emp.is_signed_in or request.session.session_key != emp.session_id:
        return redirect('none_of_your_bussiness')
    
    status = [status for status in Status.objects.all() if status.id < 4]
    item_list = [item for item in OrderItem.objects.all() if item.status in status]

    if len(item_list) < 1:
        messages.error(request, 'There is no order at all')

    if request.method == 'POST':
        item_id = request.POST['item_id']
        new_status_id = request.POST['new_status_id']
        item = get_object_or_404(OrderItem, id=item_id)
        new_status = get_object_or_404(Status, id=new_status_id)

        if new_status.name == 'denied':
            item.menu.is_available = False
            item.menu.save()

        item.status = new_status
        item.save()
        return redirect('view_item', emp_id)

    context = {
        'item_list': item_list,
        'status': [status for status in Status.objects.all() if status.id < 6]
    }
    return render(request, 'item_list.html', context)

def add_order_item(request, emp_id, order_id):
    order = get_object_or_404(Order, id=order_id)
    emp = Employee.objects.get(id=emp_id)
    if (emp.role not in ['waiter', 'manager']):
        return redirect('none_of_your_bussiness')
    if not emp.is_signed_in or request.session.session_key != emp.session_id:
        return redirect('none_of_your_bussiness')

    if request.method == 'POST':
        menu_item_id = request.POST['menu_item_id']
        quantity = int(request.POST['quantity'])
        note = request.POST['note']
        menu_item = get_object_or_404(MenuItem, id=menu_item_id)
        status = get_object_or_404(Status, id=1)
        order_items = OrderItem.objects.create(order=order, menu=menu_item, quantity=quantity, note=note, status=status)
        order_items.get_subtotal_cost()
        order_items.save()
        return redirect('order_detail', emp.id, order.id)
    
    context = {
        'order': order,
        'menu_items': [item for item in MenuItem.objects.all() if item.is_available == True]
    }
    return render(request, 'add_order_item.html', context)

def update_item(request, emp_id, order_id, item_id):
    emp = Employee.objects.get(id=emp_id)
    order = get_object_or_404(Order, id=order_id)
    item = get_object_or_404(OrderItem, id=item_id)
    if (emp.role not in ['waiter', 'manager']):
        return redirect('none_of_your_bussiness')
    if not emp.is_signed_in or request.session.session_key != emp.session_id:
        return redirect('none_of_your_bussiness')
    
    if request.method == 'POST':
        new_item_id = request.POST['menu_item_id']
        new_note = request.POST['note']
        new_quantity = int(request.POST['quantity'])
        new_item = get_object_or_404(MenuItem, id=new_item_id)
        status = get_object_or_404(Status, id=1)
        if new_item.name == item.menu.name:
            item.note = new_note
            item.quantity = new_quantity
            item.get_subtotal_cost()
            item.save()
        else:
            order_item = OrderItem.objects.create(order=order, menu=new_item, quantity=new_quantity, note=new_note, status=status)
            order_item.get_subtotal_cost()
            order_item.save()
            item.delete()

        return redirect('order_detail', emp.id, order.id)

    context = {
        'this_item': item,
        'menu_items': MenuItem.objects.all()
    }
    return render(request, 'update_items.html', context)

def cancel(request, emp_id, order_id, item_id):
    emp = Employee.objects.get(id=emp_id)
    if (emp.role not in ['waiter', 'manager']):
        return redirect('none_of_your_bussiness')
    if not emp.is_signed_in or request.session.session_key != emp.session_id:
        return redirect('none_of_your_bussiness')
    
    order_item = get_object_or_404(OrderItem, id=item_id)
    order_item.delete()
    return redirect('order_detail', emp.id, order_id)

def complete_order(request, emp_id, order_id):
    emp = Employee.objects.get(id=emp_id)
    if (emp.role not in ['waiter', 'manager']):
        return redirect('none_of_your_bussiness')
    if not emp.is_signed_in or request.session.session_key != emp.session_id:
        return redirect('none_of_your_bussiness')

    order = get_object_or_404(Order, id=order_id)
    order_items = order.order_items.all()
    status = [status for status in Status.objects.all() if status.id < 4]
    for item in order_items:
        if item.status in status:
            if item.status.id < 2:
                item.delete()
            else:
                item.status = get_object_or_404(Status, name='stopped')
                item.save()
    table_number_id = order.table.id
    table_number = get_object_or_404(Table, id=table_number_id)
    order.is_paid = True
    order.save()
    table_number.is_using = False
    table_number.save()
    return redirect('order_detail', emp.id, order.id)