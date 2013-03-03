const Lang = imports.lang;
const St = imports.gi.St;
const GLib = imports.gi.GLib;
const Shell = imports.gi.Shell;
const Gdk = imports.gi.Gdk;
const Gtk = imports.gi.Gtk
const Main = imports.ui.main;
const Util = imports.misc.util;
const Mainloop = imports.mainloop;
const PanelMenu = imports.ui.panelMenu;
const PopupMenu = imports.ui.popupMenu;
const Me = imports.misc.extensionUtils.getCurrentExtension();
const Convenience = Me.imports.convenience;

let settings;
let metadata = Me.metadata;

function CpuTemperature() {
    this._init.apply(this, arguments);
}

CpuTemperature.prototype = {
    __proto__: PanelMenu.SystemStatusButton.prototype,

    _init: function(){
        PanelMenu.SystemStatusButton.prototype._init.call(this, 'temperature');

	// I think this is the label on the top panel
	//
        this.statusLabel = new St.Label({
            text: "--",
            style_class: "temperature-label"
        });

        // destroy all previously created children, and add our statusLabel
	//
        this.actor.get_children().forEach(function(c) {
            c.destroy()
        });
        this.actor.add_actor(this.statusLabel);

	// get saved preferences
	//
        let update_time  = settings.get_int('update-time');
        let display_hdd_temp  = settings.get_boolean('display-hdd-temp');

        // locating programs, setting up help stuff       
	//
        this.sensorsPath = GLib.find_program_in_path('sensors');

        if (display_hdd_temp){
            this.hddtempPath = this._detectHDDTemp();
            this.hddtempDaemonPort = this._detectHDDTempDaemon();
        }

        this.command=["xdg-open", "http://github.com/xtranophilist/gnome-shell-extension-cpu-temperature/issues/"];

        if(this.sensorsPath){
            this.title='Error';
            this.content='Run sensors-detect as root. If it doesn\'t help, click here to report with your sensors output!';
        }
        else{
            this.title='Warning';
            this.content='Please install lm_sensors. If it doesn\'t help, click here to report with your sensors output!';
        }

	// find current status and update label: 
	//  this.statusLabel.set_text(this.title);
        //this._update_temp();
	this._update_system_status();

	// by default every 15 seconds, update loop that runs update_system_status
	//
        event = GLib.timeout_add_seconds(0, update_time, Lang.bind(this, function () {
            this._update_system_status();
            return true;
        }));
    },

    _detectHDDTemp: function(){
        //detect if hddtemp is installed
        let hddtempPath = null;
        let ret = GLib.spawn_command_line_sync("which hddtemp");
        if ( (ret[0]) && (ret[3] == 0) ) {//if yes
            hddtempPath =ret[1].toString().split("\n", 1)[0];
            // for any reason it is not possible to run hddtemp directly.
            if(GLib.spawn_command_line_sync(hddtempPath)[3])
                hddtempPath = null;
        }
        return hddtempPath;
    },

    _detectHDDTempDaemon: function(){
        //detect if hddtemp is running as daemon
        let hddtempDaemonPort = null;
        let ret = GLib.spawn_command_line_sync("pidof hddtemp");
        if(ret[1].length) {
            let cmdline = GLib.spawn_command_line_sync("ps --pid=" + ret[1] + " -o args=");
            //get listening TCP port
            hddtempDaemonPort = cmdline[1].toString().split("-p ")[1].split(" ")[0];
        }

        return hddtempDaemonPort;
    },


    // Updates system status number from file
    // Builds the popup menu from scratch
    //
    _update_system_status: function() {

	// Set the title of the top menu
        var systemStatus = this._findSystemStatusFromFile();
	this.title = systemStatus;
        this.statusLabel.set_text(this.title);

	// mysterious housekeeping
        this.menu.box.get_children().forEach(function(c) {
            c.destroy()
        });

	// Build the menu section item by item
	//
        let section = new PopupMenu.PopupMenuSection("Temperature");
        var _appSys = Shell.AppSystem.get_default();
        var _gsmPrefs = _appSys.lookup_app('gnome-shell-extension-prefs.desktop');
        let item;

	var oneliner_s = this._doExplain();
        item = new PopupMenu.PopupMenuItem(oneliner_s.toString());
        section.addMenuItem(item);

        item = new PopupMenu.PopupMenuItem("Search");
        section.addMenuItem(item);
	item.connect('activate', Lang.bind(this, this._doSearch));
 
        item = new PopupMenu.PopupMenuItem("Learn");
        section.addMenuItem(item);
	item.connect('activate', Lang.bind(this, this._doLearn));

        item = new PopupMenu.PopupMenuItem("Collaborate");
        section.addMenuItem(item);
	item.connect('activate', Lang.bind(this, this._doCollaborate));

        item = new PopupMenu.PopupMenuItem("Get Help");
        section.addMenuItem(item);
	item.connect('activate', Lang.bind(this, this._doGetHelp));	

        item = new PopupMenu.PopupMenuItem("Share");
        section.addMenuItem(item);
	item.connect('activate', Lang.bind(this, this._doShare));

	// Add the preferences menu item
	//
        item = new PopupMenu.PopupMenuItem(_("Change Stuff"));
        item.connect('activate', function () {
            if (_gsmPrefs.get_state() == _gsmPrefs.SHELL_APP_STATE_RUNNING){
                _gsmPrefs.activate();
            } else {
                _gsmPrefs.launch(global.display.get_current_time_roundtrip(),
                                 [metadata.uuid],-1,null);
            }
        });
        section.addMenuItem(item);

	// Now add the section
        this.menu.addMenuItem(section);	

    },


    _doExplain: function() {	
	global.log("In Explain");
	// read from disk and display oneliner sad file
	// the file should contain a single plain english sentence with no tech jargon 
	let oneliner_file = GLib.get_home_dir() + '/.h2gc/sad'
	if (GLib.file_test(oneliner_file,1<<4)) {
            let oneliner_object = GLib.file_get_contents(oneliner_file);
            if(oneliner_object[0]) {
		var oneliner_string = oneliner_object[1];
		global.log("oneliner_string: ");
		global.log(oneliner_string);
		return oneliner_string;    
            }	    
	}
	return "This program can't read it's status summary - that's an internal problem."
    },

    _doSearch: function() {	
	global.log("In Search");
	// need some default search text in prefs, or some better way to handle a default here
	var search_text = "hitchhikers guide to your computer h2gc"
	var priority_text = ""

	// the priority file should contain the name of the check that is most seriously troubling
	// if the priority file is empty, well, I'm not sure what we should do.  maybe open to the default search 
	let priority_file = GLib.get_home_dir() + '/.h2gc/priority'
	if (GLib.file_test(priority_file,1<<4)) {
            let priority_object = GLib.file_get_contents(priority_file);
            if(priority_object[0]) {
		var priority_string = priority_object[1];
		global.log("priority_string: ");
		global.log(priority_string);
		priority_text = priority_string; 
            }	    
	}	

	if (priority_text == "") {
	    // Open the web browser to search on the terms recommended
	    //
	    global.log("No Priority Found.");
	    let search_engine = "https://encrypted.google.com/search?q="
	    let searchurl = search_engine + search_text;
            Gtk.show_uri(null, searchurl, Gdk.CURRENT_TIME);
            return true;
        }
 
	// the checkname.search file contains search terms regarding the most serious problem at hand
	let search_terms_file = GLib.get_home_dir() + "/.h2gc/scripts/" + priority_string + ".search"
	if (GLib.file_test(search_terms_file,1<<4)) {
            let search_terms_object = GLib.file_get_contents(search_terms_file);
            if(search_terms_object[0]) {
		var search_terms_string = search_terms_object[1];
		global.log("search_terms_string: ");
		global.log(search_terms_string);
		search_text = search_terms_string; 
            }	    
	}	

	// Open the web browser to search on the terms recommended
	//
	let search_engine = "https://encrypted.google.com/search?q="
	let searchurl = search_engine + search_text;
        Gtk.show_uri(null, searchurl, Gdk.CURRENT_TIME);
        return true;    
    },

    _doCollaborate: function() {
	global.log("In Collaborate.");
	// could go to a specific chatroom for specific problems, but I think that's overkill for most orgs
	// if it were an external chatroom, like irc or something, then I can see doing that.
	// should be configurable
	let chatroom = "https://kungfuvrobots.hipchat.com/chat"
	global.log(chatroom)
        Gtk.show_uri(null, chatroom, Gdk.CURRENT_TIME);
        return true;    
    },

    _doShare: function() {	
	global.log("In Share");
	// compile basic system information, what's running, etc.
	// ask user what's new, then post all of that to a new wiki page
	// post the link to the wiki page that juts got made to whatever social network they prefer
	// as in the android share feature.
	// really large function that I haven't had time to write.
        return true;    
    },

    _doLearn: function() {	
	global.log("In Learn.");
	var priority_text = ""

	// the priority file should contain the name of the check that is most seriously troubling
	// if the priority file is empty, well, I'm not sure what we should do.  maybe open to the default search 
	let home_dir = GLib.get_home_dir()
	let priority_file = home_dir + '/.h2gc/priority'

	if (GLib.file_test(priority_file,1<<4)) {
            let priority_object = GLib.file_get_contents(priority_file);
            if(priority_object[0]) {
		var priority_string = priority_object[1];
		global.log("priority_string: ");
		global.log(priority_string);
		priority_text = priority_string; 
            }	    
	}	

	if (priority_text == "") {
	    let local_html = "file://" + home_dir + "/.h2gc/docs/" + "index.html" 
	    global.log(local_html)
            Gtk.show_uri(null, local_html, Gdk.CURRENT_TIME);
            return true;
        } else {
	    let local_html = "file://" + home_dir + "/.h2gc/docs/" + priority_text + ".html" 
	    global.log(local_html)
            Gtk.show_uri(null, local_html, Gdk.CURRENT_TIME);
            return true;
	} 
    },

    _doGetHelp: function() {	
	// Write debug summary to file
	// Open a web browser and form an email with an attachment of debug info
	// For now just going here: http://kungfuvrobots.uservoice.com/forums/196593-general/
	global.log("In Get Help.");
	let helpdesk = "http://kungfuvrobots.uservoice.com/forums/196593-general/"
	global.log(helpdesk)
        Gtk.show_uri(null, helpdesk, Gdk.CURRENT_TIME);
        return true;    
    },

    // Finds current temperatures
    // Updates status label field "title"
    // Builds the popup menu from scratch
    //
    _update_temp: function() {

        let items = new Array();
        let tempInfo=null;
        if (this.sensorsPath){

	    //get the output of the sensors command

            let sensors_output = GLib.spawn_command_line_sync(this.sensorsPath);

	    //get temperature from sensors

            if(sensors_output[0]) tempInfo = this._findTemperatureFromSensorsOutput(sensors_output[1].toString());

            if (tempInfo){
                var s=0, n=0;//sum and count
		var smax = 0;//max temp
                for (let sensor in tempInfo){
			if (tempInfo[sensor]['temp']>0 && tempInfo[sensor]['temp']<115){
	                    s+=tempInfo[sensor]['temp'];
        	            n++;
			    if (tempInfo[sensor]['temp'] > smax)
				smax=tempInfo[sensor]['temp'];
        	            items.push(tempInfo[sensor]['label']+': '+this._formatTemp(tempInfo[sensor]['temp']));
			}
                }
                if (n!=0){//if temperature is detected
                    if (settings.get_string('show-in-panel')=='Average'){
                    this.title=this._formatTemp(s/n);//set title as average
                }
                else{
                    this.title=this._formatTemp(smax);//or the maximum temp
                }
                }
            }
        }
 
        //if we don't have the temperature yet, use some known files
        if(!tempInfo){
            tempInfo = this._findTemperatureFromFiles();
            if(tempInfo.temp){
                this.title=this._formatTemp(tempInfo.temp);
                items.push('Current Temperature : '+this._formatTemp(tempInfo.temp));
                if (tempInfo.crit)
                    items.push('Critical Temperature : '+this._formatTemp(tempInfo.crit));
            }
        }

        if (this.hddtempPath){
            let hddtemp_output = GLib.spawn_command_line_sync(this.hddtempPath);//get the output of the hddtemp command
            if(hddtemp_output[0]) tempInfo = this._findTemperatureFromHDDTempOutput(hddtemp_output[1].toString());//get temperature from hddtemp
            if(tempInfo){
                for (let sensor in tempInfo){
                    items.push('Disk ' + tempInfo[sensor]['label']+': '+this._formatTemp(tempInfo[sensor]['temp']));
                }
            }
        }
        else if (this.hddtempDaemonPort) {  //Try hddtemp daemon
            let hddtemp_output = GLib.spawn_command_line_sync("nc localhost " + this.hddtempDaemonPort); //query hddtemp daemon on loopback interface
            if(hddtemp_output[0]) tempInfo = this._findTemperatureFromHDDTempDaemon(hddtemp_output[1].toString());//get temperature from hddtemp
            if(tempInfo){
                for (let sensor in tempInfo){
                    items.push('Disk ' + tempInfo[sensor]['label']+': '+this._formatTemp(tempInfo[sensor]['temp']));
                }
            }
        }

        this.statusLabel.set_text(this.title);
        this.menu.box.get_children().forEach(function(c) {
            c.destroy()
        });

	// Build entire menu from scratch
	//
        let section = new PopupMenu.PopupMenuSection("Temperature");
        if (items.length>0){
            let item;
            for each (let itemText in items){
                item = new PopupMenu.PopupMenuItem(itemText);
                section.addMenuItem(item);
            }
        }else{
            let command=this.command;
            let item = new PopupMenu.PopupMenuItem(this.content);
            item.connect('activate',function() {
                Util.spawn(command);
            });
            section.addMenuItem(item);
        }

        let _appSys = Shell.AppSystem.get_default();
        let _gsmPrefs = _appSys.lookup_app('gnome-shell-extension-prefs.desktop');

	// Add the preferences menu item
	//
        item = new PopupMenu.PopupMenuItem(_("Changed prefs..."));
        item.connect('activate', function () {
            if (_gsmPrefs.get_state() == _gsmPrefs.SHELL_APP_STATE_RUNNING){
                _gsmPrefs.activate();
            } else {
                _gsmPrefs.launch(global.display.get_current_time_roundtrip(),
                                 [metadata.uuid],-1,null);
            }
        });
        section.addMenuItem(item);
        this.menu.addMenuItem(section);
    },

    _findSystemStatusFromFile: function(){
        var system_status_string = "System Status: ";
	var status_file = GLib.get_home_dir() + '/.h2gc/status';
        
	// Have to have some bad status in case we couldn't read anything in
	// need to put more effort into detect/report/handle errors
	// need to take an hour or two to learn javascript, too!
	var status_modifier = "UNKNOWN"
	var status_number = 1;

	global.log("In findSystemStatusFromFile status file is : " + status_file);
	
        if (GLib.file_test(status_file,1<<4)) {
            let status_contents = GLib.file_get_contents(status_file);
	    if(status_contents[0]) {
		var status_lines = status_contents[1].toString().split("\n");
		status_number = parseInt(status_lines[0]);
		global.log("status_lines: ");
		global.log(status_lines);
		global.log("status_number: ");
		global.log(status_number);
	    } else {
		system_status_string += status_modifier;
		return system_status_string;
	    }	
        } else {
	    system_status_string += status_modifier;
	    return system_status_string;
	}    

        if ( status_number >=75 ) { status_modifier = "IMMEDIATE ACTION REQUIRED"; }
	else if ( status_number >=50 ) { status_modifier = "MAJOR ISSUES"; }
	else if ( status_number >=25 ) { status_modifier = "MINOR ISSUES"; }
	else if ( status_number >=10 ) {	status_modifier = "OK"; }
	else status_modifier = "AWESOME";

	system_status_string += status_modifier;

	return system_status_string
    },
    
    _findTemperatureFromFiles: function(){
        let info = new Array();
        let temp_files = [
        //hwmon for new 2.6.39, 3.x linux kernels
        '/sys/class/hwmon/hwmon0/temp1_input',
        '/sys/devices/platform/coretemp.0/temp1_input',
        '/sys/bus/acpi/devices/LNXTHERM\:00/thermal_zone/temp',
        '/sys/devices/virtual/thermal/thermal_zone0/temp',
        '/sys/bus/acpi/drivers/ATK0110/ATK0110:00/hwmon/hwmon0/temp1_input',
        //old kernels with proc fs
        '/proc/acpi/thermal_zone/THM0/temperature',
        '/proc/acpi/thermal_zone/THRM/temperature',
        '/proc/acpi/thermal_zone/THR0/temperature',
        '/proc/acpi/thermal_zone/TZ0/temperature',
        //Debian Sid/Experimental on AMD-64
        '/sys/class/hwmon/hwmon0/device/temp1_input'];
        for each (let file in temp_files){
            if(GLib.file_test(file,1<<4)){
                //let f = Gio.file_new_for_path(file);
                //f.read_async(0, null, function(source, result) {debug(source.read_finish(result).read())});

                let temperature = GLib.file_get_contents(file);
                if(temperature[0]) {
                    info['temp']= parseInt(temperature[1])/1000;
                }
            }
            break;
        }
        let crit_files = ['/sys/devices/platform/coretemp.0/temp1_crit',
        '/sys/bus/acpi/drivers/ATK0110/ATK0110:00/hwmon/hwmon0/temp1_crit',
        //hwmon for new 2.6.39, 3.0 linux kernels
        '/sys/class/hwmon/hwmon0/temp1_crit',
        //Debian Sid/Experimental on AMD-64
        '/sys/class/hwmon/hwmon0/device/temp1_crit'];
        for each (let file in crit_files){
            if(GLib.file_test(file,1<<4)){
                let temperature = GLib.file_get_contents(file);
                if(temperature[0]) {
                    info['crit']= parseInt(temperature[1])/1000;
                }
            }
        }
        return info;
    },

    _findTemperatureFromSensorsOutput: function(txt){
        let sensors_output=txt.split("\n");
        let feature_label=undefined;
        let feature_value=undefined;
        let s= new Array();
        let n=0,c=0;
        let f;
        //iterate through each lines
        for(let i = 0; i < sensors_output.length; i++) {
            // ignore chipset driver name and 'Adapter:' line for now
            i+=2;
            // get every feature of the chip
            while(sensors_output[i]){
               // if it is not a continutation of a feature line
               if(sensors_output[i].indexOf(' ') != 0){
                  let feature = this._parseSensorsTemperatureLine(feature_label, feature_value);
                  if (feature) {
                      s[n++] = feature;
                      feature = undefined;
                  }
                  [feature_label, feature_value]=sensors_output[i].split(':');
               }
               else{
                  feature_value += sensors_output[i];
               }
               i++;
            }
        }
        let feature = this._parseSensorsTemperatureLine(feature_label, feature_value);
        if (feature) {
            s[n++] = feature;
            feature = undefined;
        }
        return s;
    },

    _parseSensorsTemperatureLine: function(label, value) {
        let s = undefined;
        if(label != undefined && value != undefined) {
            let curValue = value.trim().split('  ')[0];
            // does the current value look like a temperature unit (°C)?
            if(curValue.indexOf("C", curValue.length - "C".length) !== -1){
                s = new Array();
                s['label'] = label.trim();
                s['temp'] = parseFloat(curValue.split(' ')[0]);
                s['high'] = this._getHigh(value);
                s['crit'] = this._getCrit(value);
                s['hyst'] = this._getHyst(value);
            }
        }
        return s;
    },

    _findTemperatureFromHDDTempOutput: function(txt){
        let hddtemp_output=txt.split("\n");
        let s= new Array();
        let n=0;
        for(let i = 0; i < hddtemp_output.length; i++)
        {
            if(hddtemp_output[i]){
                s[++n] = new Array();
                s[n]['label'] = hddtemp_output[i].split(': ')[0].split('/');
                s[n]['label'] = s[n]['label'][s[n]['label'].length - 1];
                s[n]['temp'] = parseFloat(hddtemp_output[i].split(': ')[2]);
            }
        }
        return s;
    },

    _findTemperatureFromHDDTempDaemon: function(txt){
        let hddtemp_output=txt.split("\n");
        let s= new Array();
        let n=0;
        for(let i = 0; i < hddtemp_output.length; i++)
        {
            if(hddtemp_output[i]){
                s[++n] = new Array();
                s[n]['label'] = hddtemp_output[i].split('|')[1].split('/');
                s[n]['label'] = s[n]['label'][s[n]['label'].length - 1];
                s[n]['temp'] = parseFloat(hddtemp_output[i].split('|')[3]);
            }
        }
        return s;
    },

    _getHigh: function(t){
        let r;
        return (r=/high=\+(\d{1,3}.\d)/.exec(t))?parseFloat(r[1]):null;
    },

    _getCrit: function(t){
        let r;
        return (r=/crit=\+(\d{1,3}.\d)/.exec(t))?parseFloat(r[1]):null;
    },

    _getHyst: function(t){
        let r;
        return (r=/hyst=\+(\d{1,3}.\d)/.exec(t))?parseFloat(r[1]):null;
    },


    _toFahrenheit: function(c){
        return ((9/5)*c+32);
    },

    _formatTemp: function(t) {
        let ret = t;
        if (settings.get_string('unit')=='Fahrenheit'){
            ret = this._toFahrenheit(t);
        }
        ret = ret.toFixed(1);
        if (!settings.get_boolean('display-decimal-value'))
            ret = Math.round(ret);
        ret = ret.toString(); // no more mathematics
        if (settings.get_boolean('display-degree-sign'))
            ret += "\u00b0";
        if (settings.get_string('unit')=='Fahrenheit')
            ret += "F";
        else
            ret+= "C";

        return ret;
    }
}

function init(extensionMeta) {
    settings = Convenience.getSettings();
}

let indicator;
let event=null;

function enable() {
    indicator = new CpuTemperature();
    Main.panel.addToStatusArea('temperature', indicator);
    //TODO catch preference change signals with settings.connect('changed::
}

function disable() {
    indicator.destroy();
    Mainloop.source_remove(event);
    indicator = null;
}
