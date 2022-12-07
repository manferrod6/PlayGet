var temp_button_text;

function CustomFormSubmitPost(e){
    var el = $(e);
    temp_button_text = el.text()
    el.attr('disabled', 'disabled').text("").append('<class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>Cargando...');
};

function CustomFormSubmitResponse(e){
    var el = $(e);
    el.removeAttr('disabled').text(temp_button_text);
};

$("#saved-cards tr").click(function(){
   $(this).addClass('selected').siblings().removeClass('selected');    
   var value=$(this).find('td:first').html();
   $('#use-card').removeAttr("disabled")    
});

$('.ok').on('click', function(e){
    alert($("saved-cards tr.selected td:first").html());
});

function payWithSavedCard(){
    CustomFormSubmitPost($('#use-card'));
    $.ajax({
        method: "POST",
        url: "/payment",
        data: {
            currency: "gbp",
            card_id: $("#saved-cards tr.selected td:first").html() ,
        },
        success: function(json){
            
            if (json["result"] == "okay") {
              alert("Your payment was a success");
              window.location.assign("/account")
            }
            else{
              CustomFormSubmitResponse($('#use-card'));
              alert(json["message"]); 
            }
        },
        error: function(xhr){
            CustomFormSubmitResponse($('#use-card'));
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });

}



jQuery(document).ready(function() {     
    FormControls.init();
});

$(function() {
    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
})