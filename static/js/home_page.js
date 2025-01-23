function add_select_class(el){
    $('.selected').removeClass('selected');
    el.addClass('selected');
}


function submit_ofer_select(){
    var forma = $('.right_section');
    var сountry_select = $('#сountry_select');
    var city_select = $('#city_select');
    var offer = forma.find('.selected');
    var submit_btn = $('.form_submit_button');
    if(offer.is('DIV')){
        var сountry = сountry_select.val();
        var city = city_select.val();
        var offer_name = offer.find('.offer_block_title').text();
        location.href='/customers/services/?сountry='+ сountry + '&city=' + city + '&offer_name=' + offer_name;
    }
}


function select_map(select){
    var value = select.find('option:selected').attr('map_value');
    if (value) {
        var coordinates = value.split(',');
        var lat = parseFloat(coordinates[0]);
        var lng = parseFloat(coordinates[1]);
        updateMarker(lat, lng);
     }   
}