/**
 * Created by alian on 16/4/18.
 */

$.ajaxSetup({

  dataType: "json",
  beforeSend: function(xhr, settings){
      var csrftoken = $.cookie('csrftoken');
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
  }
});