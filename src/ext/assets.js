"use strict";

/** 
 * Low-level resource loader. In order to load exported scenes, use the {@link module:data|data} module instead.
 * @module assets
 * @local Asset
 * @local AssetCallback
 * @local ProgressCallback
 * @local PackCallback
 */
b4w.module["assets"] = function(exports, require) {

var m_assets = require("__assets");

/**
 * Loading asset.
 * Asset has the following structure: [uri, type, filepath, optional_param],
 * where uri - asset identifier, type - asset type, filepath - 
 * path to resource (URL), optional_param - any param passed to {@link module:assets~AssetCallback|AssetCallback}
 * @typedef Asset
 * @type {Array}
 * @alias module:assets.Asset
 */

/**
 * Callback executed after a single asset is loaded.
 * @callback AssetCallback
 * @param {Data} data Loaded data
 * @param {String} uri Data asset ID
 * @param {Number} type Data type
 * @param {String} filepath Data filepath
 * @param {*} [optional_param] Optional parameter
 */

/**
 * Callback executed after the whole pack of assets is loaded.
 * @callback PackCallback
 */

/**
 * Callback for the progress of loading.
 * @callback ProgressCallback
 * @param {Number} value Loading percentage
 */

/**
 * Asset type: ArrayBuffer
 * @const module:assets.AT_ARRAYBUFFER
 */
exports.AT_ARRAYBUFFER   = m_assets.AT_ARRAYBUFFER;

/**
 * Asset type: JSON
 * @const module:assets.AT_JSON
 */
exports.AT_JSON          = m_assets.AT_JSON;

/**
 * Asset type: Text
 * @const module:assets.AT_TEXT
 */
exports.AT_TEXT          = m_assets.AT_TEXT;

/**
 * Asset type: AudioBuffer
 * @const module:assets.AT_AUDIOBUFFER
 */
exports.AT_AUDIOBUFFER   = m_assets.AT_AUDIOBUFFER;

/**
 * Asset type: HTMLImageElement
 * @const module:assets.AT_IMAGE_ELEMENT
 */
exports.AT_IMAGE_ELEMENT = m_assets.AT_IMAGE_ELEMENT;

/**
 * Asset type: HTMLAudioElement
 * @const module:assets.AT_AUDIO_ELEMENT
 */
exports.AT_AUDIO_ELEMENT = m_assets.AT_AUDIO_ELEMENT;

/**
 * Add the assets to the loading queue.
 * @method module:assets.enqueue
 * @param {Asset[]} assets_pack Array of the loading assets
 * @param {AssetCallback} [asset_cb] Callback executed after a single asset is loaded
 * @param {PackCallback} [pack_cb] Callback executed after the whole pack of assets is loaded
 * @param {ProgressCallback} [progress_cb] Callback for the progress of loading
 */
exports.enqueue = function(asset_pack, asset_cb, pack_cb) {
    m_assets.enqueue(asset_pack, asset_cb, pack_cb);
}

}

