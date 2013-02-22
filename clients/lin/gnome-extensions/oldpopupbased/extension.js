//
// testing icon manipulation in the gnome3 top panel
//
// status: Barely works - gnome-extensions are a PITA to develop 
//
// Modded version of the demo extension by fpmurphy.
//
// Maintained by richbodo@gmail.com - direct all questions to rich
//
// Copyright (c) 2012 Finnbarr P. Murphy.  All rights reserved.
//

const Lang = imports.lang;
const St = imports.gi.St;

const Main = imports.ui.main;
const PanelMenu = imports.ui.panelMenu;
const PopupMenu = imports.ui.popupMenu;
const GLib = imports.gi.GLib;

const DemoButton = new Lang.Class({
    Name: 'DemoButton',
    Extends: PanelMenu.Button,

    _init: function() {

	this.current_icon = "happyface"

        this._buttonIconHappy = new St.Icon({
            icon_name: 'happyface',
            icon_size: 22,
            reactive: true,
            track_hover: true,
            style_class: 'demobutton-icon' });

	this._buttonIconSad = new St.Icon({
            icon_name: 'sadface',
            icon_size: 22,
            reactive: true,
            track_hover: true,
            style_class: 'demobutton-icon' });

        let menuAlignment = 0.5;
        this.parent(menuAlignment);
 
        let topLayout = new St.BoxLayout();
        topLayout.add_actor(this._buttonIconHappy);
        this.actor.add_actor(topLayout);
        this._topLayout = topLayout;
 
        this.litem = new PopupMenu.PopupMenuItem("Learn!");
        this.menu.addMenuItem(this.litem);
	this.litem.connect('activate', Lang.bind(this, this._doLearnAboutIt));
	
        this.citem = new PopupMenu.PopupMenuItem("Collaborate!");
        this.menu.addMenuItem(this.citem);
	this.citem.connect('activate', Lang.bind(this, this._doCollaborate));

        this.gitem = new PopupMenu.PopupMenuItem("Get help!");
        this.menu.addMenuItem(this.gitem);
	this.gitem.connect('activate', Lang.bind(this, this._doGetHelp));

        Main.panel.menuManager.addMenu(this.menu);

        // update status every 10 seconds
        event = GLib.timeout_add_seconds(0, 10, Lang.bind(this, function () {
            this._update_icon();
            return true;
        }));

    },

    _update_icon: function() {	
	global.log("In update_icon");
	
        // found some potential GLib stuff here: http://www.roojs.org/seed/gir-1.2-gtk-3.0/gjs/GLib.FileTest.html
	let status_file="/home/richbodo/test";
	if (GLib.file_test(status_file,1<<4)) {
            let status = GLib.file_get_contents(status_file);
            if(status[0]) {
		overall_status = parseInt(status[1]);
		global.log("status 1: ");
		global.log(status[1]);
		global.log("overall_status: ");
		global.log(overall_status);
		global.log("current_icon: ");
		global.log(this.current_icon);
	
            }
	}

	// this doesn't work
	//
	// if (this.currenticon == "happyface") {
	//     this._topLayout.add_actor(this._buttonIconSad);
	//     this._topLayout.remove_actor(this._buttonIconHappy);
	//     this.currenticon == "sadface";
	// }
	// else {
	//     this._topLayout.add_actor(this._buttonIconHappy);
	//     this._topLayout.remove_actor(this._buttonIconSad);
	//     this.currenticon == "happyface";
	// }
	
	// this works, but throws an exception
	// try changing the icon name does same thing
	// spent umpteen hours with the symbolic icon method. giving up.
	this._topLayout.add_actor(this._buttonIconSad);
	this._topLayout.remove_actor(this._buttonIconHappy);
        return true;    
    },

    _doLearnAboutIt: function() {	
	global.log("In Learn About It");
        return true;    
    },

    _doCollaborate: function() {	
	global.log("In Collaborate.");
        return true;    
    },

    _doGetHelp: function() {	
	global.log("In Get help.");
        return true;    
    },

    enable: function() {
        Main.panel._centerBox.insert_child_at_index(this.container, 1);
        this.container.show();
    },

    disable: function() {
        this.container.hide();
    },
});


function init() {
    return new DemoButton();
}
