var SettingsModel = function (settings) {
    var self = this,
        locationAutocomplete = $(".interestsDiv > input[name='locationAutocomplete']");/*,
        autocomplete = new google.maps.places.Autocomplete(locationAutocomplete.get(0));*/

    self.location = ko.observable(settings.location);
    self.city = ko.observable(settings.city);
    self.publish_to_fb = ko.observable(settings.publish_to_fb);
    self.editingLocation = ko.observable(false);
    self.editLocation = function() { self.editingLocation(true); };
    /*google.maps.event.addListener(autocomplete, 'place_changed', function () {
        var place = autocomplete.getPlace(),
            locationGeometry = place.geometry.location,
            location = {
                lat:locationGeometry.lat(),
                lng:locationGeometry.lng()
            };
        self.setLocation(place.formatted_address, location);
    });*/
    self.setLocation = function(city, location) {
        if (location && location.lat && location.lng) {
            $.ajax({
            type:'POST',
            url:"/user/settings",
            data:{
                location:JSON.stringify(location),
                city:city
            },
            success:function (result) {
                location.lon = location.lng;//fix this to be consistent at some point
                self.location(location);
                self.city(city);
		    SettingsModel.closeEditLocation();
		    locationAutocomplete.trigger('settings.location');
		}
            });
	}
    };

    // Events
    self.changeValue = function() {
	var newValue = !self.publish_to_fb();
	self.publish_to_fb(newValue);
	$.post("/user/settings", {publish_to_fb:newValue});
	console.log(self.publish_to_fb());
	return true;
    };
};
SettingsModel.closeEditLocation = function() {
    $(".interestsDiv > span[name='locationLabel']").show();
    $(".interestsDiv > input[name='locationAutocomplete']").hide();
};
SettingsModel.editLocation = function () {
    $(".interestsDiv > span[name='locationLabel']").hide();
    $(".interestsDiv > input[name='locationAutocomplete']").show();
};
SettingsModel.onSettingsBtnClick = function(event) {
    SettingsModel.show();
};
SettingsModel.show = function () {
    hideAll();
    $(".bar > .settingsDiv").show();
    $(".app > .settingsDiv").show();
    $(".settingsDiv").trigger('panelshow.settings');
};
