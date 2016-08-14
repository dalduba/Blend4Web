"use strict"

// =============================================================================
//                                  BEGIN COMMON
// =============================================================================
if (typeof window === "undefined") {
  var b4w = require("./b4w");
  module.require = b4w.require;
}

// RENAME MODULE NAME
b4w.register("nmain", function(exports) {
// =============================================================================
//                                   END COMMON
// =============================================================================

// NOTE: add your code here
});

// import modules used by the app
var m_app       = require("app");
var m_data      = require("data");

/**
 * export the method to initialize the app (called at the bottom of this file)
 */
var init = function() {
    m_app.init({
        canvas_container_id: "main_canvas_container",
        callback: init_cb,
        // show_fps: true,
        console_verbose: true,
        physics_enabled: false,
        // physics_uranium_path: "../../deploy/apps/common/uranium.js",
        // autoresize: true
    });
}

/**
 * callback executed when the app is initialized
 */
function init_cb(canvas_elem, success) {

    if (!success) {
        console.log("b4w init failure");
        return;
    }

    load();
}

/**
 * load the scene data
 */
function load() {
    m_data.load("../apps_dev/nodejs/nodejs.json", load_cb);
}

/**
 * callback executed when the scene is loaded
 */
function load_cb(data_id) {
    // place your code here

}

init();
