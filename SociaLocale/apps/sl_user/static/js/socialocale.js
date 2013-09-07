socialocaleApp.service('MeService', function($rootScope, $http, $dialog) {
    var self = this;

    self.sync = function(data) {
        self.userDetails = data;
        self.username = data.user.username;
        self.name = data.user.first_name + ' ' + data.user.last_name;
        self.email = data.user.email;
        self.picture = '/media/' + data.mugshot;
        self.selectedInterest = data.selectedInterest;
        self.location = data.location;
        self.city = data.city;
        self.map_zoom = data.settings.map_zoom;
        self.userDetails.picture = self.picture;
    };
    self.get = function() {
        $http.get('/user/details').success(function(data){
            if (data.isNewUser) {
                self.showEditProfileModal();
            } else {
                self.sync(data);
                $rootScope.$broadcast('me_loaded');
            }
        });
    };
    self.setSettings = function(settings) {
        $http.post(settings.url, settings.params);
    };
    self.showEditProfileModal = function(){
        var dialog = $dialog.dialog({resolve: {userDetails: function() { return self.userDetails; }}});
        dialog.open('/static/partials/editProfileModal.html', 'EditProfileCtrl');
        dialog.modalEl.keypress(function(e) {
            if (e.keyCode == 13) {
                // prevent enter key from submitting form
                e.preventDefault();
            }
        });
    };
});
socialocaleApp.controller('MainCtrl', function($scope, MessageService) {
    $scope.showMessagesModal = MessageService.showMessagesModal;
});
socialocaleApp.directive('fileupload', function() {
    return {
        restrict: 'E',
        scope: {
            imgSrc:'@',
            uploadName:'@'
        },
        template: '<div class="imageUpload"><img style="height: 200px; width: 200px;" name="imagePreview" ng-src="{{imgSrc}}"><br/><input type="file" name="{{uploadName}}"/></div>',
        link: function(scope, element, attrs, controller) {
            var fileUploadInput = angular.element('input[type=file]', element),
                imagePreview = angular.element('img[name="imagePreview"]', element),
                changePreviewImage = function(data) {
                    var reader = new window.FileReader(),
                        fileToUpload;
                    reader.onload = function (oFREvent) {
                        imagePreview.attr('src', oFREvent.target.result );
                    };
                    fileToUpload = data.files[0];
                    reader.readAsDataURL(fileToUpload);
                };
            fileUploadInput.change(function() {
                changePreviewImage(this);
            });
        }
    }
});

socialocaleApp.directive('autocomplete', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs, controller) {
            element.autocomplete({
                minLength: 2,
                html: true,
                source: function(request, response) {
                    $.ajax({
                        url: attrs.autocomplete,
                        data: {
                            q: request.term
                        },
                        success: function (data) {
                            response($.map(data, function (item) {
                                var labelImage = $("<img class='autocomplete_interest_image'/>").attr('src', item.profile ? item.profile.mugshot : '').attr('title', item.username),
                                    labelSpan = $("<span class='autocomplete_interest_text'/>").text(item.username),
                                    label = labelImage.after(labelSpan),
                                    resp = {
                                        value: item.username,
                                        label: label,
                                        id: item.id
                                    };
                                return resp;
                            }));
                        }      ,
                        open: function () {
                            var uiAutocomplete = angular.element('.ui-autocomplete');
                            uiAutocomplete.css('height', '250');
                            uiAutocomplete.css('width', '190');
                            uiAutocomplete.css('overflow-y', 'scroll');
                        },
                        close: function () {
                            element.val('');
                        }
                    });
                }
            });
        }
    };
});
socialocaleApp.controller('EditProfileCtrl', function($scope, dialog, userDetails) {
    $scope.userDetails = userDetails;
    $scope.submitEditProfile = function() {
        angular.element('form', dialog.modalEl).ajaxSubmit();
        $scope.close();
    };
    $scope.close = function() {
        dialog.close('cancel');
    };
});
socialocaleApp.controller('MeCtrl', function($scope, MeService) {
    $scope.userDetails = function() {
        return MeService.userDetails;
    };
    $scope.showEditProfileModal = MeService.showEditProfileModal;
});