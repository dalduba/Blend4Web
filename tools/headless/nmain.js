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

function bufferToFile (gl, width, height, filename) {
    var fs = require("fs")
    var file = fs.createWriteStream(filename)

          // Write output
            var pixels = new Uint8Array(width * height * 4)
          gl.readPixels(0, 0, width, height, gl.RGBA, gl.UNSIGNED_BYTE, pixels)
          file.write(['P3\n# gl.ppm\n', width, ' ', height, '\n255\n'].join(''))
          for (var i = 0; i < pixels.length; i += 4) {
            file.write(pixels[i] + ' ' + pixels[i + 1] + ' ' + pixels[i + 2] + ' ')
          }
    }
var _gl_ctx = null
var _width=800
var _height=600
function write_to_file() {
    var filename = __filename + '.ppm'
        bufferToFile(_gl_ctx, _width, _height, filename)
        setTimeout(write_to_file, 2000)
    }
/**
 * callback executed when the scene is loaded
 */
function load_cb(data_id) {
    // place your code here
    var main = require("main")
    var camera_anim = require("camera_anim")
    camera_anim.auto_rotate(1);
    _gl_ctx = main.get_context()

    setTimeout(write_to_file, 2000)
}

init();
