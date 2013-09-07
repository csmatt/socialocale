var FB_GRAPH_URL = "https://graph.facebook.com/",
getFbUrl = function(uriComponent) {
    return FB_GRAPH_URL + encodeURIComponent(uriComponent);
},
getFbInterestPictureUrl = function(interest_id) {
  return getFbUrl(interest_id) + '/picture'
};
//$('html').ajaxSend(function(event, xhr, settings) {
//    function csrfSafeMethod(method) {
//	// these HTTP methods do not require CSRF protection
//	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
//    }
//    function getCookie(name) {
//        var cookieValue = null;
//        if (document.cookie && document.cookie != '') {
//            var cookies = document.cookie.split(';');
//            for (var i = 0; i < cookies.length; i++) {
//                var cookie = jQuery.trim(cookies[i]);
//                // Does this cookie string begin with the name we want?
//                if (cookie.substring(0, name.length + 1) == (name + '=')) {
//                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                    break;
//                }
//            }
//        }
//        return cookieValue;
//    }
//    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))
//	&& !csrfSafeMethod(settings.type)) {
//        // Only send the token to relative URLs i.e. locally.
//	var cookie = getCookie('c');
//        xhr.setRequestHeader("X-CSRFToken", cookie);
//	settings.data += "&_csrf_token=" + cookie;
//    }
//});
// modify jquery ajax to add csrtoken when doing "local" requests

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
$('html').ajaxSend(function(event, xhr, settings) {
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
