'use strict';

let stream = require( 'stream' );
let Scraper = require( 'twitter-scraper' ).Scraper;

let query = 'from:emol since:2015-05-01 until:2015-06-01';
let scraper = new Scraper( query );
let toConsole = new stream.Writable( {
  objectMode: true,
  write: function( tweet, enc, cb ) {
    console.log( 'Got tweet: ', tweet );
    return cb();
  }
} )
scraper.pipe( toConsole );

// Start the scraper
scraper.start();
