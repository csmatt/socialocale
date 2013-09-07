var LoginModel = function() {
    var self = this;
    self.loginTypes = ko.observableArray([
        {
            siteName: "Facebook",
            imageUrl: "/static/images/social_login/facebook_normal.png",
            href: "/login/facebook"
        },
        {
            siteName: "Twitter",
            imageUrl: "/static/images/social_login/twitter_normal.png",
            href: "/login/twitter"
        },
        {
            siteName: "Google",
            imageUrl: "/static/images/social_login/googleplus_normal.png",
            href: "/login/google-oauth2"
        },
        {
            siteName: "LinkedIn",
            imageUrl: "/static/images/social_login/linkedin_normal.png",
            href: "/login/linkedin"
        }
    ]);
    self.onButtonClick = function(loginType) {
        window.location.href = loginType.href;
    };
};
var loginModel = null;
$(document).ready(function() {
    $(window).bind('slm.initialized', function() {
        if (slm.me.user_id === -1) {
            $("#loginBtn").button({label: 'Login'}).click(LoginModel.show);
        } else {
            $("#loginBtn").button({label: 'Sign out'}).click(LoginModel.logOff);
        }
        loginModel = new LoginModel();
        ko.applyBindings(loginModel, $("div#loginOptions").get(0));
    });
});
LoginModel.show = function() {
    $("div#loginDialog").dialog();
    $("div#loginDialog").show();
};
LoginModel.logOff = function() {
    window.location.href = '/logout';
};