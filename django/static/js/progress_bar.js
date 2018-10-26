$(".card > .progress > .progress-bar").each(function( index ) {

  var percent = 100,
      record_sum = $( this ).attr('record_sum'),
      goal_daily_value = $( this ).attr('goal_daily_value');

  // Is a goal created for this action?
  if (goal_daily_value != "") {
    percent = parseInt(record_sum) * 100 / parseInt(goal_daily_value);

    if (percent > 100) {
      percent = 100;
    }
  }

  percent = "" + percent + "%";

  $( this ).css(
    {
      'width': percent
    }
  )
});

var card_output = $(".card-output");

if (card_output.length) {
  function get_color(elem) {
    color_id = elem.val()
    color = 'action-' + elem.text().split(' ')[color_id]
    return color;
  }

  $("#card-title").text($("form #div_id_text input").val())
  $("#card-unit").text($("form #div_id_unit input").val())
  $("#progress-bar")[0].classList = ['progress-bar', get_color($("form #div_id_color select"))].join(' ')


  $("form #div_id_text input").on("input", function(e) {
    $("#card-title").text( $(e.target).val() )
  });

  $("form #div_id_unit input").on("input", function(e) {
    $("#card-unit").text( $(e.target).val() )
  });

  $("form #div_id_color select").on("input", function(e) {
    $("#progress-bar")[0].classList = ['progress-bar', get_color($(e.target))].join(' ')
  });
}
