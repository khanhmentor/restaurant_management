$(document).ready(function() {

    current_page = window.location.pathname.replaceAll('/', '').replace(/\d+/g, '');

    var pages = {

        /*Homepage*/

        '': function() {
            if (emp_role != 'cook')
                $('#update_menu').hide(),
                $('#view_item_list').hide()
            if ($.inArray(emp_role, ['waiter', 'manager']) < 0) 
                $('#new_order').hide(),
                $('#view_order').hide()
            $("#new_order").click(function(){
                window.location.href = window.location.pathname + 'order/';
            });
            $("#view_order").click(function(){
                window.location.href = window.location.pathname + 'view_order/';
            });
            $("#update_menu").click(function(){
                window.location.href = window.location.pathname + 'update_menu/';
            });
            $("#view_item_list").click(function(){
                window.location.href = window.location.pathname + 'item_list/';
            });
            $("#sign_out").click(function(){
                window.location.href = window.location.origin + '/' + emp_id + '/sign_out/';
            });
        },

        /*Order Detail*/

        'view_order': function() {
            var filter_enabled = false;

            if ($('#message').text().includes('There is no order at all'))
                $('#total-sum').hide()

            if (emp_role != 'manager')
                $('#filter-button').hide()

            $("#filter-button").click(function(){
                filter_enabled = !filter_enabled;
                if (filter_enabled) {
                $(this).text("Disable Filter");
                $('#label').show();    
                $("#order-time-input").show();
                } else {
                $(this).text("Enable Filter");
                $('#label').hide();    
                $("#order-time-input").hide();
                }
            });

            $("#order-time-input").change(function(){
                var input_time = $("#order-time-input").val();
                $(".order-time").each(function(){
                    var order_time = moment($(this).text(), 'MMMM DD, YYYY, h:mm a').tz('Asia/Ho_Chi_Minh').format('YYYY-MM-DD');
                    
                    if (order_time == input_time) {
                        $(this).parent().parent().show();
                    } else {
                        $(this).parent().parent().hide();
                    }
                });
            });

            $(".button").click(function(){
                id = $(this).attr('id');
                window.location.href = window.location.pathname.replace('view_order', 'order/' + id);
            });
        },
        // '': function() {

        // },
        // '': function() {

        // },
        // '': function() {

        // },
        // '': function() {

        // },

        /*Customer*/

        'customer': function() {
            function checkWidth() {
                if ($('.sidebar').length < 1) {
                    $('.main-content').css('grid-column', '3 / 9');
                    $('.main-content').css('padding', '0');
                    $('.main-content').css('padding-top', '20px');
                    if (screen.width <= 719) {
                        $('.main-content').css('grid-column', '1 / 12');
                    }
                    else if (screen.width >= 720 && screen.width <= 1366) {
                        $('.main-content').css('grid-column', '2 / 10');
                    }
                }
            }
        
            checkWidth()
        
            $(window).resize(function() {
                checkWidth();
            });
        
            window.onload = function() {
                $('#' + current_type_id).addClass('active');
            }
        
            $('.dishes-container').click(function() {
                id = $(this).attr('id');
                $('.navbar, .grid-container').addClass('blur');
                $('.navbar').css('margin-top', '-10px');
                $('.overlay').show();
                $('#' + id).appendTo($('.modal .modal-content'));
                if (current_page != 'cart')
                    $('.quantity-field').text(1),
                    $('.modal textarea').val('');
                else
                    $('.quantity-field').text($(this).attr('data-quantity'));
                    $('.modal textarea').val($(this).attr('data-note'));
                $('.modal').show();
            });
        
            $('.overlay').click(function() {
                $('.navbar, .grid-container').removeClass('blur')
                $('.navbar').css('margin-top', '0');
                $('.overlay').hide();
                id = $('.modal .modal-content .dishes-container').attr('id');
                if (current_page == 'cart')
                    $('#' + id).appendTo($('#i-' + id));
                else
                    $('#' + id).appendTo($('.main-content'));
                $('.button').removeClass('move-right');
                $('.modal').hide();
            });
        
            $('.add').click(function() {
                $('.quantity-field').text(parseInt($('.quantity-field').text()) + 1);
            });
        
            $('.minus').click(function() {
                if ($('.quantity-field').text() > 1)
                    $('.quantity-field').text(parseInt($('.quantity-field').text()) - 1);
            });
        
            $('.modal .button').click(function(e) {
                e.preventDefault();
                id = $('.modal .modal-content .dishes-container').attr('id');
                $('#item-id').val(id);
                $('#quantity').val($('.quantity-field').text());
                $('#note').val($('.modal textarea').val());
                $(this).addClass('move-right');
                setTimeout(function() {
                    $('.modal form').submit();
                }, 1000);
            });
                
            $('.menu-button').click(function() {
                id = $(this).attr('id');
                window.location.href = window.location.origin + '/menu/' + id + '/' + order_id;
            });
        
            $('#' + current_page).addClass('active');
            $('.navbar a').click(function() {
                $('.navbar a').removeClass('active');
                $(this).addClass('active');
                id = $(this).attr('id');
                if (id == 'menu')
                    window.location.href = window.location.origin + '/menu/0/' + order_id;  
                else 
                    window.location.href = window.location.origin + '/' + id + '/' + order_id;
            });
        
            const images = $(".image-gallery img");
            const dots = $(".dots span");
        
            let activeIndex = 0;
            images.eq(activeIndex).addClass("active-img");
            dots.eq(activeIndex).addClass("active-dot");
        
            dots.click(function() {
                images.eq(activeIndex).removeClass("active-img");
                dots.eq(activeIndex).removeClass("active-dot");
                activeIndex = $(this).index();
                images.eq(activeIndex).addClass("active-img");
                dots.eq(activeIndex).addClass("active-dot");
            });
        
            $(document).on('mousemove', function(event) {
                if (event.pageX < 20) {
                  $('.sidebar').addClass('show-sidebar');
                } else {
                    $('.sidebar').on('mouseleave', function() {
                        $('.sidebar').removeClass('show-sidebar');
                    });  
                }
            });
        
            if ($('.info .data .sub-field').length > 0) {
        
                var total = 0;
                var allChecked = true;
        
                $('.info .data .sub-field').each(function() {
                    total += parseFloat($(this).text());
                });
        
                $('.payment-field h1 span').text(total.toFixed(2));
        
                $('.main-content .button').click(function() {
                    $('.check-box input').each(function() {
                        if (!$(this).prop('checked')) {
                          allChecked = false;
                          return false;
                        }
                    });
                    if (allChecked)
                        $(this).addClass('move-right'),
                        setTimeout(function() {
                            $('.main-content form').submit();
                        }, 1000);
                    else
                        allChecked = true,
                        alert('There might be some items having not been double checked!');
                });
            }
        
            if (current_page == 'cart')
                if ($('.payment-field h1 span').text() == '')
                    $('.payment-field h1').text("You don't have any item!"),
                    $('.main-content .button').text('Order some?'),
                    $('.main-content .button').click(function() {
                        $(this).addClass('move-right'),
                        setTimeout(function() {
                            window.location.href = window.location.origin + '/menu/0/' + order_id;  
                        }, 1000);
                    });
        },
    };

    if (pages[current_page]) 
        pages[current_page]();
    else 
        pages['customer']();
});     
