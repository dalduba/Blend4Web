"use strict"

// =============================================================================
//                                  BEGIN COMMON
// =============================================================================
if (typeof window === "undefined") {
    var b4w = require("./b4w");
}

// RENAME MODULE NAME
b4w.register("nmain", function(exports, require) {

if (typeof window === "undefined") {
    exports = module.exports;
    require = function(name) {
        return module.require("./" + name);
    }
}
// =============================================================================
//                                   END COMMON
// =============================================================================

// NOTE: add your code here

});