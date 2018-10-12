//Set random image in welcome page
var random_number = Math.floor((Math.random() * images.length));
var random_image = images[random_number]; // images are initialized in core/welcome.js

$('#header').css(
  {
    'background': 'url(' + random_image + ')',
    'background-position': 'center center',
    'background-repeat': 'no-repeat',
    'background-size': 'cover'
  }
)

