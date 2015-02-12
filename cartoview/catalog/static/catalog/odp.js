var odp = {
    tags: null,
    apps:null,
    categories:null,
    site_root:"",
    rest_url : "",
    trackEvent: function(category, action, label, value) {       
        _gaq.push(['_trackEvent', category, action, label, value]);        
    },
    trackPageview: function(url) {        
        _gaq.push(['_trackPageview', url]);        
    },

    setupSearchInput: function () {
        if ($.query.get('qs') && $.query.get('qs') != "") {
            $("#qs")[0].value = decodeURI($.query.get('qs')).replace(/\x2B/g, " ");
        }
    
        $("#qs").focus(function (evt) {
            if (this.value == "Search for data") {
                this.value = "";
            }
        });
        $("#qs").focusout(function (evt) {
            if(this.value == "") {
                this.value = "Search for data";
            }
        });
        
        $("#search_form").submit(function(evt) {
            evt.stopImmediatePropagation();
            evt.preventDefault();
            if ($("#qs")[0].value != "" && $("#qs")[0].value != "Search for data") {
                window.location = odp.site_root + "search/?sort=name&dir=asc&qs=" + decodeURI($("#qs")[0].value);
            } else {
                window.location = odp.site_root + "search/?sort=name&dir=asc";
            }
        });
        
        $("#search_img").click(function(evt) {
            $("#search_form").submit();
        });
        
    },
    
    setupNominate: function() {
        $("#form_container").hide();
        $("#nominate_button").toggle(
          function() {
            $("#form_container").slideDown();
            $("#nominate_button").html('Cancel');
            odp.trackEvent('Nominate Data', 'Show Form');
            },
          function() {
            $("#form_container").slideUp();
            $("#nominate_button").html('Add Nomination');
            odp.trackEvent('Nominate Data', 'Hide Form');
        });
        
        if ($.query.get('nqs') && $.query.get('nqs') != "") {
            $("#nqs")[0].value = decodeURI($.query.get('nqs')).replace(/\x2B/g, " ");
        }

        $("#nqs").focus(function (evt) {
            if (this.value == "Search for nominations") {
                this.value = "";
            }
        });
        $("#nqs").focusout(function (evt) {
            if(this.value == "") {
                this.value = "Search for nominations";
            }
        });
        
        $("#n_search_form").submit(function(evt) {
            evt.stopImmediatePropagation();
            evt.preventDefault();
            if ($("#nqs")[0].value != "" && $("#nqs")[0].value != "Search for nominations") {
                window.location = odp.site_root + "nominate/?nqs=" + decodeURI($("#nqs")[0].value); 
            } else {
                window.location = odp.site_root + "nominate/";
            }
        });

        $("#n_search_img").click(function(evt) {
            $("#n_search_form").submit();
        });
        
        $("#nominate_form").submit(function(evt) {
            odp.trackEvent('Nominate Data', 'Submit Form');
        });

        odp.setupNomFilterLinks();
        odp.setupNomSortLinks();
        
    },

    setupSortLinks: function () {
        var sort_name = $("#sort_name > a")[0];//.addClass("url_image")[0];
        if (sort_name) {sort_name.innerHTML = 'A-Z';}

        /*var sort_title = $("#sort_title > a");.addClass("url_image")[0];
         if (sort_title) {sort_title.innerHTML = '';}*/
        
        var sort_rating = $("#sort_rating_score > a")[0];//.addClass("url_image")[0];
         if (sort_rating) {sort_rating.innerHTML = 'RATING';}
    
        /*var sort_vote = $("#sort_vote_count > a").addClass("url_image")[0];
         if (sort_vote) {sort_vote.innerHTML = '';}*/
        
        if ($.query.get('sort')) {
            st = $.query.get('sort');
            $("#sort_" + st + ".btn-circle").addClass('selected');
        }
        
        $("#sort .url_image").each(function () {
            $(this).hover(function() {
                $(this).removeClass('selected');
            }, function () {
                var filter_split = this.parentNode.id.split('sort_');
                if ($.query.get('sort') && $.query.get('sort') == filter_split[1]) {
                    $(this).addClass('selected');
                } /*else {
                    this.style.backgroundPosition="0 0";
                }*/
            });
        });
    },
    
    setupFilterLinks: function () {
        /*var filter_api = $("#filter_api > a").addClass("url_image")[0];
        filter_api.innerHTML = '';
        
        var filter_data = $("#filter_data > a").addClass("url_image")[0];
        filter_data.innerHTML = '';
        
        var filter_application = $("#filter_application > a").addClass("url_image")[0];
        filter_application.innerHTML = '';

        var filter_all = $("#filter_all >_all").addClass("url_image")[0];
        filter_application.innerHTML = '';*/
        
        if ($.query.get('filter')) {
            st = $.query.get('filter');
            $("#filter_" + st + ".btn-circle").addClass('selected');//.backgroundPosition="0 -45px";
        }
        else
            $("#filter_all.btn-circle").addClass('selected');
        $("#filter .btn-circle").each(function () {
            $(this).hover(function() {
                $(this).removeClass('selected');
            }, function () {
                var filter_split = this.id.split('filter_');
                if ($.query.get('filter') && $.query.get('filter') == filter_split[1]) {
                    $(this).addClass('selected');//.backgroundPosition="0 -45px";
                }/* else {
                    this.style.backgroundPosition="0 0";
                }*/
            });
        });
    },
    
    setupNomSortLinks: function () {
        var sort_name = $("#sort_suggested_date > a").addClass("url_image")[0];
        sort_name.innerHTML = '';

        var sort_rating = $("#sort_rating_score > a").addClass("url_image")[0];
        sort_rating.innerHTML = '';

        if ($.query.get('sort')) {
            st = $.query.get('sort');
            $("#sort_" + st + " > a")[0].style.backgroundPosition="0 -45px";
        }

        $("#sort .url_image").each(function () {
            $(this).hover(function() {
                this.style.backgroundPosition="0 -89px";
            }, function () {
                var filter_split = this.parentNode.id.split('sort_');
                if ($.query.get('sort') && $.query.get('sort') == filter_split[1]) {
                    this.style.backgroundPosition="0 -45px";
                } else {
                    this.style.backgroundPosition="0 0";
                }
            });
        });
    },
    
    setupNomFilterLinks: function () {
        var filter_mine = $("#filter_mine > a")
        if (filter_mine) {
            filter_mine.addClass("url_image");
            filter_mine.innerHTML = '';
        }
        var filter_done = $("#filter_done > a")
        if (filter_done) {
            filter_done.addClass("url_image");
            filter_done.innerHTML = '';
        }

        if ($.query.get('filter')) {
            st = $.query.get('filter');
            $("#filter_" + st + " > a")[0].style.backgroundPosition="0 -45px";
        }
        $("#filter .url_image").hover(function() {
            this.style.backgroundPosition="0 -90px";
        }, function () {
            var filter_split = this.parentNode.id.split('filter_');
            if ($.query.get('filter') && $.query.get('filter') == filter_split[1]) {
                this.style.backgroundPosition="0 -45px";
            } else {
                this.style.backgroundPosition="0 0";
            }
        });
    },
    
    getFiltered: function (value) {
        
        if ($.query.get('filter') == value) {
            var newQuery = "" + $.query.remove('filter').remove('page');
            window.location = window.location.pathname + newQuery;
        } 
        else {
            var newQuery = "" + $.query.set('filter', value).remove('page');
            window.location = window.location.pathname + newQuery;
        }
    },
    getNomFiltered: function (value) {
        if ($.query.get('filter') == value) {
            var newQuery = "" + $.query.remove('filter').remove('page');
            window.location = window.location.pathname + newQuery;
        } 
        else {
            var newQuery = "" + $.query.set('filter', value).remove('page');
            window.location = window.location.pathname + newQuery;
        }
    },
    setupCommentForm: function () {
        $('#resource_comment_form').submit(function (evt) {
            if ($("#id_comment")[0].value == "" || !$("#id_rating_0").hasClass("star-rating-on")) {
                evt.stopImmediatePropagation();
                evt.preventDefault();
                $('#comment_field_errors')[0].innerHTML = "You must enter both a comment and select a rating."
            }
            odp.trackEvent('Resource Comment', 'Post')
        });
    },
    
    
    getTags: function() {
        $.getJSON(odp.rest_url + 'rest/catalog/tag/?format=json', function(tags){
            odp.tags = tags.objects;
            odp.setupTagList();
        });
    },
    getCategories: function() {
        $.getJSON(odp.rest_url + 'rest/catalog/category/?format=json', function(categories){
            odp.categories = categories.objects;
            odp.setupCategoryList();
        });
    },
    setupTagList: function() {
        if (!odp.tags) {return;}
        var tag_list = "";
        for(var i = 0; i < odp.tags.length; i++) {
            var tag = odp.tags[i];
            tag_list += "<span class='badge pull-right'>" + tag.resource_count + "</span><li  id='" + tag.id + "'><a class='tag' href='" + odp.site_root + "tag/" + tag.id + "/?sort=name&dir=asc'>" + tag.tag_name + "</a></li>"
        }
        $("#tag_list").replaceWith(tag_list);
        
        odp.setNavLink();
    },
    setupCategoryList: function() {
        if (!odp.categories) {return;}
        var category_list = "";
        for(var i = 0; i < odp.categories.length; i++) {
            var category = odp.categories[i];
            category_list += "<span class='badge pull-right'>" + category.resource_count + "</span><li  id='" + category.id + "'><a class='category' href='" + odp.site_root + "category/" + category.id + "/?sort=name&dir=asc'>" + category.category_name + "</a></li>"
        }
        $("#category_list").replaceWith(category_list);

        odp.setNavLink();
    },
    getApps: function() {
        $.getJSON(odp.site_root + 'apps/', function(apps){
            odp.apps = apps;
            odp.setupAppList();
        });
    },

    setupAppList: function() {
        if (!odp.apps) {return;}
        var app_list = "";
        for(var i = 0; i < odp.apps.length; i++) {
            var app = odp.apps[i];
            app_list += "<li id='" + app.pk + "'><a class='app' href='" + odp.site_root + "search/?sort=name&dir=asc&app=" + app.fields.name +"'>" + app.fields.title + "</a></li>"
        }
        $("#app_list").replaceWith(app_list);

        odp.setNavLink();
    },
    makeTabs: function(div) {
      $(div).each(function () {
        $(this).tabs();
      });
    },
    
    makeDialog: function(div) {
        $(div).each(function () {
            //make the dialog for each thumb
            var $dialog = $(this).find('.dialog');
            $dialog.dialog({
              autoOpen: false,
              modal: true,
              draggable: false,
              resizable: false,
              // width: auto does not work in ie7/ie6
              width: 626
            });
            //open dialog by clicking the thumb
            $(this).click(function() {
              $dialog.dialog("open");
              odp.trackEvent('View Image', 'Large Image', 'Image', this.id)
              return false;
           });
           // close the window when clicking the overlay background
          /* $('.ui-widget-overlay').live("click", function() {
              $dialog.dialog("close");
          });   */
         });
      },
    
    setNavLink: function() {
        var loc = window.location.href;
        if(loc.indexOf("/tag/") != -1) {
            var id = loc.split("/tag/")[1].split("/")[0];
            $("#" + id).addClass('active_page');
        } else {
            loc = loc.split("/");
            for(var i = 0; i < loc.length; i++) {
                var val = loc.pop();
                if (val != "" && !odp.isNumber(val) && val.indexOf("=") == -1) {
                    var test = $("#" + val);
                    if (test.length == 1) {
                        test.addClass('active_page');
                        return;
                    }
                }
            }            
        }
    },

    isNumber: function(n) {
      return !isNaN(parseFloat(n)) && isFinite(n);
    }

}
      

