var express = require('express');
var jade = require('jade');
var stylus = require('stylus');
var nib = require('nib');

log = require('./routes/logs');
 
var app = express();

function compile(str, path) {
  return stylus(str)
    .set('filename', path)
    .use(nib())
} 

app.configure(function () {
    app.set('views', __dirname + '/views');
    app.set('view engine', 'jade');
    app.use(express.logger('dev')); /* 'default', 'short', 'tiny', 'dev' */
    app.use(express.bodyParser());
    app.use(stylus.middleware(
	{ src: __dirname + '/public'
	  , compile: compile
	}
    ))
    app.use(express.static(__dirname + '/public'))
});


app.get('/', log.homePage); 
app.get('/logs', log.findAll);
app.get('/logs/:id', log.findById);
app.get('/humanpages', log.getHtmlPages);
app.get('/humanpages/:id', log.findPage);
app.post('/logs', log.addLog);
app.put('/logs/:id', log.updateLog);
app.delete('/logs/:id', log.deleteLog);

app.listen(3000);
console.log('Listening on port 3000...');	
