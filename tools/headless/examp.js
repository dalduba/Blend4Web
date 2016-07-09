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
    "./../../src/config.js",
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
    "./../../src/ipc.js",
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
b4w.register("examp", function(exports, require) {

    var m_data = require("__data");
    var m_main  = require("main");
    var m_assets  = require("__assets");
    var m_debug = require("__debug");

    var createContext = require_orig('gl/index')
    var utils = require_orig('./common/utils')
    var utils_log = require_orig('./common/utils_log.js')
    var path = require_orig('path')
    var log = new utils_log.Log(path.basename(__filename), 'DEBUG')

    var loaded = false;
    function load_json() {
        function loaded_callback(data_id) {
            log.info(__line, "file loaded")
            loaded = true
        }
        function stage_load_callback(a,b) {
            log.info("stage_load_callback", a + " " + b)
        }
        log.info(__line, "start loading")
        m_data.load("../deploy/assets/tutorials/cartoon_room/cartoon_interior_all.json",
            loaded_callback, stage_load_callback, true);
    }

    exports.main = function main() {

        load_json()

        // Create context
        var width = 64
        var height = 64
        var gl = createContext(width, height)
        var canvas = {}
        canvas.width = width
        canvas.height = height
        m_main.init_headless(canvas, gl)
        //
        // var vertex_src = [
        //     'attribute vec2 a_position;',
        //     'void main() {',
        //     'gl_Position = vec4(a_position, 0, 1);',
        //     '}'
        // ].join('\n')
        //
        // var fragment_src = [
        //     'void main() {',
        //     'gl_FragColor = vec4(1, 0, 0, 1);  // green',
        //     '}'
        // ].join('\n')
        //
        // // setup a GLSL program
        // var program = utils.createProgramFromSources(gl, [vertex_src, fragment_src])
        //
        // if (!program) {
        //     return
        // }
        // gl.useProgram(program)
        //
        // // look up where the vertex data needs to go.
        // var positionLocation = gl.getAttribLocation(program, 'a_position')
        //
        // // Create a buffer and put a single clipspace rectangle in
        // // it (2 triangles)
        // var buffer = gl.createBuffer()
        // gl.bindBuffer(gl.ARRAY_BUFFER, buffer)
        // gl.bufferData(
        //     gl.ARRAY_BUFFER,
        //     new Float32Array([
        //         -1.0, -1.0,
        //         1.0, -1.0,
        //         -1.0, 1.0,
        //         -1.0, 1.0,
        //         1.0, -1.0,
        //         1.0, 1.0]),
        //     gl.STATIC_DRAW)
        // gl.enableVertexAttribArray(positionLocation)
        // gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0)

        // draw
        // gl.drawArrays(gl.TRIANGLES, 0, 6)

        //loading is not working yet => infinite loop
        var sleep = require_orig('sleep');
        while (!loaded) {
            sleep.sleep(1)
            log.info(__line, 'waiting')
        }

        var filename = __filename + '.ppm' // eslint-disable-line
        log.info(__line, 'rendering ' + filename)
        utils.bufferToFile(gl, width, height, filename)

        gl.destroy()
    }
})
b4w.require("examp").main();