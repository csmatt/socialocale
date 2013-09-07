$(function(){
    //$('#subscribeBtn').click(function(){
    var subscribeForm = $('#subscribeForm');
    subscribeForm.ajaxForm();
    subscribeForm.keypress(function(e) {
        if (e.keyCode == 13) {
            // prevent enter key from submitting form
            e.preventDefault();
            return false;
        }
    });
    $('#subscribeBtn').click(function() {
        var emailInvalidErrorSpan = $('#emailInvalidError');
        subscribeForm.ajaxSubmit(function(response) {
            if (response.error) {
                emailInvalidErrorSpan.text(response.error);
            } else {
                emailInvalidErrorSpan.hide();
            }
        });
    });
    $('#subscribeEmail').watermark('Enter your email to subscribe')
});
