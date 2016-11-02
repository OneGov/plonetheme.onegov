var c=0;

function close_opened_breadcrumbs(element) {
  $('#portal-breadcrumbs .flyoutBreadcrumbs .crumb.active > ul').each(function(a,b){
    var object = $(b);
    if (object.parent().find('a.loadChildren').attr('href') != element.attr('href')) {
      object.hide();
      object.parent().removeClass('active');
    }
  });
}

function valid_response(data) {
  // It's possible that we do no get what we expect.
  return $(data).is('ul.flyoutChildren') || $(data).is('ul.children');
}

jQuery(function($) {

   var load_flyout_grandchildren = function(indicator, open) {
      var me = indicator.children("a:first");
      var parent = me.parent('li');

      // hide grandchildren of other children
      var others = parent.siblings();
      others.find('ul.flyoutChildren').hide();
      others.removeClass('flyoutActive');
      // show my grandchildren
      var children = parent.find('ul:first');
      if (children.length == 0) { // load grandchildren once
          if (open) {
              $.ajax({
                type : 'GET',
                url : me.attr('href') + '/load_flyout_children',
                success : function(data, textStatus, XMLHttpRequest) {
                  if (textStatus == 'success') {
                    var result = $(data);
                    result.show();
                    parent.removeClass('loading');
                    parent.append(result);
                  }
                }
              });
          };
      } else {
          children.toggle();
      };
      if(open) {
        parent.toggleClass('flyoutActive');
      }
  };

  var load_flyout_children = function(indicator, open) {
    var me = indicator;
    var parent = me.parent('.wrapper').parent('li');

    // hide all but this children
    var others = $('#portal-globalnav li').not('#'+parent.attr('id'));
    others.find('ul').hide();
    others.removeClass('flyoutActive');

    var children = parent.find('ul:first');
    if (children.length == 0) {
      $.ajax({
        type : 'GET',
        url : me.attr('href') + '/load_flyout_children',
        success : function(data, textStatus, XMLHttpRequest) {
          if (textStatus == 'success' && valid_response(data)) {
            var result = $(data);
            result.hide();
            parent.removeClass('loading');
            parent.append(result);

            // flyout navigation grandchildren
            if ($("#portal-globalnav").hasClass('flyoutGrandchildrenEnabled')) {
                parent.find('.level1').not(".noChildren").hover(function(e){
                  e.preventDefault();
                  load_flyout_grandchildren($(this), true);
                }, function(e){
                  e.preventDefault();
                  load_flyout_grandchildren($(this), false);
                });
            }
          }
        }
      });
    }
    if(open) {
      parent.toggleClass('flyoutActive');
    }
    children.toggle();
  }

  $('#portal-globalnav.flyoutEnabled > li > .wrapper a').each(function(idx, el){
    load_flyout_children($(el), false);
  });

  // flyout navigation
  $('#portal-globalnav.flyoutEnabled > li > .wrapper a').click(function(e){
    e.preventDefault();
    load_flyout_children($(this), true);
  });
  // close flyout and breadcrumb children onclick on body
  $('body').click(function(e){
    if (!$(e.target).closest( "#portal-globalnav" ).length) {
      $('#portal-globalnav li').removeClass('flyoutActive').find('ul').hide();
    }
    if (!$(e.target).closest( "#portal-breadcrumbs .crumb" ).length) {
      $('#portal-breadcrumbs .flyoutBreadcrumbs .crumb.active').removeClass('active').find('ul').hide();
    }
  });

  // To top link
  $('div.to_top a').click(function(e) {
    e.preventDefault();
    $('html, body').scrollTop(0).focus().blur();
  });

  // Toggle languageselector menu
  $('#toggle_subsitelangs').click(function(e){
    e.preventDefault();
    var me = $(this);
    close_opened(me);
    me.toggleClass('selected');
    $('#portal-languageselector actionMenuContent').toggle();
  });

  // breadcrumbs

  $('#portal-breadcrumbs .flyoutBreadcrumbs .crumb > a').each(function(a,b){
    var obj = $(b);
    if (!obj.hasClass('factory')) {
      $.ajax({
        type : 'GET',
        url : obj.attr('href') + '/load_flyout_children',
        data: {breadcrumbs: true},
        success : function(data, textStatus, XMLHttpRequest) {
          if (textStatus === 'success' && valid_response(data)) {
            if ($(data).hasClass('children') && $(data).is('ul')) {
              obj.after('<a href="'+obj.attr('href')+'" class="loadChildren" tabindex="-1">▼</a>');
              obj.after(data);
            }
            else {
              obj.addClass('noChildren');
            }
          }
          else {
            obj.addClass('noChildren');
          }
        }
      });
    }
  });

  $('#portal-breadcrumbs').delegate('.flyoutBreadcrumbs a.loadChildren', 'click', function(e){
    e.preventDefault();
    var me = $(this);
    var parent = me.parent();
    var children = parent.find('ul.children');
    close_opened_breadcrumbs(me);
    children.toggle();
    parent.toggleClass('active');
  });

  // customstyles :-)
  $('#fieldsetlegend-importexport').click(function(e){
    if (c==0) setTimeout("c=0;", 2000);
    c += 1;
    if (c==10) $('#custom-scss-field').fadeIn('slow');
  });

});
