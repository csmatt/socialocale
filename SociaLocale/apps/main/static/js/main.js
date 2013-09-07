if (typeof console == "undefined") var console = { log: function() {} };

var socialocaleApp = angular.module('socialocaleApp', ['ui','ui.bootstrap']).
    config(['$httpProvider', function($httpProvider){
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
        $httpProvider.defaults.headers.post['X-CSRFToken'] = getCookie('csrftoken');
        var numLoadings = 0;
        var loadingScreen = angular.element('#loadingOverlay')
            .appendTo(angular.element('body')).hide();
        $httpProvider.responseInterceptors.push(function() {
            return function(promise) {
                numLoadings++;
                loadingScreen.show();
                var hide = function(r) { if (!(--numLoadings)) loadingScreen.hide(); return r; };
                return promise.then(hide, hide);
            };
        });
    }]);
socialocaleApp.run(function(MeService, SelectedInterestService, InterestService, MessageService, MapService) {
    MeService.get();
});

$(document).ready(function () {
    $("#controlPanelToggleClickableArea").click(function() {
        $('#controlPanel').animate({height: 'toggle'});
        $(this).toggleClass("ui-icon-arrowthickstop-1-s ui-icon-arrowthickstop-1-n");
    });
});
