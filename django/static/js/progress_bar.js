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

  var form_title = $("form #div_id_text input"),
      form_unit = $("form #div_id_unit input"),
      form_color = $("form #div_id_color select");

  var card_title = $("#card-title"),
      card_unit = $("#card-unit"),
      card_color = $("#progress-bar");

  card_title.text(form_title.val())
  card_unit.text(form_unit.val())
  card_color[0].classList = ['progress-bar', get_color(form_color)].join(' ')


  form_title.on("input", function(e) {
    card_title.text( $(e.target).val() )
  });

  form_unit.on("input", function(e) {
    card_unit.text( $(e.target).val() )
  });

  form_color.on("input", function(e) {
    card_color[0].classList = ['progress-bar', get_color($(e.target))].join(' ')
  });
}
