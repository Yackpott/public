var requestify = require('requestify');

var user = 'scarlettjohannson';
var pattern = /[^{]"id": "[^\"]*"|"display_src": "[^\"]*"|"comments": {[^\}]*}|"likes": {[^\}]*}/g;
requestify.get('https://www.instagram.com/' + user + '/')
  .then(function(res) {
    var match = res.getBody().match(pattern);
    for (i = 0; i < match.length; i++) {
      console.log(match[i]);
    }
  }
);
