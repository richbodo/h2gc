const St = imports.gi.St;
const Lang = imports.lang;
const PanelMenu = imports.ui.panelMenu;
const PopupMenu = imports.ui.popupMenu;
const Main = imports.ui.main;
const GLib = imports.gi.GLib;
const Util = imports.misc.util;
const Mainloop = imports.mainloop;
const Me = imports.misc.extensionUtils.getCurrentExtension();
const Convenience = Me.imports.convenience;
const Shell = imports.gi.Shell;

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

        item = new PopupMenu.PopupMenuItem("Learn");
        section.addMenuItem(item);
	item.connect('activate', Lang.bind(this, this._doLearn));

        item = new PopupMenu.PopupMenuItem("Collaborate");
        section.addMenuItem(item);
	item.connect('activate', Lang.bind(this, this._doCollaborate));

        item = new PopupMenu.PopupMenuItem(_("Contact A Guru"));
        section.addMenuItem(item);
	item.connect('activate', Lang.bind(this, this._doContactGuru));	

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
	// read from disk and display oneliner.teach file
	// the file should contain a single plain english sentence with no tech jargon 
	let oneliner_file = '/home/richbodo/.h2gc/status_oneliner.txt'
	if (GLib.file_test(oneliner_file,1<<4)) {
            let oneliner_object = GLib.file_get_contents(oneliner_file);
            if(oneliner_object[0]) {
		var oneliner_string = oneliner_object[1];
		global.log("oneliner_string: ");
		global.log(oneliner_string);
            }
	}
        return oneliner_string;    
    },

    _doLearn: function() {	
	global.log("In Learn About It");
	// open local web page
	// sensible-browser in debian-derived
	// xdg-open, x-www-browser in some others
	// since we are using gnome - gnome-open URL works as well
        return true;    
    },

    _doCollaborate: function() {	
	global.log("In Collaborate.");
	// open private chatroom
	//
        return true;    
    },

    _doContactGuru: function() {	
	global.log("In Contact a Guru.");
	// open default email application
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
	global.log("In findSystemStatusFromFile status file is : " + status_file);
	
        if (GLib.file_test(status_file,1<<4)) {
            let status_contents = GLib.file_get_contents(status_file);
	    if(status_contents[0]) {
		var status_lines = status_contents[1].toString().split("\n");
		var status_number = parseInt(status_lines[0]);
		global.log("status_lines: ");
		global.log(status_lines);
		global.log("status_number: ");
		global.log(status_number);
	    }
        }
	
	if (status_number >= 1) {
	    system_status_string += status_number.toString();
	} else {
	    system_status_string += "AWESOME";
	}
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
