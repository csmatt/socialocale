var UserModel = function(user) {
    var self = this;
    self.username = user.username;
    self.name = user.first_name + " " + user.last_name;
    if (user.profile) {
        // TODO: remove
        self.picture = '/media/' + user.profile.mugshot;
    }
    if (user.location) {
        self.location = {
            lat: user.location.lat,
            lon: user.location.lon
        };
    }
};