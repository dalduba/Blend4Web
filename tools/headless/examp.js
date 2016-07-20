"use strict";
var require_orig = require
var fs = require('fs');
var vm = require('vm');
var includeInThisContext = function (path) {
    var code = fs.readFileSync(path);
    vm.runInThisContext(code, path);
}.bind(this);

var b4w_include = [
    "./../../src/b4w.js",
    "./../../src/anchors.js",
    "./../../src/batch.js",
    "./../../src/boundings.js",
    "./../../src/tsr.js",
    "./../../src/libs/gl-matrix2.js",
    "./../../src/util.js",
    "./../../src/math.js",
    "./../../src/data.js",
    "./../../src/print.js",
    "./../../src/extensions.js",
    "./../../src/geometry.js",
    "./../../src/graph.js",
    "./../../src/nodemat.js",
    "./../../src/debug.js",
    "./../../src/compat.js",
    "./../../src/textures.js",
    "./../../src/dds.js",
    "./../../src/time.js",
    "./../../src/renderer.js",
    "./../../src/camera.js",
    "./../../src/constraints.js",
    "./../../src/armature.js",
    "./../../src/container.js",
    "./../../src/hud.js",
    "./../../src/input.js",
    "./../../src/scenes.js",
    "./../../src/lights.js",
    "./../../src/objects.js",
    "./../../src/animation.js",
    "./../../src/obj_util.js",
    "./../../src/particles.js",
    "./../../src/physics.js",
    "./../../src/transform.js",
    "./../../src/sfx.js",
    "./../../src/version.js",
    "./../../src/reformer.js",
    "./../../src/curve.js",
    "./../../src/logic_nodes.js",
    "./../../src/nla.js",
    "./../../src/controls.js",
    "./../../src/assets.js",
    "./../../src/primitives.js",
    "./../../src/prerender.js",
    "./../../src/scenegraph.js",
    "./../../src/shaders.js",
    "./../../src/loader.js",
    "./../../src/libs/md5.js",
    "./../../src/ext/main.js",
    "./../../src/debug.js",
    "./../../src/libs/gpp_parser.js",
    "./../../uranium/build/uranium.js",
    "./../../src/ipc.js",
    "./../../src/config.js",
];
for (var i in b4w_include) {
    includeInThisContext(__dirname + "/" + b4w_include[i]);
}

b4w.register("__fs",  function(exports, require) {
    var m_fs = require_orig("fs")
    var m_process = require_orig("process")
    exports.readFileSync = m_fs.readFileSync
    exports.cwd = m_process.cwd
    exports.StringDecoder = require_orig('string_decoder').StringDecoder

});

b4w.register("fs",  function(exports, require) {
    var m_fs = require_orig("fs")
    for (var p in m_fs) {
        exports[p] = m_fs[p]
    }
});
b4w.register("path",  function(exports, require) {
    var m_fs = require_orig("path")
    for (var p in m_fs) {
        exports[p] = m_fs[p]
    }
});
b4w.register("worker",  function(exports, require) {
    exports.Worker = require_orig('webworker-threads').Worker
});

b4w.register("config",  function(exports, require) {
    var m_fs = require_orig("config")
    exports = m_fs.exports
});
b4w.register("__gl",  function(exports, require) {
    var m_gl = require_orig("gl")
    exports = m_gl.exports
});
b4w.register("__performance_now",  function(exports, require) {
    exports.now = require_orig("performance-now")
});
b4w.register("examp", function(exports, require) {

    var m_data = require("__data");
    var m_main  = require("main");
    var m_assets  = require("__assets");
    var m_debug = require("__debug");

    var createContext = require_orig('gl')
    var utils = require_orig('./common/utils')
    var utils_log = require_orig('./common/utils_log.js')
    var path = require_orig('path')
    var log = new utils_log.Log(path.basename(__filename), 'DEBUG')
    var _gl_ctx = null;
    var _width = 800
    var _height = 600

    var loaded = false;
    function load_json() {
        function write_to_file() {
            var filename = __filename + '.ppm' // eslint-disable-line
            log.info(__line, 'rendering ' + filename)

            utils.bufferToFile(_gl_ctx, _width, _height, filename)
            // m_main.pause()

            // gl.destroy()
        }
        function loaded_callback(data_id) {
            log.info(__line, "file loaded")
            loaded = true
            m_main.resume()
            setTimeout(m_main.resume, 5000)
            setTimeout(write_to_file, 10000)
        }
        function stage_load_callback(a,b) {
            log.info("stage_load_callback", a + " " + b)
        }
        log.info(__line, "start loading")
        m_data.load("headless/test.json",
            loaded_callback, stage_load_callback, true);
    }

    exports.main = function main() {

        load_json()

        // Create context
        _gl_ctx = createContext(_width, _height)
        var canvas = {}
        canvas.width = _width
        canvas.height = _height
        m_main.init_headless(canvas, _gl_ctx)
        function do_nothing() {
            console.log("do nothong")
            setTimeout(do_nothing, 1000)
        }
        do_nothing()
    }
})
b4w.require("examp").main();