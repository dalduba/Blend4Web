//==============================================================================
// DUMMY BROWSERFY
//==============================================================================
var m_gl = require("gl");
var m_fs = require("fs");
var m_pr = require("process");
var m_str = require('string_decoder');
var m_work = require("webworker-threads");
global.Worker = m_work.Worker;

var style = {
  height: 1000,
  width: 1000,
  left: 0,
  top: 0,
  position: "absolute",
  display: "block"
};

var element = {
  style: style,

  parentNode: null,

  // TODO: add logic
  appendChild: function(){},
  removeChild: function(){},

  addEventListener: function(){},
  removeEventListener: function(){},

  getContext: function(name, cfg_ctx){
    var ctx = m_gl(1000, 1000, cfg_ctx);
    return ctx;
  },
  getBoundingClientRect: function(){
    return {
      bottom : 1000,
      heigh  : 1000,
      left   : 0,
      right  : 1000,
      top    : 0,
      width  : 1000,
      x      : 0,
      y      : 0
    }
  },

  offsetWidth: 1000,
  offsetHeight: 1000,
  clientWidth: 1000,
  clientHeight: 1000
};
element.parentNode = element;


var document = {
  documentElement: element,
  body: element,
  head: element,
  location: {href: ""},

  // TODO: add logic
  addEventListener: function(){},
  removeEventListener: function(){},

  createElement: function(){return element},
  getElementById: function(){return element},

  getElementsByTagName: function(){return [];},


  // TODO: make configurable
  readyState: "complete",
  hidden: false,
  // fullscreenElement: null,
  // pointerLockElement: null,
};
global.document = document;


var screen = {
  height: 1000,
  width: 1000
};

global.window = {
  document: document,
  screen: screen,
  localStorage: {},

  // WTF is this?
  // TODO: check
  WebGLRenderingContext: true,

  setTimeout: setTimeout,

  // TODO: add logic
  addEventListener: function(){},
  removeEventListener: function(){},

  // TODO: make configurable
  URL: "",
  devicePixelRatio: 1,
  innerHeight: 1000,
  orientation: 0
};

global.performance = {
  now: function() {
    var now = process.hrtime();
    return now[0]*1000 + now[1] / 1000000;
  },
}

global.navigator = {
  userAgent: "",
}

global.XMLHttpRequest = function() {
  var req = {
    _source_url: null,
    _parse_response: function(source) {
      switch(req.responseType) {
      case "json":
      case "text":
        var decoder = new m_str.StringDecoder('utf8');
        return decoder.write(source)
      case "arraybuffer":
        var bin_str = source;
        return new Uint8Array(source).buffer
      default:
        return source;
      }
    },

    status: 0,
    readyState: 0,
    response: "",
    responseType: "",
    onreadystatechange: null,

    overrideMimeType: function() {},
    addEventListener: function() {},
    open: function(method, url, async) {
      req._source_url = url;
      req.readyState = 1;
    },
    send: function() {
      req.status = 404;
      req.readyState = 4;

      req.status = 200;

      var file_data = m_fs.readFileSync("../"+req._source_url.split("?")[0])
      req.response = req._parse_response(file_data);

      var get_type = {};
      if (get_type.toString.call(req.onreadystatechange)
          === '[object Function]')
          req.onreadystatechange();
    }
  }
  return req;
}
