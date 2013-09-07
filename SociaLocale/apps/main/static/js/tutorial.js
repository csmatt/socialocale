var TutorialModel = function() {
    var self = this,
        locationAutocomplete = $(".interestsDiv > input[name='locationAutocomplete']");

    self.tips = ko.observableArray([]);
    self.heading = ko.observable();
    self.instructions = ko.observable();
    self.enabled = ko.observable(false);

    // init
    self.startTutorial = function() {
        $("#broadcastsBtn").button("disable");
        self.tutorialNavigationHelper(0);
    };
    self.stepOne = function() {
        self.enabled(true);
        InterestModel.show();
        SettingsModel.editLocation();
        slm.settingsModel.editLocation();
        self.heading("First time using SociaLocale?");
        self.instructions("To get started, enter your street address, city, and state in the box to the right.");
    };
    self.stepTwo = function() {
        self.fxnCntr = self._onLocationChangeFxnIndex;
        self.heading("Great! What are your interests?");
        self.instructions("Add an interest by typing in the box to the right and selecting from the list that appears.");
        self.setTips(["Just add one interest for now. At the end of the tutorial, you an import from your Facebook likes."]);
    };
    /**
     * Triggered by selectedInterest changing
     * @param newValue - the new selectedInterest
     */
    self.stepThree = function(newValue) {
        self.fxnCntr = self._onSelectedInterestChangeFxnIndex;
        var newValueName = "your interests.",
            closeBtn,
            importBtn;
        if (newValue) {
            newValueName = newValue.name;
        }
        if (selectedInterestSubscription) {
            selectedInterestSubscription.dispose();
        }
        BroadcastModel.show();
        $("#broadcastsBtn").button("enable");
        self.heading("Awesome! Last step...");
        self.instructions("Broadcast to those around you to let them know you're serious about " + newValueName);
        self.setTips(["To search for more users, use the zoom bar on the left to zoom out.","Click and drag the map to look for more users."]);
        closeBtn = $("<span class='uniqueToPane whiteText' style='text-align: center; font-size: 1.5em; text-decoration: underline;cursor:pointer;'>close</span>");
        importBtn = $("<span class='uniqueToPane whiteText' style='text-align: center; font-size: 1.5em; text-decoration: underline;cursor:pointer;'>import from Facebook</span>");
        if ( slm.me.user_id !== -1 ) {
            importBtn.appendTo("#newUserTutorialExtraButtons");
            importBtn.click(self.closeAndImport);
        }
        closeBtn.click(self.close);
        closeBtn.appendTo("#newUserTutorialExtraButtons");
    };

    self.setTips = function(tips) {
        self.tips.removeAll();
        self.tips(tips);
    };
    self.close = function() {
        self.fxnCntr = 0; // reset fxnCntr
        $("#newUserTutorial").hide();
        locationAutocomplete.off(); // just in case the user never got that far
        $("#broadcastsBtn").button("enable"); // just in case the user never got that far
        if (selectedInterestSubscription) {
            selectedInterestSubscription.dispose();
        }
        self.enabled(false);
    };
    self.closeAndImport = function() {
        self.close();
        LikesImportModel.show();
    };
    self.fxns = [self.stepOne, self.stepTwo, self.stepThree];
    self._onLocationChangeFxnIndex = 1;
    self._onSelectedInterestChangeFxnIndex = 2;
    self.fxnCntr = 0;
    self.tutorialNavigationHelper = function(delta) {
        var forwardBtn = $("#tutorialNavigationForwardBtn"),
            backBtn = $("#tutorialNavigationBackBtn");
        self.fxnCntr += delta;
        self.tips.removeAll();
        $(".uniqueToPane").remove();
        forwardBtn.button("option", "disabled", (self.fxnCntr === self.fxns.length - 1));
        backBtn.button("option", "disabled", (self.fxnCntr === 0));
        self.fxns[self.fxnCntr]();
    };
    self.prevTutorialPane = function() {
        self.tutorialNavigationHelper(-1);
    };
    self.nextTutorialPane = function() {
        self.tutorialNavigationHelper(1);
    };
    /* Events */
    locationAutocomplete.one('settings.location', self.fxns[self._onLocationChangeFxnIndex]);
    var selectedInterestSubscription = slm.selectedInterest.subscribe(self.fxns[self._onSelectedInterestChangeFxnIndex]);

    /* Styles */
    $("#newUserTutorialCloseBtn").button({icons: {primary: "ui-icon-closethick"}, text: false}).click(self.close);
    $("#tutorialNavigationBackBtn").button({icons: {primary: "ui-icon ui-icon-circle-arrow-w"}, text: true, disabled: true}).click(self.prevTutorialPane);
    $("#tutorialNavigationForwardBtn").button({icons: {primary: "ui-icon ui-icon-circle-arrow-e"}, text: true}).click(self.nextTutorialPane);
};
var tutModel = null;
$(document).ready(function() {
    $(window).bind('slm.initialized', function() {
        if (slm.isNewUser) {
            TutorialModel.show();
        }
    });
});
TutorialModel.show = function() {
    if (!tutModel) {
        tutModel = new TutorialModel();
        ko.applyBindings(tutModel, $("div#newUserTutorial").get(0));
    }
    $("#newUserTutorial").show();
    tutModel.startTutorial();
};