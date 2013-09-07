var BroadcastModel = function(data) {
    var self = this;
    self.id = data.broadcast_id;
    self.coords = [data.latitude, data.longitude];
    self.author = data.author;
    self.content = data.content;
    self.created = data.created;
    self.authorNameAndTime = ko.computed(function() {
        return self.author.name + " - " + self.created;
    });
    self.data = ko.computed(function() {
        return self.author.name + ": " + self.content;
    });
};
BroadcastModel.show = function() {
    hideAll();
    $(".bar > .broadcastsDiv").show();
    $(".app > .broadcastsDiv").show();
    $(".broadcastsDiv").trigger('panelshow.broadcasts');
};