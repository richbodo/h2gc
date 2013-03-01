var mongo = require('mongodb');
 
var Server = mongo.Server,
Db = mongo.Db,
BSON = mongo.BSONPure;
 
var server = new Server('localhost', 27017, {auto_reconnect: true});
db = new Db('logdb', server);

//
//  Homepage renderer
//

exports.homePage = function(req, res) {
    db.collection('logs', function(err, collection) {
	collection.find().toArray(function(err, items) {
	    res.render('index', { title:'H2GC', sidebartitle:'Recent Problem Machines', loglines:items, probs:'example' });	    
	});
    });
    
};

//
// REST API functions
//
 
exports.findById = function(req, res) {
    var id = req.params.id;
    console.log('Retrieving log: ' + id);
    db.collection('logs', function(err, collection) {
	collection.findOne({'_id':new BSON.ObjectID(id)}, function(err, item) {
	    res.send(item);
	});
    });
};

exports.findPage = function(req, res) {
    var id = req.params.id;
    console.log('Retrieving log: ' + id);
    db.collection('logs', function(err, collection) {
	collection.findOne({'_id':new BSON.ObjectID(id)}, function(err, item) {
	    res.send(item);
	});
    });
};
 
exports.findAll = function(req, res) {
    db.collection('logs', function(err, collection) {
	collection.find().toArray(function(err, items) {
	    res.send(items);
	});
    });
};

exports.getHtmlPages = function(req, res) {
    db.collection('logs', function(err, collection) {
	collection.find().toArray(function(err, items) {
	    res.send(items);
	});
    });
};
 
exports.addLog = function(req, res) {
    var log = req.body;
    console.log('Adding log: ' + JSON.stringify(log));
    db.collection('logs', function(err, collection) {
	collection.insert(log, {safe:true}, function(err, result) {
	    if (err) {
		res.send({'error':'An error has occurred'});
	    } else {
		console.log('Success: ' + JSON.stringify(result[0]));
		res.send(result[0]);
	    }
	});
    });
}
 
exports.updateLog = function(req, res) {
    var id = req.params.id;
    var log = req.body;
    console.log('Updating log: ' + id);
    console.log(JSON.stringify(log));
    db.collection('logs', function(err, collection) {
	collection.update({'_id':new BSON.ObjectID(id)}, log, {safe:true}, function(err, result) {
	    if (err) {
		console.log('Error updating log: ' + err);
		res.send({'error':'An error has occurred'});
	    } else {
		console.log('' + result + ' document(s) updated');
		res.send(log);
	    }
	});
    });
}
 
exports.deleteLog = function(req, res) {
    var id = req.params.id;
    console.log('Deleting log: ' + id);
    db.collection('logs', function(err, collection) {
	collection.remove({'_id':new BSON.ObjectID(id)}, {safe:true}, function(err, result) {
	    if (err) {
		res.send({'error':'An error has occurred - ' + err});
	    } else {
		console.log('' + result + ' document(s) deleted');
		res.send(req.body);
	    }
	});
    });
}


//
// db functions
//
 
db.open(function(err, db) {
    if(!err) {
	console.log("Connected to 'logdb' database");
	db.collection('logs', {safe:true}, function(err, collection) {
	    if (err) {
		console.log("The 'logs' collection doesn't exist. Creating it with sample data...");
		populateDB();
	    }
	});
    }
});
 
var populateDB = function() {
    var logs = [
	{
	    computer: "asfasdfsadfasf",
	    status: "0"
	},
	{
	    computer: "qerqwerwqreqwerqre",
	    status: "0"
	}];

db.collection('logs', function(err, collection) {
    collection.insert(logs, {safe:true}, function(err, result) {});
});
 
};
