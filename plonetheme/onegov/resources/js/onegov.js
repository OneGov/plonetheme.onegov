jQuery(function($) {
  $('#portal-globalnav > li > a').click(function(e){
    e.preventDefault();
    var me = $(this);
    var parent = me.parent('li');

    // hide all but this children
    var others = $('#portal-globalnav li').not('#'+parent.attr('id'));
    others.find('ul').hide();
    others.removeClass('flyoutActive');

    var children = parent.find('ul:first');
    if (children.length == 0) {
      $.ajax({
        type : 'POST',
        url : me.attr('href') + '/load_children',
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
});
