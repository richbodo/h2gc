var express = require('express'),
log = require('./routes/logs');
 
var app = express();
 
app.configure(function () {
    app.use(express.logger('dev')); /* 'default', 'short', 'tiny', 'dev' */
    app.use(express.bodyParser());
});
 
app.get('/logs', log.findAll);
app.get('/logs/:id', log.findById);
app.post('/logs', log.addLog);
app.put('/logs/:id', log.updateLog);
app.delete('/logs/:id', log.deleteLog);
 
app.listen(3000);
console.log('Listening on port 3000...');	
