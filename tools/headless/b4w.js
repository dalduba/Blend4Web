var is_nodejs = typeof window === "undefined";
//==============================================================================
//
//==============================================================================
if (is_nodejs) {
  global.is_nodejs = is_nodejs;

  var fs = require("fs");
  var vm = require("vm");
  // add browser's global variables
  require("./browserfy")

  var B4W_SRC_FOLDER = "../../";
  var B4W_SRC_FILES = [
    "src/b4w.js",
    "src/anchors.js",
    "src/animation.js",
    "src/armature.js",
    "src/assets.js",
    "src/batch.js",
    "src/boundings.js",
    "src/camera.js",
    "src/compat.js",
    "src/config.js",
    "src/constraints.js",
    "src/container.js",
    "src/controls.js",
    "src/curve.js",
    "src/data.js",
    "src/dds.js",
    "src/debug.js",
    "src/extensions.js",
    "src/geometry.js",
    "src/graph.js",
    "src/hud.js",
    "src/input.js",
    "src/ipc.js",
    "src/lights.js",
    "src/loader.js",
    "src/logic_nodes.js",
    "src/math.js",
    "src/nla.js",
    "src/nodemat.js",
    "src/objects.js",
    "src/obj_util.js",
    "src/particles.js",
    "src/physics.js",
    "src/prerender.js",
    "src/primitives.js",
    "src/print.js",
    "src/reformer.js",
    "src/renderer.js",
    "src/scenegraph.js",
    "src/scenes.js",
    "src/sfx.js",
    "src/shaders.js",
    "src/textures.js",
    "src/time.js",
    "src/transform.js",
    "src/tsr.js",
    "src/util.js",
    "src/version.js",
    "src/libs/gl-matrix2.js",
    "src/libs/gpp_parser.js",
    "src/libs/md5.js",
    "src/ext/anchors.js",
    "src/ext/animation.js",
    "src/ext/armature.js",
    "src/ext/assets.js",
    "src/ext/camera.js",
    "src/ext/config.js",
    "src/ext/constraints.js",
    "src/ext/container.js",
    "src/ext/controls.js",
    "src/ext/data.js",
    "src/ext/debug.js",
    "src/ext/geometry.js",
    "src/ext/hud.js",
    "src/ext/input.js",
    "src/ext/lights.js",
    "src/ext/logic_nodes.js",
    "src/ext/main.js",
    "src/ext/material.js",
    "src/ext/math.js",
    "src/ext/objects.js",
    "src/ext/particles.js",
    "src/ext/physics.js",
    "src/ext/rgb.js",
    "src/ext/scenes.js",
    "src/ext/sfx.js",
    "src/ext/textures.js",
    "src/ext/time.js",
    "src/ext/tsr.js",
    "src/ext/transform.js",
    "src/ext/util.js",
    "src/ext/version.js",
    "src/ext/nla.js",
    "src/addons/app.js",
    "src/addons/camera_anim.js",
    "src/addons/gyroscope.js",
    "src/addons/hmd.js",
    "src/addons/hmd_conf.js",
    "src/addons/mixer.js",
    "src/addons/mouse.js",
    "src/addons/npc_ai.js",
    "src/addons/preloader.js",
    "src/addons/screenshooter.js",
    "src/addons/gp_conf.js",
    "src/addons/storage.js"
  ];

  var includeInThisContext = function (path) {
    var code = fs.readFileSync(path);
    vm.runInThisContext(code, path);
  }.bind(this);

  for (var i = 0; i < B4W_SRC_FILES.length; ++i) {
    includeInThisContext(B4W_SRC_FOLDER + B4W_SRC_FILES[i]);
  }

  var b4w_require = b4w.require;
  b4w.require = function(name) {
    try {
      return b4w_require(name);
    } catch(e) {
      return require(name);
    }
  }
  module.exports = b4w;
} else {
    // TODO: add code for browser
}
