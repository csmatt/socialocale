socialocaleApp.service('SelectedInterestService', function($rootScope, $http, MeService, MapService) {
    var self = this;
    self.users = [];
    self.selectedInterest = function() {
        return MeService.selectedInterest;
    };
    self.prepareInterestQuery = function() {
        var mapCenter = MapService.map.getCenter(),
            mapBounds = MapService.map.getBounds(),
            requestData = {
                neMapBounds: mapBounds.getNorthEast().toUrlValue(),
                swMapBounds: mapBounds.getSouthWest().toUrlValue(),
                mapCenterLat: mapCenter.lat(),
                mapCenterLon: mapCenter.lng()
            };
        return requestData;
    };
    self.get = function() {
        var requestData = self.prepareInterestQuery();
        $http.get('/interests/selected?' + jQuery.param(requestData)).success(function(data){
            MeService.selectedInterest = data;
            $rootScope.$broadcast('selected_interest_changed');
        });
    };
    self.set = function(interest) {
        var requestData = {interest: interest};
        $http.post('/interests/selected', jQuery.param(requestData)).success(self.get);
    };
    $rootScope.$on('map_changed');
});
socialocaleApp.service('InterestService', function($rootScope, $http, SelectedInterestService) {
    var self = this;
    self.interests = [];
    self.get = function() {
        $http.get('/interests').success(function(interests){
            SelectedInterestService.get();
            self.interests = interests;
        });
    };
    self.add = function(interest) {
        var requestData = SelectedInterestService.prepareInterestQuery();
        requestData['interest_id'] = interest.interest_id;
        requestData['interest_name'] = interest.interest_name;
        $http.post('/interests/add', jQuery.param(requestData)).success(self.get);
    };
    self.delete = function(interest) {
        $http.post('/interests/delete', 'id='+interest.id).success(self.get);
    };
    $rootScope.$on('map_loaded', self.get);
});

socialocaleApp.controller('InterestCtrl', function($scope, InterestService, SelectedInterestService) {
    $scope.interests = function() {
        return InterestService.interests;
    };
    $scope.firstVisibleIndex = 0;
    $scope.visible = 3;
    $scope.lastIndex = function() {return $scope.interests().length - 1;};
    $scope.lastVisibleIndex = function() {
        var newLastVisibleIndex = $scope.firstVisibleIndex + $scope.visible;
        if (newLastVisibleIndex > $scope.lastIndex()) {
            newLastVisibleIndex = $scope.lastIndex();
        }
        return newLastVisibleIndex;
    };
    $scope.prev = function() {
        var newIndex = $scope.firstVisibleIndex - $scope.visible;
        if (newIndex >= 0) {
            $scope.firstVisibleIndex = newIndex;
        } else {
            $scope.firstVisibleIndex = $scope.lastIndex();
        }
    };
    $scope.next = function() {
        var newIndex = $scope.firstVisibleIndex + $scope.visible;

        if (newIndex <= $scope.lastIndex()) {
            $scope.firstVisibleIndex = newIndex;
        } else if (newIndex + $scope.visible >= $scope.lastIndex()) {
            // wrap by setting the current index to 0
            $scope.firstVisibleIndex = 0;
        }
    };
    $scope.isVisible = function(index) {
        //return (index >= $scope.firstVisibleIndex && (index < ($scope.firstVisibleIndex + $scope.visible) || (index <= $scope.firstVisibleIndex - $scope.visible)));
        return (index >= $scope.firstVisibleIndex && index < $scope.lastVisibleIndex());
    };
    $scope.delete = InterestService.delete;
    $scope.selectedInterest = SelectedInterestService.selectedInterest;
    $scope.setSelectedInterest = SelectedInterestService.set;
    // scrolls to the selected interest
    $scope.$watch('interests()', function(interests){
        var selectedInterest = $scope.selectedInterest();
        for(var i = 0; i < interests.length; i++) {
            if (interests[i].id === selectedInterest.id) {
                if (interests.length - i < $scope.visible) {
                    $scope.crntIndex = interests.length - $scope.visible;
                } else {
                    $scope.crntIndex = i;
                }
                return;
            }
        }
    });
});

socialocaleApp.controller('InterestAutoCompleteCtrl', function($scope, $http, SelectedInterestService, InterestService) {
    var addInterest = function (event, ui) {
        var interest_name = ui.item.value,
            interest_id = ui.item.id;
        InterestService.add({
            interest_id: interest_id,
            interest_name: interest_name
        });
    };
    $("#addInterestTextBox").watermark("Type an interest here");
    $('#addInterestTextBox').autocomplete({
        minLength: 2,
        html: true,
        select: addInterest,
        source: function (request, response) {
            $.ajax({
                url: getFbUrl("search"),
                dataType: "jsonp",
                data: {
                    q: request.term,
                    type: 'page'
                },
                error: function () {
                    console.log($.makeArray(arguments));
                },
                success: function (data) {
                    response($.map(data.data, function (item) {
                        var labelImage = $("<img class='autocomplete_interest_image'/>").attr('src', getFbInterestPictureUrl(item.id)).attr('title', item.name),
                            labelSpan = $("<span class='autocomplete_interest_text'/>").text(item.name),
                            label = labelImage.after(labelSpan),
                            resp = {
                                value: item.name,
                                label: label,
                                id: item.id
                            };
                        return resp;
                    }));
                }
            });
        },
        open: function () {
            var uiAutocomplete = $('.ui-autocomplete');
            uiAutocomplete.css('height', '250');
            uiAutocomplete.css('width', '190');
            uiAutocomplete.css('overflow-y', 'scroll');
        },
        close: function () {
            $('#addInterestTextBox').val('');
        }
    });
});
/*socialocaleApp.directive('carousel', function($timeout) {
    return {
        restrict: 'A',
        scope: true,
        template: "<ul><li ng-repeat='visibleItem in visibleItems'></li></ul>",
        link: function(scope, element, attrs, controller) {
            var options = scope.$eval(attrs.options), // visible, moveby, prevSelector, nextSelector
                lis = angular.element('li', element),
                prevBtn = angular.element(options.prev),
                nextBtn = angular.element(options.next);
            nextBtn.click(function() {
                if (scope.crntIndex < lis.length) {
                    if ((scope.crntIndex + options.moveby) < lis.length) {
                        scope.crntIndex += 1;
                        scope.visibleItems = scope.items.slice(scope.crntIndex, scope.crntIndex + options.moveby);
                    }
                }
            });
            scope.crntIndex = 0;

            scope.$watch(scope.interests, function(interests) {
                if (interests.length !== 0) {
                    var interestsUl = angular.element('#interests');
                    if (!scope.jcarouselInitialized) {
                        interestsUl.jcarousel({itemFallbackDimension:310, size: interests.length, wrap:'both', visible:3});
                        scope.jcarouselInitialized = true;
                    } else {
                        $timeout(function(){
                            interestsUl.jcarousel('reload');
                        }, 500);
                    }
                }
            });
        }
    };
});*/