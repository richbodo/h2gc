var sys = require('sys');
var exec = require('child_process').exec;

var mongo = require('mongodb'); 
var Server = mongo.Server,
Db = mongo.Db,
BSON = mongo.BSONPure;
var server = new Server('localhost', 27017, {auto_reconnect: true});

// Super simple - DB is logdb, collection is logs
db = new Db('logdb', server);

//
//  Homepage renderer
//

exports.homePage = function(req, res) {
    db.collection('logs', function(err, collection) {
	// db.logs.find( { "status" : { $ne: "0" } } ) works
        // 
	collection.find({ "status" : { $ne: "0" } } ).sort({datetime: 1}).limit(10).toArray(function(err, items) {
	    res.render('index', { title:'H2GC', sidebartitle:'Recent Checkins', loglines:items });	    
	});
    });
    
};

//
//  REST API functions
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
    var logstringified = JSON.stringify(log);
    var child;
    console.log('Adding log: ' + logstringified);
    db.collection('logs', function(err, collection) {

    // First integration test - uservoice
    if ( log.status !== "0" ) {
	console.log('non-zero, executing command.');
	// uservoice api key is not enabled yet so just sending email
	// fixup the home dir, add server config
	child = exec("/home/richbodo/integrations/send_gmail.py", function (error, stdout, stderr) {
	    sys.print('stdout: ' + stdout);
	    sys.print('stderr: ' + stderr);
	    if (error !== null) {
		console.log('exec error: ' + error);
	    }
	});

    }

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
	    device: "asfasdfsadfasf",
	    status: "0",
	    datetime: "124312432134"
	},
	{
	    device: "qerqwerwqreqwerqre",
	    status: "0",
	    datetime: "3653464563"
	}];

db.collection('logs', function(err, collection) {
    collection.insert(logs, {safe:true}, function(err, result) {});
});
 
};
