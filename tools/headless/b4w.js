//==============================================================================
//
//==============================================================================
if (typeof window === "undefined") {
    module.exports.register = function(module_name, func) {
        func();
    }

    exports.require = function(module_name) {
        module.require(module_name);
    }
} else {
    // TODO: add code for nodejs
}