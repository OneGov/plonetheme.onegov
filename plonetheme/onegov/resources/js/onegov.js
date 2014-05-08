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

jQuery(function($) {

  // flyout navigation
  $('#portal-globalnav.flyoutEnabled > li > .wrapper a').click(function(e){
    e.preventDefault();
    var me = $(this);
    var parent = me.parent('.wrapper').parent('li');

    // hide all but this children
    var others = $('#portal-globalnav li').not('#'+parent.attr('id'));
    others.find('ul').hide();
    others.removeClass('flyoutActive');

    var children = parent.find('ul:first');
    if (children.length == 0) {
      $.ajax({
        type : 'POST',
        url : me.attr('href') + '/load_flyout_children',
        success : function(data, textStatus, XMLHttpRequest) {
          if (textStatus == 'success') {
            var result = $(data);
            parent.removeClass('loading');
            parent.append(result);
          }
        }
      });
    }
    parent.toggleClass('flyoutActive');
    children.toggle();
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
    var me = $(this)
    close_opened(me);
    me.toggleClass('selected');
    $('#portal-languageselector dd.actionMenuContent').toggle();
  });

  // breadcrumbs

  $('#portal-breadcrumbs .flyoutBreadcrumbs .crumb > a').each(function(a,b){
    var obj = $(b);
    if (!obj.hasClass('factory')) {
      $.ajax({
        type : 'POST',
        url : obj.attr('href') + '/load_flyout_children',
        data: {breadcrumbs: true},
        success : function(data, textStatus, XMLHttpRequest) {
          if (textStatus == 'success') {
            if (data.length > 0) {
              if (data.search('<ul class="children">')!=-1) {
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
        }
      });
    }
  });

  $('#portal-breadcrumbs .flyoutBreadcrumbs a.loadChildren').live('click', function(e){
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
