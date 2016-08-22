"use strict"

if (typeof is_nodejs === "undefined")
  global.is_nodejs = typeof window === "undefined";

if (is_nodejs) {
  const m_fs = require("fs");
  const m_vm = require("vm");

  const B4W_SRC_FOLDER = "../../";
  const B4W_SRC_FILES = [
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

  const b4w_context = m_vm.createContext({
    require: require,
    setTimeout: setTimeout,
    console: console,
    process: process
  });

  // add browser's global variables
  const browserfy_code = m_fs.readFileSync("./browserfy.js");
  m_vm.runInContext(browserfy_code, b4w_context);

  for (var i = 0; i < B4W_SRC_FILES.length; ++i) {
    const b4w_module_path = B4W_SRC_FOLDER + B4W_SRC_FILES[i];
    const code = m_fs.readFileSync(b4w_module_path);
    m_vm.runInContext(code, b4w_context);
  }

  module.exports = b4w_context.b4w;
} else {
  // TODO: add code for browser
}
