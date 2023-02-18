// menu accordian ui toggles
$('a.btn-light[href="#editFields"]').hover(function(){
    $('#editBanner').toggleClass('alert-dark').toggleClass('alert-light');
});
$('a.btn-light[href="#recipeFields"]').hover(function(){
    $('#recipeBanner').toggleClass('alert-dark').toggleClass('alert-light');
});
