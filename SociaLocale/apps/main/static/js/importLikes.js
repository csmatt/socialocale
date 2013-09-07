var LikesImportModel = function() {
    var self = this,
    i;
    self.selectedToImport = ko.observableArray([]);
    self.allLikes = ko.observableArray([]);

    // show the interest panel initially
    InterestModel.show();

    // retrieve user's likes
    self.loadLikes = function(){
        FB.api('/me/likes',
			  function(data) {
		      if (data && data.likes) {
			  self.allLikes(data.likes.data);
		      }
		  });
    };
    /* Adds if the like isn't in self.selectedToImport and removes otherwise */
    self.addToSelected = function(like, event) {
	var removedImport = self.selectedToImport.remove(like);
	if (removedImport.length <= 0) {
	    self.selectedToImport.push(like);
	    slm.addInterestToUi(like.name, like.id, FB_GRAPH_URL + like.id + '/picture');
	} else {
	    slm.removeInterestFromUiById(like.id);
	}
    };
    self.selectAllToImport = function() {
	var allLikes = self.allLikes();
	for (i = 0; i < allLikes.length; i++) {
	    self.addToSelected(allLikes[i]);
	}
    };
    self.removeAllSelectedToImport = function() {
	var removedLikes = self.selectedToImport.removeAll();
	self.removeAllSelectedToImportFromInterestList(removedLikes);
    };
    self.removeAllSelectedToImportFromInterestList = function(likes) {
	likes = likes || self.selectedToImport();
	for (i = 0; i < likes.length; i++) {
	    slm.removeInterestFromUiById(likes[i].id);
	}
    };
    self.close = function() {
	$("#importLikes").hide();
    };

    self.doImportLikes = function() {
	self.removeAllSelectedToImportFromInterestList();
	var selectedToImport = self.selectedToImport();
	for(i = 0; i < selectedToImport.length; i++) {
	    slm.persistNewInterest(selectedToImport[i].id, selectedToImport[i].name);
	}
	self.close(); // must come at end so that we persist first
    };

    /* Styles & Events */
    $("#importLikesCloseBtn").button({icons: {primary: "ui-icon-closethick"}, text: false}).click(self.close);
    $("#importLikesBtn").button().click(self.doImportLikes);
    $("#likesSelectAllBtn").button().click(self.selectAllToImport);
    $("#likesSelectNoneBtn").button().click(self.removeAllSelectedToImport);
}; 
var lim = null;
$(document).ready(function() {
    lim = new LikesImportModel();
    ko.applyBindings(lim, $("div#importLikes").get(0));
});

LikesImportModel.show = function() {
    $("#importLikes").show();
    lim.loadLikes();
};