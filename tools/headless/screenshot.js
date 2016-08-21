"use strict"

// =============================================================================
//                                  BEGIN COMMON
// =============================================================================
if (is_nodejs) {
  var b4w = require("./b4w");
  module.require = b4w.require;
}

// RENAME MODULE NAME
b4w.register("screenshot", function(exports) {
// =============================================================================
//                                   END COMMON
// =============================================================================

// NOTE: add your code here
});

var fs = require("fs");

var _gl_ctx = null;
var _width = 1000;
var _height = 1000;

function buffer_to_file(gl, width, height, filename) {
  var file = fs.createWriteStream(filename);

  // Write output
  var pixels = new Uint8Array(width * height * 4);
  gl.readPixels(0, 0, width, height, gl.RGBA, gl.UNSIGNED_BYTE, pixels);
  file.write(['P3\n# gl.ppm\n', width, ' ', height, '\n255\n'].join(''));
  for (var i = 0; i < pixels.length; i += 4) {
    file.write(pixels[i] + ' ' + pixels[i + 1] + ' ' + pixels[i + 2] + ' ')
  }
}

function write_to_file() {
  var filename = __filename + '.ppm';
  buffer_to_file(_gl_ctx, _width, _height, filename);
  setTimeout(write_to_file, 2000);
}
