"use strict"

var fs = require("fs");

var _gl_ctx = null;
var _width = 1000;
var _height = 1000;

exports.context_to_file = context_to_file;
function context_to_file(gl, width, height, filename) {
  var filename = filename || __filename + '.ppm';
  var file = fs.createWriteStream(filename);

  // Write output
  var pixels = new Uint8Array(width * height * 4);
  gl.readPixels(0, 0, width, height, gl.RGBA, gl.UNSIGNED_BYTE, pixels);
  file.write(['P3\n# gl.ppm\n', width, ' ', height, '\n255\n'].join(''));
  for (var i = 0; i < pixels.length; i += 4) {
    file.write(pixels[i] + ' ' + pixels[i + 1] + ' ' + pixels[i + 2] + ' ')
  }
}
