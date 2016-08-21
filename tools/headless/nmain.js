"use strict"

// =============================================================================
//                                  DECLARE NODEJS MODULES
// =============================================================================
if (typeof window === "undefined") {
  var b4w = require("./b4w");
  var m_screenshot = require("./screenshot");
}

// =============================================================================
//                                  DECLARE BLEND4WEB MODULES
// =============================================================================
b4w.module["nmain"] = function(exports, require) {
  var m_app = require("app");
  var m_data = require("data");
  var m_main = require("main");

  exports.init = init;
  function init() {
    m_app.init({
      canvas_container_id: "main_canvas_container",
      callback: init_cb,
      console_verbose: true,

      // used by physic
      // prevent_caching: false,
      physics_enabled: false,
      // physics_uranium_path: "../../deploy/apps/common/uranium.js",
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
    // var camera_anim = require("camera_anim");
    // camera_anim.auto_rotate(1);

    var ctx = m_main.get_context();

    setInterval(function() {
      m_screenshot.context_to_file(ctx, 1000, 1000);
    }, 2000);
  }
};

b4w.require("nmain").init()
