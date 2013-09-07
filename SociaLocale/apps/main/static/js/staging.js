var Staging = function() {
    var self = this;
};
var writeMessageDialog = $("<div id='writeMessageDialog' title='New Message'><form action='/messages/compose/' method='post' id='compose_message_form'><p><input type='text' name='to'><textarea name='body'></textarea><input type='submit' name='send' value='Send'></p></div>");
Staging.showUMessages = function() {
    $.getJSON("/user/umessages/", {}, function(messages){
        var i = 0, msg;
        slm.me.messages.removeAll();
        if ( messages ) {
            for ( i = 0; i < messages.length; i++) {
                msg = {
                    broadcast_id: messages[i].pk,
                    content: messages[i].fields.body,
                    author: messages[i].fields.sender,
                    created: messages[i].fields.sent_at
                };
                slm.me.messages.push(new BroadcastModel(msg));
            }
        }
        BroadcastModel.show();
        $("#broadcastsForInterest").toggle();
        $("#umessages").toggle();
    });
    if ($('#writeMessageDialog', $('body')).length == 0) {
        writeMessageDialog.appendTo($('body'));
        writeMessageDialog.dialog();
        $('#compose_message_form', writeMessageDialog).submit(function(){
            $.post($(this).attr('action'), $(this).serialize(), function(response){
                // do something here on success
            },'json');
            writeMessageDialog.dialog('close');
            return false;
        });
    }
};

$(".user_count").click(function() {
    console.log('appended alert');
    var alert = $("<alert type='success' ui-animate='ui-hide' style='position: absolute; top: 0; z-index: 2000; left:50%;'>alert text here</alert>");
    alert.appendTo('body');
});
