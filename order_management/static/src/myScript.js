$(document).ready(function() {
    current_page = window.location.pathname.replaceAll('/', '')
    if (current_page.indexOf("menu") >= 0) {
        current_page = current_page.slice(0, 4)
        window.onload = function() {
            $('#' + current_type_id).addClass('active')
            // if (menu_items.split(', ').length > 10)
            //     $('.main-content').css('height', '140vh')
        }
        $('.tasty-dishes').click(function() {
            id = $(this).attr('src')
        });
        $('.menu-button').click(function() {
            id = $(this).attr('id')
            window.location.href = window.location.origin + '/menu/' + id
        });
    }
    $('#' + current_page).addClass('active')
    $('.navbar a').click(function() {
        $('.navbar a').removeClass('active');
        $(this).addClass('active');
        id = $(this).attr('id')
        if (id == 'menu')
            window.location.href = window.location.origin + '/menu/0'
        else 
            window.location.href = window.location.origin + '/' + id
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
});