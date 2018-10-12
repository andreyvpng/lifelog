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
