socialocaleApp.service('MessageService', function($http, $rootScope, $dialog, MeService) {
    var self = this;
    self.messages = [];
    self.currentConversation = {};
    self.get = function() {
        $http.get('/messages/').success(function(messages){
            self.messages = messages;
        });
    };
    self.getOtherUser = function(message) {
        if (message.from_user.username != MeService.userDetails.user.username) {
            return message.from_user;
        } else {
            return message.to_user;
        }
    };
    self.send = function(body, message, to) {
        if (message && !to) {
            to = self.getOtherUser(message).username;
        }
        $http.post('/messages/compose/', jQuery.param({to: to, body: body})).success(function() {
            self.get();
        });
    };
    self.showMessagesModal = function() {
        var dialog = $dialog.dialog();
        dialog.open('/static/partials/messages.html', 'MessageCtrl');
    };
    self.showConversationModal = function(message) {
        var other_user_id = self.getOtherUser(message).id;
        $http.get('/messages/between?other_user_id='+other_user_id).success(function(data){
            self.currentConversation = {
                latestMessage: message,
                messages: data
            };
            var dialog = $dialog.dialog();
            dialog.open('/static/partials/messageConversation.html', 'MessageConversationCtrl').then(function(){
                self.currentConversation = {};
            });
        });
    };
    $rootScope.$on('me_loaded', self.get);
});
socialocaleApp.controller('MessageConversationCtrl', function($scope, dialog, MessageService) {
    $scope.messages = function() {
        return MessageService.currentConversation.messages;
    };
    $scope.send = function(body) {
        var message = MessageService.messages[0];
        MessageService.send(body, message);
        $scope.flags.reply = false;
    };
    $scope.otherUser = function(message) {
        if (message) { // workaround since function calls as scope properties will cause a watch to try to run this method when the dialogs are closed
            return MessageService.getOtherUser(MessageService.currentConversation.latestMessage).username;
        }
    };
    $scope.close = function() {
        dialog.close('cancel');
    };
});
socialocaleApp.controller('MessageCtrl', function($scope, dialog, MessageService) {
    $scope.messages = function() {
        return MessageService.messages;
    };
    $scope.replyBody = "";
    $scope.send = function(body, message, to) {
        MessageService.send(body, message, to);
        if (message) {
            $scope.flags.reply = false;
        } else {
            $scope.flags.compose = false;
        }
    };
    $scope.viewConversation = MessageService.showConversationModal;
    $scope.close = function() {
        dialog.close('cancel');
    };
});