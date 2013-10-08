jQuery(function($) {

  // flyout navigation
  $('#portal-globalnav > li > .wrapper a').click(function(e){
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

  // To top link
  $('div.to_top a').click(function(e) {
    e.preventDefault();
    $('html, body').scrollTop(0);
  });

  // Toggle languageselector menu
  $('#toggle_subsitelangs').click(function(e){
    e.preventDefault();
    var me = $(this)
    close_opened(me);
    me.toggleClass('selected');
    $('#portal-languageselector dd.actionMenuContent').toggle();
  });

});
