var HelpModel = function() {
    var self = this;
};

HelpModel.show = function() {
    hideAll();
    $(".bar > .helpDiv").show();
    $(".app > .helpDiv").show();
    $(".helpDiv").trigger('panelshow.help');
};

$(document).ready(function() {
    $("#showTutorialLink").click(TutorialModel.show);
});