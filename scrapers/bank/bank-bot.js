const express = require('express');
const bodyParser = require('body-parser');
const request = require("request");

const port = 8080;
const app = express();

app.listen(port, function(){
  console.log('Starting server at port: ' + port);
});

app.use(bodyParser());

app.use('/', express.static('../client/'));

app.post('/bank-wrapper',function(req, res) {
  const j = request.jar();
  const cookies = request.cookie('ctx=persona; path=/');
  j.setCookie(cookies, 'https://login.bancochile.cl/bancochile-web/persona/login/index.html#/login');
  request.defaults({jar: j});
  request({
    url: "https://login.bancochile.cl/bancochile-web/persona/login/index.html#/login",
    method: "GET",
    headers: {
      'cookies': j
    }
  }, function(error, response, body) {
    console.log('1');
    console.log(response);
  });
  wait(1000);
  request({
    url: "https://login.bancochile.cl/oam/server/auth_cred_submit",
    method: "POST",
    form: {
      username2:req.body.username,
      userpassword: req.body.password,
      request_id: '',
      ctx: 'persona',
      path: '/',
      username: req.body.username,
      password: req.body.password
    },
    headers: {
      'cookies': j
    }
  }, function(error, response, body) {
    console.log('2');
    console.log(response);
  });
  wait(1000);
  request({
    url: "https://login.bancochile.cl/bancochile-web/persona/oam/server/auth_cred_submit",
    method: "POST",
    form: {
      username2:req.body.username,
      userpassword: req.body.password,
      request_id: '',
      ctx: 'persona',
      path: '/',
      username: req.body.username,
      password: req.body.password
    },
    headers: {
      'cookies': j
    }
  }, function(error, response, body) {
    console.log('3');
  });
  wait(1000);
  request({
    url: "https://login.bancochile.cl/persona/oam/server/auth_cred_submit",
    method: "POST",
    form: {
      username2:req.body.username,
      userpassword: req.body.password,
      request_id: '',
      ctx: 'persona',
      path: '/',
      username: req.body.username,
      password: req.body.password
    },
    headers: {
      'cookies': j
    }
  }, function(error, response, body) {
    console.log('4');
  });
  wait(1000);
  request({
    url: "https://login.bancochile.cl/bancochile-web/persona/rest/login",
    method: "POST",
    form: {
      username2:req.body.username,
      userpassword: req.body.password,
      request_id: '',
      ctx: 'persona',
      path: '/',
      username: req.body.username,
      password: req.body.password
    },
    headers: {
      'cookies': j
    }
  }, function(error, response, body) {
    console.log('5');
  });
  wait(1000);
  request({
    url: "https://login.bancochile.cl/persona/rest/login",
    method: "POST",
    form: {
      username2:req.body.username,
      userpassword: req.body.password,
      request_id: '',
      ctx: 'persona',
      path: '/',
      username: req.body.username,
      password: req.body.password
    },
    headers: {
      'cookies': j
    }
  }, function(error, response, body) {
    console.log('6');
  });
  wait(1000);
  request({
    url: "https://login.bancochile.cl/rest/login",
    method: "POST",
    form: {
      username2:req.body.username,
      userpassword: req.body.password,
      request_id: '',
      ctx: 'persona',
      path: '/',
      username: req.body.username,
      password: req.body.password
    },
    headers: {
      'cookies': cookies
    }
  }, function(error, response, body) {
    console.log('7');
  });
  wait(1000);
  request({
    url: "https://portalpersonas.bancochile.cl/mibancochile/rest/persona/tef-rest/tef/cartola-actual?year=2016&month=12&tipoCartola=R&reciente=false",
    method: "GET",
    headers: {
      'cookies': j
    }
  }, function(error, response, body) {
    console.log('8');
  });
  request.post({
    url: 'https://login.bancochile.cl/oam/server/auth_cred_submit',
    form: {
      username2:req.body.username,
      userpassword: req.body.password,
      request_id: '',
      ctx: 'persona',
      path: '/',
      username: req.body.username,
      password: req.body.password
    }
  }, function(error, response, body){
    request.get({
        url:"https://portalpersonas.bancochile.cl/mibancochile/rest/persona/tef-rest/tef/cartola-actual?year=2016&month=12&tipoCartola=R&reciente=false",
        header: response.headers
    },function(error, response, body){
        console.log(9);
    });
  });
});

function wait(ms){
   let start = new Date().getTime();
   let end = start;
   while(end < start + ms) {
     end = new Date().getTime();
  }
};
