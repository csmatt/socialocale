socialocaleApp.service('MapService', function($rootScope, $http, MeService) {
    var self = this;
    self.map = undefined;
    self.markers = [];
    var markerClusterer,
        mapLoadedListener = null,
        mapIdleAfterChangeListener = null,
        placesAutocompleteService = null;

    self.broadcastMapLoaded = function() {
        google.maps.event.removeListener(mapLoadedListener);
        google.maps.event.addListener(self.map, 'idle', function() { console.log('map idle'); });
        $rootScope.$broadcast('map_loaded');
    };
    self.createMap = function() {
        self.map = new google.maps.Map(document.getElementById('map_canvas'), self.options());
        markerClusterer = new MarkerClusterer(self.map);
        placesAutocompleteService = new google.maps.places.PlacesService(self.map);
        google.maps.event.addListener(self.map, 'center_changed', self.onMapChange);
        google.maps.event.addListener(self.map, 'zoom_changed', self.onMapChange);
        mapLoadedListener = google.maps.event.addListener(self.map, 'tilesloaded', self.broadcastMapLoaded);
    };
    self.onMapChange = function() {
        if (!mapIdleAfterChangeListener) {
            mapIdleAfterChangeListener = google.maps.event.addListener(self.map, 'idle', function() {
                var mapAlertElem = $('#mapAlert');
                mapAlertElem.addClass('in');
                window.setTimeout(function() {
                    mapAlertElem.removeClass('in');
                }, 3000);
                google.maps.event.removeListener(mapIdleAfterChangeListener);
                mapIdleAfterChangeListener = null;
                $rootScope.$broadcast('map_changed');
            });
        }
    };
    self.setMapSettings = function() {
        var zoom = self.map.getZoom(),
            mapCenter = self.map.getCenter(),
            location = {
                lat: mapCenter.lat(),
                lon: mapCenter.lng()
            };

        MeService.setSettings({url:'/user/settings', params: jQuery.param({map_zoom:zoom,location:location})});
    };
    self.options = function() {
        var options = {
            zoom: 15,
            center: new google.maps.LatLng(parseFloat(0), parseFloat(0)),
            panControl: false,
            scrollwheel:false,
            mapTypeControl: false,
            streetViewControl: false,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            zoomControlOptions: {
                position: google.maps.ControlPosition.LEFT_CENTER
            }
        };

        if (MeService.location) {
            options['center'] = new google.maps.LatLng(parseFloat(MeService.location.lat), parseFloat(MeService.location.lon));
        }
        if (MeService.map_zoom) {
                options['zoom'] = MeService.map_zoom;
        }
        return options;
    };
    self.clearMarkers = function() {
        for ( var i = 0; i < self.markers.length; i++ ) {
            markerClusterer.removeMarker(self.markers[i]);
        }
        self.markers = [];
    };
    self.setMarkers = function() {
        var users = MeService.selectedInterest.users,
            locations = [], markerLocation, marker, i;
        self.clearMarkers();
        for ( i = 0; i < users.length; i++ ) {
            locations.push(users[i].location);
            markerLocation = new google.maps.LatLng(parseFloat(users[i].location.lat), parseFloat(users[i].location.lon));
            marker = new google.maps.Marker({position: markerLocation});
            markerClusterer.addMarker(marker);
            self.markers.push(marker);
        }
        return locations;
    };
    $rootScope.$on('me_loaded', self.createMap);
    $rootScope.$on('selected_interest_changed', self.setMarkers);
});

socialocaleApp.controller('MapCtrl', function($scope, SelectedInterestService, MapService) {
    $scope.setMapSettings = function() {
        MapService.setMapSettings();
        $('#mapAlert').removeClass('in');
    };
});
socialocaleApp.directive('locationAutocomplete', function() {
    return {
        restrict: 'E',
        template: '<div><input name="locationAutocomplete" type="text"/><input type="hidden" name="location"/></div>',
        replace: true,
        link: function(scope, element, attrs) {
            var locationAutocompleteField = angular.element('input[name=locationAutocomplete]', element),
                locationCoords = angular.element('input[name=location]', element),
                autocomplete = new google.maps.places.Autocomplete(locationAutocompleteField.get(0));
            google.maps.event.addListener(autocomplete, 'place_changed', function () {
                var locationGeometry = autocomplete.getPlace().geometry.location;
                locationCoords.val(locationGeometry.lat()+';'+locationGeometry.lng());
            });
        }
    }
});

