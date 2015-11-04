/**
 * Copyright (C) 2014-2015 Triumph LLC
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

"use strict";

/** 
 * Camera API.
 * All functions require a valid camera object reference. Use get_object_by_name() or
 * get_active_camera() from {@link module:scenes} to obtain it.
 * @module camera
 */
b4w.module["camera"] = function(exports, require) {

var m_cam      = require("__camera");
var m_cfg      = require("__config");
var m_cons     = require("__constraints");
var m_cont     = require("__container");
var m_mat3     = require("__mat3");
var m_mat4     = require("__mat4");
var m_obj_util = require("__obj_util");
var m_phy      = require("__physics");
var m_print    = require("__print");
var m_trans    = require("__transform");
var m_util     = require("__util");
var m_vec3     = require("__vec3");
var m_vec4     = require("__vec4");

var cfg_ctl = m_cfg.controls;

var _vec2_tmp = new Float32Array(2);
var _vec3_tmp = new Float32Array(3);
var _vec3_tmp2 = new Float32Array(3);
var _vec4_tmp = new Float32Array(4);
var _mat3_tmp = new Float32Array(9);

/**
 * The camera's movement style: static (non-interactive).
 * @const {CameraMoveStyle} module:camera.MS_STATIC
 */
exports.MS_STATIC = m_cam.MS_STATIC;
/**
 * The camera's movement style: animated.
 * @const {CameraMoveStyle} module:camera.MS_ANIMATION
 * @deprecated use {@link module:camera.MS_STATIC|camera.MS_STATIC} instead.
 */
exports.MS_ANIMATION = m_cam.MS_STATIC;
/**
 * The camera's movement style: target.
 * @const {CameraMoveStyle} module:camera.MS_TARGET_CONTROLS
 */
exports.MS_TARGET_CONTROLS = m_cam.MS_TARGET_CONTROLS;
/**
 * The camera's movement style: eye.
 * @const {CameraMoveStyle} module:camera.MS_EYE_CONTROLS
 */
exports.MS_EYE_CONTROLS = m_cam.MS_EYE_CONTROLS;
/**
 * The camera's movement style: hover.
 * @const {CameraMoveStyle} module:camera.MS_HOVER_CONTROLS
 */
exports.MS_HOVER_CONTROLS = m_cam.MS_HOVER_CONTROLS;

/**
 * Check if the object is a camera.
 * @method module:camera.is_camera
 * @param {Object3D} obj Object 3D
 * @returns {Boolean} Checking result.
 * @deprecated use {@link module:objects.is_camera|objects.is_camera} instead.
 */
exports.is_camera = function(obj) {
    m_print.error("camera.is_camera() deprecated, use objects.is_camera() instead");
    return m_obj_util.is_camera(obj);
}

/**
 * Check if the object is a camera and has the MS_TARGET_CONTROLS movement style.
 * @method module:camera.is_target_camera
 * @param {Object3D} obj Object 3D
 * @returns {Boolean} Checking result.
 */
exports.is_target_camera = m_cam.is_target_camera;

/**
 * Check if the object is a camera and has the MS_EYE_CONTROLS movement style.
 * @method module:camera.is_eye_camera
 * @param {Object3D} obj Object 3D
 * @returns {Boolean} Checking result.
 */
exports.is_eye_camera = m_cam.is_eye_camera;

/**
 * Check if the object is a camera and has the MS_HOVER_CONTROLS movement style.
 * @method module:camera.is_hover_camera
 * @param {Object3D} obj Object 3D
 * @returns {Boolean} Checking result.
 */
exports.is_hover_camera = m_cam.is_hover_camera;

/**
 * Set the movement style (MS_*) for the camera.
 * @method module:camera.set_move_style
 * @param {Object3D} camobj Camera object
 * @param {CameraMoveStyle} move_style Camera movement style
 * @returns {Boolean} Operation success flag.
 */
exports.set_move_style = function(camobj, move_style) {
    if (!m_obj_util.is_camera(camobj)) {
        m_print.error("set_move_style(): Wrong object");
        return false;
    }

    if (move_style != m_cam.MS_STATIC && move_style != m_cam.MS_EYE_CONTROLS 
            && move_style != m_cam.MS_HOVER_CONTROLS 
            && move_style != m_cam.MS_TARGET_CONTROLS) {
        m_print.error("set_move_style(): Wrong camera move style");
        return false;
    }

    return m_cam.set_move_style(camobj, move_style);
}
/**
 * Get the movement style of the camera.
 * @method module:camera.get_move_style
 * @param {Object3D} camobj Camera object
 * @returns {?CameraMoveStyle} Camera movement style.
 */
exports.get_move_style = function(camobj) {
    if (!m_obj_util.is_camera(camobj)) {
        m_print.error("get_move_style(): Wrong object");
        return null;
    }

    return m_cam.get_move_style(camobj);
}

/**
 * Set the velocity parameters for the camera.
 * @method module:camera.set_velocity_params
 * @param {Object3D} camobj Camera object
 * @param {Vec3} velocity Camera velocity params (velocity_trans, velocity_rot, velocity_zoom)
 */
exports.set_velocity_params = function(camobj, velocity) {
    if (!m_cam.is_target_camera(camobj)
            && !m_cam.is_eye_camera(camobj)
            && !m_cam.is_hover_camera(camobj)) {
        m_print.error("set_velocity_params(): Wrong object or camera move style");
        return;
    }

    var render = camobj.render;

    render.velocity_trans = m_util.clamp(velocity[0], 0, Infinity);
    render.velocity_rot = m_util.clamp(velocity[1], 0, Infinity);
    render.velocity_zoom = m_util.clamp(velocity[2], 0, 1);
}
/**
 * Get the velocity parameters of the camera.
 * @method module:camera.get_velocity_params
 * @param {Object3D} camobj Camera object
 * @param {Vec3} [dest=vec3.create()] Velocity params [velocity_trans, velocity_rot,
 * velocity_zoom].
 * @returns {?Vec3} Velocity params [velocity_trans, velocity_rot, 
 * velocity_zoom].
 */
exports.get_velocity_params = function(camobj, dest) {
    if (!m_cam.is_target_camera(camobj)
            && !m_cam.is_eye_camera(camobj)
            && !m_cam.is_hover_camera(camobj)) {
        m_print.error("get_velocity_params(): Wrong object or camera move style");
        return null;
    }

    if (!dest) {
        dest = new Float32Array(3);
    }

    var render = camobj.render;

    dest[0] = render.velocity_trans;
    dest[1] = render.velocity_rot;
    dest[2] = render.velocity_zoom;

    return dest;
}

/**
 * Low-level method to set position of the STATIC/EYE camera.
 * @method module:camera.set_look_at
 * @param {Object3D} camobj Camera object
 * @param {Vec3} eye Eye point (position of the camera)
 * @param {Vec3} target Target point (point the camera is looking at)
 * @param {Vec3} [up=util.AXIS_Y] Up vector ("up" direction of the camera)
 */
exports.set_look_at = function(camobj, eye, target, up) {
    up = up || m_util.AXIS_Y;
    m_cam.set_look_at(camobj, eye, target, up);
};

/**
 * Get the eye point (position) of the camera.
 * @method module:camera.get_eye
 * @param {Object3D} camobj Camera object
 * @param {Vec3} [dest=vec3.create()] Destination eye vector.
 * @returns {?Vec3} Destination eye vector.
 */
exports.get_eye = get_eye;
function get_eye(camobj, dest) {
    if (!m_obj_util.is_camera(camobj)) {
        m_print.error("get_eye(): Wrong object");
        return null;
    }
    
    return m_cam.get_eye(camobj, dest);
}

exports.set_pivot = set_pivot;
/**
 * Set the pivot point for the TARGET camera.
 * @method module:camera.set_pivot
 * @param {Object3D} camobj Camera object
 * @param {Vec3} coords New pivot vector.
 */
function set_pivot(camobj, coords) {
    if (!m_cam.is_target_camera(camobj)) {
        m_print.error("set_pivot(): Wrong object or camera move style");
        return;
    }

    m_vec3.copy(coords, camobj.render.pivot);
    m_trans.update_transform(camobj);
    m_phy.sync_transform(camobj);
}

exports.set_trans_pivot = set_trans_pivot;
/**
 * Set the translation and the pivot point for the TARGET camera.
 * @method module:camera.set_trans_pivot
 * @param {Object3D} camobj Camera Object 3D
 * @param {Vec3} trans Translation vector
 * @param {Vec3} pivot Pivot vector
 */
function set_trans_pivot(camobj, trans, pivot) {
    if (!m_cam.is_target_camera(camobj)) {
        m_print.error("set_trans_pivot(): Wrong object or camera move style");
        return;
    }

    m_cam.set_trans_pivot(camobj, trans, pivot);
}

/**
 * Get the pivot point of the camera.
 * @method module:camera.get_pivot
 * @param {Object3D} camobj Camera object
 * @param {Vec3} [dest] Destination pivot vector.
 * @returns {?Vec3} Destination pivot vector.
 */
exports.get_pivot = function(camobj, dest) {
    if (!m_cam.is_target_camera(camobj)) {
        m_print.error("get_pivot(): Wrong object or camera move style");
        return null;
    }

    if (!dest)
        var dest = new Float32Array(3);

    var render = camobj.render;

    m_vec3.copy(render.pivot, dest);
    return dest;
}

/**
 * Rotate the TARGET camera around the pivot point.
 * @method module:camera.rotate_pivot
 * @param {Object3D} camobj Camera object
 * @param {Number} delta_phi Azimuth angle in radians
 * @param {Number} delta_theta Elevation angle in radians
 * @deprecated use {@link module:camera.rotate_camera|camera.rotate_camera} or {@link module:camera.rotate_target_camera|camera.rotate_target_camera} instead.
 */
exports.rotate_pivot = function(camobj, delta_phi, delta_theta) {
    m_print.error("rotate_pivot() deprecated, use rotate_camera() or rotate_target_camera() instead");
    exports.rotate_target_camera(camobj, delta_phi, delta_theta);
}

/**
 * Translate the pivot point of the TARGET camera.
 * +h from left to right
 * +v from down to up
 * @method module:camera.move_pivot
 * @param {Object3D} camobj Camera object
 * @param {Number} trans_h_delta Delta of the horizontal translation
 * @param {Number} trans_v_delta Delta of the vertical translation
 */
exports.move_pivot = function(camobj, trans_h_delta, trans_v_delta) {

    if (!m_cam.is_target_camera(camobj)) {
        m_print.error("move_pivot(): wrong object");
        return;
    }

    var render = camobj.render;
    
    if (render.use_panning) {
        var mat = m_mat3.fromMat4(render.world_matrix, _mat3_tmp);

        var trans_vector = _vec3_tmp;

        var dist_vector = m_vec3.subtract(render.trans, render.pivot, _vec3_tmp2);

        trans_vector[0] = trans_h_delta;
        trans_vector[1] = 0;
        trans_vector[2] = trans_v_delta;

        m_vec3.scale(trans_vector, m_vec3.len(dist_vector), trans_vector);
        m_vec3.transformMat3(trans_vector, mat, trans_vector);
        m_vec3.add(render.pivot, trans_vector, render.pivot);
        m_vec3.add(render.trans, trans_vector, render.trans);

        m_trans.update_transform(camobj);
        m_phy.sync_transform(camobj);
    }
}

/**
 * Rotate the HOVER camera around the hover pivot point.
 * @method module:camera.rotate_hover_cam
 * @param {Object3D} camobj Camera object
 * @param {Number} angle Horizontal angle in radians
 * @deprecated Use {@link module:camera.rotate_camera|camera.rotate_camera} or {@link module:camera.rotate_hover_camera|camera.rotate_hover_camera} instead.
 */
exports.rotate_hover_cam = function(camobj, angle) {
    m_print.error("rotate_hover_cam() deprecated, use rotate_camera() or rotate_hover_camera() instead");
    exports.rotate_hover_camera(camobj, angle, 0);
}

/**
 * Get the angle of the HOVER camera.
 * @method module:camera.get_hover_cam_angle
 * @param {Object3D} camobj Camera object
 * @returns {?Number} An angle of the hover camera
 * @deprecated Use {@link module:camera.get_camera_angles|camera.get_camera_angles} instead.
 */
exports.get_hover_cam_angle = function(camobj) {
    m_print.error("get_hover_cam_angle() deprecated, use get_camera_angles() instead");
    if (!m_cam.is_hover_camera(camobj)) {
        m_print.error("get_hover_cam_angle(): wrong object or camera move style");
        return null;
    }

    return -m_cam.get_camera_angles(camobj, _vec2_tmp)[1];
}

/**
 * Set the angle for the HOVER camera.
 * @method module:camera.set_hover_cam_angle
 * @param {Object3D} camobj Camera object
 * @param {Number} angle Angle between the view and the horizontal plane
 * @deprecated Use {@link module:camera.rotate_camera|camera.rotate_camera} or {@link module:camera.rotate_hover_camera|camera.rotate_hover_camera} instead.
 */
exports.set_hover_cam_angle = function(camobj, angle) {
    m_print.error("set_hover_cam_angle() deprecated, use rotate_camera() or rotate_hover_camera() instead");

    if (!m_cam.is_hover_camera(camobj)) {
        m_print.error("set_hover_cam_angle(): wrong object or camera move style");
        return;
    }
    var render = camobj.render;

    if (!render.use_distance_limits) {
        m_print.error("set_hover_cam_angle(): distance/hover_angle limits are not defined or disabled");
        return;
    }

    var angles = m_cam.get_camera_angles(camobj, _vec2_tmp);
    // NOTE: prepare hover angle (CCW style)
    var angle_ccw = -angle;
    var rot_angle = angle_ccw - angles[1];

    if (rot_angle)
        m_cam.rotate_hover_camera(camobj, 0, rot_angle);

    m_trans.update_transform(camobj);
    m_phy.sync_transform(camobj);
}

/**
 * Get the hover angle limits for the HOVER camera, converted to the [-PI, PI] range.
 * @see https://www.blend4web.com/doc/en/camera.html#api
 * @method module:camera.get_hover_angle_limits
 * @param {Object3D} camobj Camera object
 * @param {Vec2} [angles] Destination vector [hover_angle_limits.down, hover_angle_limits.up].
 * @returns {?Vec2} Destination vector [hover_angle_limits.down, hover_angle_limits.up].
 */
exports.get_hover_angle_limits = function(camobj, angles) {
    if (!m_cam.is_hover_camera(camobj)) {
        m_print.error("get_hover_angle_limits(): wrong object");
        return null;
    }

    if(camobj.render.hover_angle_limits) {
        if (!angles)
            angles = new Float32Array(2);

        angles[0] = camobj.render.hover_angle_limits.down;
        angles[1] = camobj.render.hover_angle_limits.up;
    } else 
        m_print.error("get_hover_angle_limits(): camera hasn't angle limits");

    return angles;
}

/**
 * Get the distance limits of the TARGET/HOVER camera.
 * @method module:camera.get_cam_dist_limits
 * @param {Object3D} camobj Camera object
 * @param {Vec2} [dist] Array of distance limits [distance_max, distance_min].
 * @returns {?Vec2} Array of distance limits [distance_max, distance_min].
 */
exports.get_cam_dist_limits = function(camobj, dist) {
    if (!m_cam.is_hover_camera(camobj) && !m_cam.is_target_camera(camobj)) {
        m_print.error("get_cam_dist_limits(): wrong object");
        return null;
    }

    if (camobj.render.use_distance_limits) {
        if (!dist)
            dist = new Float32Array(2);

        dist[0] = camobj.render.distance_max;
        dist[1] = camobj.render.distance_min;
    } else 
        m_print.error("get_cam_dist_limits(): camera hasn't distance limits");
        
    return dist;
}

/**
 * Translate the HOVER camera.
 * @method module:camera.translate_hover_cam_v
 * @param {Object3D} camobj Camera object
 * @param {Vec3} trans Translation vector
 * @deprecated Use {@link module:camera.hover_cam_set_translation|camera.hover_cam_set_translation} instead.
 */
exports.translate_hover_cam_v = function(camobj, trans) {
    m_print.error("translate_hover_cam_v() deprecated, use hover_cam_set_translation() instead");
    exports.hover_cam_set_translation(camobj, trans);
}

/**
 * Set translation for the HOVER camera.
 * @method module:camera.hover_cam_set_translation
 * @param {Object3D} camobj Camera object
 * @param {Vec3} trans Translation vector.
 */
exports.hover_cam_set_translation = function(camobj, trans) {
    if (!m_cam.is_hover_camera(camobj)) {
        m_print.error("hover_cam_set_translation(): wrong object");
        return;
    }

    var render = camobj.render;
    if (render.use_distance_limits) {
        var trans_delta = m_vec3.subtract(trans, render.trans, _vec3_tmp);
        m_vec3.add(trans_delta, render.hover_pivot, render.hover_pivot);
    } 
    m_trans.set_translation(camobj, trans);
    
    m_trans.update_transform(camobj);
    m_phy.sync_transform(camobj);   
}

exports.set_hover_pivot = set_hover_pivot;
/**
 * Set the pivot point for the HOVER camera.
 * @method module:camera.set_hover_pivot
 * @param {Object3D} camobj Camera object
 * @param {Vec3} coords Pivot vector
 */
function set_hover_pivot(camobj, coords) {
    if (!m_cam.is_hover_camera(camobj)) {
        m_print.error("set_hover_pivot(): Wrong object or camera move style");
        return;
    }

    m_cam.set_hover_pivot(camobj, coords);
}

/**
 * Get the pivot translation of the HOVER camera.
 * @method module:camera.get_hover_cam_pivot
 * @param {Object3D} camobj Camera object
 * @param {Vec3} [dest=vec3.create()] Destination translation pivot vector.
 * @returns {?Vec3} Destination translation pivot vector.
 */
exports.get_hover_cam_pivot = function(camobj, dest) {
    if (!m_cam.is_hover_camera(camobj)) {
        m_print.error("get_hover_cam_pivot(): wrong object");
        return null;
    }

    if (!dest)
        dest = new Float32Array(3);

    m_vec3.copy(camobj.render.hover_pivot, dest);

    return dest;
}

/**
 * Check whether the camera has its distance limited.
 * @method module:camera.has_distance_limits
 * @param {Object3D} camobj Camera object.
 * @returns {?Boolean} True if the camera has distance limits.
 */
exports.has_distance_limits = function(camobj) {
    if (!m_cam.is_target_camera(camobj)
            && !m_cam.is_hover_camera(camobj)) {
        m_print.error("has_distance_limits(): wrong object");
        return null;
    }
    return camobj.render.use_distance_limits;
}

/**
 * Set the vertical angle limits for the TARGET/EYE camera, or the vertical (Z axis)
 * translation limits for the HOVER camera.
 * @see https://www.blend4web.com/doc/en/camera.html#api
 * @method module:camera.apply_vertical_limits
 * @param {Object3D} camobj Camera object
 * @param {Number} down_value Vertical down limit
 * @param {Number} up_value Vertical up limit
 * @param {Space} [space=transform.SPACE_WORLD] Space to make clamping relative to (actual for the TARGET/EYE camera)
 */
exports.apply_vertical_limits = function(camobj, down_value, up_value, space) {

    var ms = m_cam.get_move_style(camobj);
    switch (ms) {
    case m_cam.MS_TARGET_CONTROLS:
    case m_cam.MS_EYE_CONTROLS:
        space = space | m_trans.SPACE_WORLD;
        break;
    case m_cam.MS_HOVER_CONTROLS:
        if (down_value > up_value) {
            m_print.error("apply_vertical_limits(): wrong vertical limits");
            return;
        }
        break;
    default:
        m_print.error("apply_vertical_limits(): wrong object");
        return;
        break;
    }

    var render = camobj.render;
    render.vertical_limits = {
        down: down_value,
        up: up_value
    };
    m_cam.prepare_vertical_limits(camobj, space == m_trans.SPACE_LOCAL);

    m_trans.update_transform(camobj);
    m_phy.sync_transform(camobj);
}

/**
 * Remove the vertical clamping limits from the TARGET/EYE/HOVER camera.
 * @method module:camera.clear_vertical_limits
 * @param {Object3D} camobj Camera object
 */
exports.clear_vertical_limits = function(camobj) {
    var render = camobj.render;
    render.vertical_limits = null;
}

/**
 * Get the vertical angle limits of the TARGET/EYE camera (converted to the [-PI, PI] range), or
 * the vertical translation limits of the HOVER camera.
 * @see https://www.blend4web.com/doc/en/camera.html#api
 * @method module:camera.get_vertical_limits
 * @param {Object3D} camobj Camera Object 3D
 * @param {Vec2} [dest] Destination vector for the camera limits: [down, up] rotation or [Min, Max] translation limits.
 * @returns {?Vec2} Destination vector for the camera limits: [down, up] rotation or [Min, Max] translation limits.
 */
exports.get_vertical_limits = function(camobj, dest) {
    if (!m_cam.is_target_camera(camobj)
            && !m_cam.is_eye_camera(camobj)
            && !m_cam.is_hover_camera(camobj)) {
        m_print.error("get_vertical_limits(): wrong object");
        return null;
    }
    var render = camobj.render;

    dest = dest || new Float32Array(2);
    if (render.vertical_limits) {
        dest[0] = render.vertical_limits.down;
        dest[1] = render.vertical_limits.up;
        return dest;
    }
    return null;
}

 /**
 * Check whether the camera has any vertical limits.
 * @method module:camera.has_vertical_limits
 * @param {Object3D} camobj Camera Object 3D
 * @returns {?Boolean} True if the camera has vertical limits.
 */
exports.has_vertical_limits = function(camobj) {
    if (!m_cam.is_target_camera(camobj)
            && !m_cam.is_eye_camera(camobj)
            && !m_cam.is_hover_camera(camobj)) {
        m_print.error("has_vertical_limits(): wrong object");
        return null;
    }

    return Boolean(camobj.render.vertical_limits);
}

/**
 * Set the horizontal angle limits for the TARGET/EYE camera, or the horizontal (X axis)
 * translation limits for the HOVER camera.
 * @see https://www.blend4web.com/doc/en/camera.html#api
 * @method module:camera.apply_horizontal_limits
 * @param {Object3D} camobj Camera object
 * @param {Number} left_value Horizontal left limit
 * @param {Number} right_value Horizontal right limit
 * @param {Space} [space=transform.SPACE_WORLD] Space to make clamping relative to (actual for the TARGET/EYE camera)
 */
exports.apply_horizontal_limits = function(camobj, left_value, right_value,
        space) {

    var ms = m_cam.get_move_style(camobj);
    switch (ms) {
    case m_cam.MS_TARGET_CONTROLS:
    case m_cam.MS_EYE_CONTROLS:
        space = space | m_trans.SPACE_WORLD;
        break;
    case m_cam.MS_HOVER_CONTROLS:
        if (left_value > right_value) {
            m_print.error("apply_horizontal_limits(): wrong horizontal limits");
            return;
        }
        break;
    default:
        m_print.error("apply_horizontal_limits(): wrong object");
        return;
        break;
    }

    camobj.render.horizontal_limits = {
        left: left_value,
        right: right_value
    };
    m_cam.prepare_horizontal_limits(camobj, space == m_trans.SPACE_LOCAL);

    m_trans.update_transform(camobj);
    m_phy.sync_transform(camobj);
}

/**
 * Remove the horizontal clamping limits from the TARGET/EYE/HOVER camera.
 * @method module:camera.clear_horizontal_limits
 * @param {Object3D} camobj Camera object
 */
exports.clear_horizontal_limits = function(camobj) {
    var render = camobj.render;
    render.horizontal_limits = null;
}

/**
 * Get the horizontal angle limits of the TARGET/EYE camera (converted to the [0, 2PI] range), or
 * the horizontal translation limits of the HOVER camera.
 * @see https://www.blend4web.com/doc/en/camera.html#api
 * @method module:camera.get_horizontal_limits
 * @param {Object3D} camobj Camera Object 3D
 * @param {Vec2} [dest] Destination vector for the camera limits: [left, right] rotation or [Min, Max] translation limits.
 * @returns {?Vec2} Destination vector for the camera limits: [left, right] rotation or [Min, Max] translation limits.
 */
exports.get_horizontal_limits = function(camobj, dest) {
    if (!m_cam.is_target_camera(camobj)
            && !m_cam.is_eye_camera(camobj)
            && !m_cam.is_hover_camera(camobj)) {
        m_print.error("get_horizontal_limits(): wrong object");
        return null;
    }
    var render = camobj.render;

    dest = dest || new Float32Array(2);
    if (render.horizontal_limits) {
        dest[0] = render.horizontal_limits.left;
        dest[1] = render.horizontal_limits.right;
        return dest;
    }
    return null;
}

 /**
 * Check whether the camera has any horizontal limits.
 * @method module:camera.has_horizontal_limits
 * @param {Object3D} camobj Camera Object 3D
 * @returns {?Boolean} True if the camera has horizontal limits.
 */
exports.has_horizontal_limits = function(camobj) {
    if (!m_cam.is_target_camera(camobj)
            && !m_cam.is_eye_camera(camobj)
            && !m_cam.is_hover_camera(camobj)) {
        m_print.error("has_horizontal_limits(): wrong object");
        return null;
    }

    return Boolean(camobj.render.horizontal_limits);
}


/**
 * Set the hover angle limits for the HOVER camera.
 * @see https://www.blend4web.com/doc/en/camera.html#api
 * @method module:camera.apply_hover_angle_limits
 * @param {Object3D} camobj Camera object
 * @param {Number} down_angle Down hover angle limit
 * @param {Number} up_angle Up hover angle limit
 */
exports.apply_hover_angle_limits = function(camobj, down_angle, up_angle) {
    if (m_cam.is_hover_camera(camobj)) {
        if (down_angle < up_angle) {
            m_print.error("apply_hover_angle_limits(): wrong hover angle limits");
            return;
        }

        m_cam.apply_hover_angle_limits(camobj, down_angle, up_angle);
    } else {
        m_print.error("apply_hover_angle_limits(): wrong object");
        return;
    }
}

/**
 * Remove the hover angle limits from the HOVER camera.
 * @method module:camera.clear_hover_angle_limits
 * @param {Object3D} camobj Camera object
 */
exports.clear_hover_angle_limits = function(camobj) {
    if (!m_cam.is_hover_camera(camobj)) {
        m_print.error("clear_hover_angle_limits(): wrong object");
        return;
    }

    camobj.render.hover_angle_limits = null;
}

/**
 * Set the distance limits for the TARGET/HOVER camera.
 * @method module:camera.apply_distance_limits
 * @param {Object3D} camobj Camera object
 * @param {Number} min Minimum distance to target
 * @param {Number} max Maximum distance to target
 */
exports.apply_distance_limits = function(camobj, min, max) {
    if (!m_cam.is_target_camera(camobj)
            && !m_cam.is_hover_camera(camobj)) {
        m_print.error("apply_distance_limits(): wrong object");
        return;
    }

    if (min > max) {
        m_print.error("apply_distance_limits(): wrong distance limits");
        return;
    }

    m_cam.apply_distance_limits(camobj, min, max);
}

/**
 * Remove the distance clamping limits from the TARGET camera.
 * @method module:camera.clear_distance_limits
 * @param {Object3D} camobj Camera object
 */
exports.clear_distance_limits = function(camobj) {
    if (!m_cam.is_target_camera(camobj)
            && !m_cam.is_hover_camera(camobj)) {
        m_print.error("clear_distance_limits(): wrong object");
        return;
    }

    camobj.render.use_distance_limits = false;
}

/**
 * @method module:camera.set_eye_params
 * @deprecated Use {@link module:camera.rotate_camera|camera.rotate_camera} or {@link module:camera.rotate_eye_camera|camera.rotate_eye_camera} to change the camera orientation.
 */
exports.set_eye_params = function(camobj, h_angle, v_angle) {
    m_print.error("set_eye_params() deprecated, use rotate_camera() or rotate_eye_camera() instead");
    exports.rotate_eye_camera(camobj, h_angle, Math.PI/2 - v_angle);
}
/**
 * Check whether the camera is looking upwards.
 * @method module:camera.is_look_up
 * @param {Object3D} camobj Camera object
 * @returns {Boolean} Checking result.
 */
exports.is_look_up = function(camobj) {
    var quat = camobj.render.quat;

    var dir = _vec3_tmp;
    m_util.quat_to_dir(quat, m_util.AXIS_MY, dir);

    if (dir[1] >= 0)
        return true;
    else 
        return false;
}

/**
 * Rotate the camera counterclockwise (CCW) by the given angles depending on the camera's movement style.
 * Performs the delta rotation or sets the camera's absolute rotation depending on the "*_is_abs" parameters.
 * @see https://www.blend4web.com/doc/en/camera.html#api
 * @method module:camera.rotate_camera
 * @param {Object3D} camobj Camera object
 * @param {Number} phi Azimuth angle in radians
 * @param {Number} theta Elevation angle in radians
 * @param {Boolean} [phi_is_abs=false] For phi angle: if FALSE performs delta rotation, if TRUE sets camera absolute rotation
 * @param {Boolean} [theta_is_abs=false] For theta angle: if FALSE performs delta rotation, if TRUE sets camera absolute rotation
 */
exports.rotate_camera = function(camobj, phi, theta, phi_is_abs, theta_is_abs) {
    var move_style = exports.get_move_style(camobj);

    switch (move_style) {
    case m_cam.MS_STATIC:
        break; 
    case m_cam.MS_TARGET_CONTROLS:
        m_cam.rotate_target_camera(camobj, phi, theta, phi_is_abs, theta_is_abs);
        break;
    case m_cam.MS_EYE_CONTROLS:
        m_cam.rotate_eye_camera(camobj, phi, theta, phi_is_abs, theta_is_abs);
        break;
    case m_cam.MS_HOVER_CONTROLS:
        m_cam.rotate_hover_camera(camobj, phi, theta, phi_is_abs, theta_is_abs);
        break;
    default:
        m_print.error("rotate_camera(): Wrong object");
        break;
    }

    m_trans.update_transform(camobj);
    m_phy.sync_transform(camobj);
}

/**
 * Rotate the TARGET camera counterclockwise (CCW) around its pivot by the given angles. 
 * Performs the delta rotation or sets the camera's absolute rotation depending on the "*_is_abs" parameters.
 * @see https://www.blend4web.com/doc/en/camera.html#api
 * @method module:camera.rotate_target_camera
 * @param {Object3D} camobj Camera object
 * @param {Number} phi Azimuth angle in radians
 * @param {Number} theta Elevation angle in radians
 * @param {Boolean} [phi_is_abs=false] For phi angle: if FALSE performs delta rotation, if TRUE sets camera absolute rotation
 * @param {Boolean} [theta_is_abs=false] For theta angle: if FALSE performs delta rotation, if TRUE sets camera absolute rotation
 */
exports.rotate_target_camera = function(camobj, phi, theta, phi_is_abs, theta_is_abs) {
    if (!m_cam.is_target_camera(camobj)) {
        m_print.error("rotate_target_camera(): wrong object");
        return;
    }

    m_cam.rotate_target_camera(camobj, phi, theta, phi_is_abs, theta_is_abs);
    m_trans.update_transform(camobj);
    m_phy.sync_transform(camobj);
}

/**
 * Rotate the EYE camera counterclockwise (CCW) around its origin by the given angles.
 * Performs the delta rotation or sets the camera's absolute rotation depending on the "*_is_abs" parameters.
 * @see https://www.blend4web.com/doc/en/camera.html#api
 * @method module:camera.rotate_eye_camera
 * @param {Object3D} camobj Camera object
 * @param {Number} phi Azimuth angle in radians
 * @param {Number} theta Elevation angle in radians
 * @param {Boolean} [phi_is_abs=false] For phi angle: if FALSE performs delta rotation, if TRUE sets camera absolute rotation
 * @param {Boolean} [theta_is_abs=false] For theta angle: if FALSE performs delta rotation, if TRUE sets camera absolute rotation
 */
exports.rotate_eye_camera = function(camobj, phi, theta, phi_is_abs, theta_is_abs) {
    if (!m_cam.is_eye_camera(camobj)) {
        m_print.error("rotate_eye_camera(): wrong object");
        return;
    }

    m_cam.rotate_eye_camera(camobj, phi, theta, phi_is_abs, theta_is_abs);
    m_trans.update_transform(camobj);
    m_phy.sync_transform(camobj);
}

/**
 * Rotate the HOVER camera around its pivot by the given angles.
 * Performs the delta rotation or sets the camera's absolute rotation depending on the "*_is_abs" parameters.
 * @see https://www.blend4web.com/doc/en/camera.html#api
 * @method module:camera.rotate_hover_camera
 * @param {Object3D} camobj Camera object
 * @param {Number} phi Azimuth angle in radians
 * @param {Number} theta Elevation angle in radians
 * @param {Boolean} [phi_is_abs=false] For phi angle: if FALSE performs delta rotation, if TRUE sets camera absolute rotation
 * @param {Boolean} [theta_is_abs=false] For theta angle: if FALSE performs delta rotation, if TRUE sets camera absolute rotation
 */
exports.rotate_hover_camera = function(camobj, phi, theta, phi_is_abs, theta_is_abs) {
    if (!m_cam.is_hover_camera(camobj)) {
        m_print.error("rotate_hover_camera(): wrong object");
        return;
    }

    m_cam.rotate_hover_camera(camobj, phi, theta, phi_is_abs, theta_is_abs);
    m_trans.update_transform(camobj);
    m_phy.sync_transform(camobj);
}

/**
 * Rotate the EYE camera around its origin by the given delta angles.
 * @method module:camera.rotate
 * @param {Object3D} camobj Camera Object 3D
 * @param {Number} delta_phi Azimuth angle delta in radians
 * @param {Number} delta_theta Elevation angle delta in radians
 * @deprecated Use {@link module:camera.rotate_camera|camera.rotate_camera} or {@link module:camera.rotate_eye_camera|camera.rotate_eye_camera} instead.
 */
exports.rotate = function(camobj, delta_phi, delta_theta) {
    m_print.error("rotate() deprecated, use rotate_camera() or rotate_eye_camera() instead");
    exports.rotate_eye_camera(camobj, delta_phi, -delta_theta);
}

/**
 * Get the azimuth and elevation angles (CCW as seen from the rotation axis)
 * of the TARGET/HOVER camera, or the orientation angles of the EYE camera.
 * @see https://www.blend4web.com/doc/en/camera.html#api
 * @method module:camera.get_camera_angles
 * @param {Object3D} camobj Camera object
 * @param {Vec2} [dest] Destination vector for the camera angles: [phi, theta],
 * phi ~ [0, 2PI], theta ~ [-PI, PI]
 * @returns {Vec2} Destination vector for the camera angles: [phi, theta]
 */
exports.get_camera_angles = function(camobj, dest) {
    if (!dest)
        var dest = new Float32Array(2);
    m_cam.get_camera_angles(camobj, dest);
    return dest;
}

/**
 * Get the azimuth and elevation angles (CCW as seen from the rotation axis)
 * of the TARGET/HOVER camera, or the orientation angles of the EYE camera.
 * The angles are converted for the character object.
 * @see https://www.blend4web.com/doc/en/camera.html#api
 * @method module:camera.get_camera_angles_char
 * @param {Object3D} camobj Camera object
 * @param {Vec2} [dest] Destination vector for the camera angles: [phi, theta],
 * phi ~ [0, 2PI], theta ~ [-PI, PI]
 * @returns {Vec2} Destination vector for the camera angles: [phi, theta]
 */
exports.get_camera_angles_char = function(camobj, dest) {
    if (!dest)
        var dest = new Float32Array(2);
    m_cam.get_camera_angles_char(camobj, dest);
    return dest;   
}

/**
 * Get the horizontal and vertical angles of the camera.
 * @method module:camera.get_angles
 * @param {Object3D} camobj Camera Object 3D
 * @param {Vec2} [dest] Destination vector for the camera angles: [h, v]
 * @returns {Vec2} Destination vector for the camera angles: [h, v]
 * @deprecated Use {@link module:camera.get_camera_angles|camera.get_camera_angles} instead.
 */
exports.get_angles = function(camobj, dest) {
    m_print.error("get_angles() deprecated, use get_camera_angles() instead");
    if (!dest)
        var dest = new Float32Array(2);
    m_cam.get_angles(camobj, dest);
    return dest;
}

/**
 * Set the distance to the convergence plane of the stereoscopic camera.
 * @method module:camera.set_stereo_distance
 * @param {Object3D} camobj Camera object
 * @param {Number} conv_dist Distance from the convergence plane
 */
exports.set_stereo_distance = function(camobj, conv_dist) {

    var cameras = camobj.render.cameras;
    for (var i = 0; i < cameras.length; i++) {
        var cam = cameras[i];

        if (cam.type == m_cam.TYPE_STEREO_LEFT || 
                cam.type == m_cam.TYPE_STEREO_RIGHT)
            m_cam.set_stereo_params(cam, conv_dist, cam.stereo_eye_dist);
    }
}
/**
 * Get the distance from the convergence plane of the stereoscopic camera.
 * @method module:camera.get_stereo_distance
 * @param {Object3D} camobj Camera object
 * @returns {Number} Distance from convergence plane
 */
exports.get_stereo_distance = function(camobj) {

    var cameras = camobj.render.cameras;
    for (var i = 0; i < cameras.length; i++) {
        var cam = cameras[i];

        if (cam.type == m_cam.TYPE_STEREO_LEFT || 
                cam.type == m_cam.TYPE_STEREO_RIGHT)
            return cam.stereo_conv_dist;
    }

    return 0;
}
/**
 * Translate the view plane of the camera.
 * Modify the projection matrix of the camera so it appears to be moving in up-down
 * and left-right directions. This method can be used to imitate character
 * walking/running/driving.
 * @method module:camera.translate_view
 * @param {Object3D} camobj Camera object
 * @param {Number} x X coord (positive - left to right)
 * @param {Number} y Y coord (positive - down to up)
 * @param {Number} angle Rotation angle (clockwise)
 */
exports.translate_view = function(camobj, x, y, angle) {
    var cameras = camobj.render.cameras;
    for (var i = 0; i < cameras.length; i++) {
        var cam = cameras[i];

        // NOTE: camera projection matrix already has been updated in 
        // set_view method of camera
        if (!cam.reflection_plane) 
            m_cam.set_projection(cam, cam.aspect);

        var vec3_tmp = _vec3_tmp;
        vec3_tmp[0] = -x;
        vec3_tmp[1] = -y;
        vec3_tmp[2] = 0;

        m_mat4.translate(cam.proj_matrix, vec3_tmp, cam.proj_matrix);
        m_mat4.rotateZ(cam.proj_matrix, angle, cam.proj_matrix);

        m_mat4.multiply(cam.proj_matrix, cam.view_matrix, cam.view_proj_matrix);
        m_cam.calc_view_proj_inverse(cam);
        m_cam.calc_sky_vp_inverse(cam);
    }
}
/**
 * Get the vertical angle of the camera's field of view.
 * @method module:camera.get_fov
 * @param {Object3D} camobj Camera object
 * @returns {Number} Camera field of view (in radians)
 */
exports.get_fov = function(camobj) {
    return m_util.rad(camobj.render.cameras[0].fov);
}

/**
 * Set the vertical angle of the camera's field of view.
 * @method module:camera.set_fov
 * @param {Object3D} camobj Camera object
 * @param {Number} fov New camera field of view (in radians)
 */
exports.set_fov = function(camobj, fov) {
    var cameras = camobj.render.cameras;
    for (var i = 0; i < cameras.length; i++) {
        var cam = cameras[i];

        cam.fov = m_util.deg(fov);

        // see comments in translate_view()
        if (!cam.reflection_plane)
            m_cam.set_projection(cam, cam.aspect);

        m_mat4.multiply(cam.proj_matrix, cam.view_matrix, cam.view_proj_matrix);
        m_cam.calc_view_proj_inverse(cam);
        m_cam.calc_sky_vp_inverse(cam);
    }
}

/**
 * Correct the UP vector of the camera.
 * @method module:camera.correct_up
 * @param {Object3D} camobj Camera object
 * @param {Vec3} y_axis Axis vector
 */
exports.correct_up = function(camobj, y_axis) {
    if (!y_axis) {
        y_axis = m_util.AXIS_Y;
    }

    m_cons.correct_up(camobj, y_axis);
}

/**
 * Zoom the camera to the object.
 * @method module:camera.zoom_object
 * @param {Object3D} camobj Camera object
 * @param {Object3D} obj Object 3D
 */
exports.zoom_object = function(camobj, obj) {

    if (!m_cam.is_target_camera(camobj)) {
        m_print.error("zoom_object(): wrong object");
        return;
    }

    var calc_bs_center = false;

    var center = _vec3_tmp;
    m_trans.get_object_center(obj, calc_bs_center, center);
    set_pivot(camobj, center);
    m_trans.update_transform(camobj);

    var radius = m_trans.get_object_size(obj);
    var ang_radius = m_cam.get_angular_diameter(camobj) / 2;

    var dist_need = radius / Math.sin(ang_radius);
    var dist_current = m_trans.obj_point_distance(camobj, center);

    // +y move backward
    m_trans.move_local(camobj, 0, dist_need - dist_current, 0);

    m_trans.update_transform(camobj);
    m_phy.sync_transform(camobj);
}

/**
 * Set the orthogonal scale of the camera.
 * @method module:camera.set_ortho_scale
 * @param {Object3D} camobj Camera object
 * @param {Number} ortho_scale Orthogonal scale
 */
exports.set_ortho_scale = function(camobj, ortho_scale) {
    if (!m_obj_util.is_camera(camobj) || !exports.is_ortho_camera(camobj)) {
        m_print.error("set_ortho_scale(): wrong object");
        return;
    }

    var render = camobj.render;

    if (m_cam.is_target_camera(camobj)) {
        var dir_dist = m_vec3.dist(render.trans, render.pivot);
        render.init_top = ortho_scale / 2 * render.init_dist / dir_dist;
    } else if (m_cam.is_hover_camera(camobj) 
            && exports.has_distance_limits(camobj)) {
        var dir_dist = m_vec3.distance(render.trans, render.hover_pivot);
        render.init_top = ortho_scale / 2 * render.init_dist / dir_dist;
    } else
        // hover camera without distance limits, eye or static camera
        camobj.render.cameras[0].top = ortho_scale / 2;

    m_cam.update_ortho_scale(camobj);
}

/**
 * Get the orthogonal scale of the camera.
 * @method module:camera.get_ortho_scale
 * @param {Object3D} camobj Camera object
 * @returns {?Number} Orthogonal scale
 */

exports.get_ortho_scale = function(camobj) {
    if (!m_obj_util.is_camera(camobj) || !exports.is_ortho_camera(camobj)) {
        m_print.error("get_ortho_scale(): wrong object");
        return null;
    }

    return camobj.render.cameras[0].top * 2;
}

/**
 * Check whether the camera is an ORTHO camera. 
 * @method module:camera.is_ortho_camera
 * @param {Object3D} camobj Camera Object 3D
 * @returns {?Boolean} In case of the orthogonal type of the camera it is true, else false
 */
exports.is_ortho_camera = function(camobj) {
    if (!m_obj_util.is_camera(camobj)) {
        m_print.error("is_ortho_camera(): wrong object");
        return null;
    }
    
    return camobj.render.cameras[0].type == m_cam.TYPE_ORTHO;
}

/**
 * Calculate the direction of the camera ray based on the Canvas coordinates.
 * The origin of the Canvas space is located in the top left corner of the Canvas.
 * @method module:camera.calc_ray
 * @param {Object3D} camobj Camera object
 * @param {Number} canvas_x X Canvas coordinate
 * @param {Number} canvas_y Y Canvas coordinate
 * @param {Vec3} [dest] Destination vector
 * @returns {Vec3} Destination vector
 */
exports.calc_ray = function(camobj, canvas_x, canvas_y, dest) {

    if (!dest)
        var dest = new Float32Array(3);

    var cam = camobj.render.cameras[0];

    switch (cam.type) {
    case m_cam.TYPE_PERSP:
    case m_cam.TYPE_PERSP_ASPECT:
    case m_cam.TYPE_STEREO_LEFT:
    case m_cam.TYPE_STEREO_RIGHT:
        var top_1m = Math.tan(cam.fov * Math.PI / 360.0);
        var right_1m = top_1m * cam.aspect;

        var dir = _vec4_tmp;

        var viewport_xy = m_cont.canvas_to_viewport_coords(canvas_x, canvas_y, 
            _vec2_tmp, cam);

        // in the camera's local space
        dir[0] = (2.0 * viewport_xy[0] / cam.width - 1.0) * right_1m;
        dir[1] = -1;
        dir[2] = (2.0 * viewport_xy[1] / cam.height - 1.0) * top_1m;
        dir[3] = 0;

        var wm = camobj.render.world_matrix;
        m_vec4.transformMat4(dir, wm, dir);

        dest[0] = dir[0];
        dest[1] = dir[1];
        dest[2] = dir[2];

        m_vec3.normalize(dest, dest);

        return dest;
    default:
        m_print.error("Non-compatible camera");
        return dest;
    }
}

/**
 * Project the 3D point to the Canvas.
 * Returned coordinates are measured in CSS pixels.
 * @method module:camera.project_point
 * @param {Object3D} camobj Camera object
 * @param {Vec3} point Point in world space
 * @param {Vec2|Vec3} [dest] Destination canvas coordinates (vec2 - X/Y, vec3 - X/Y/DEPTH).
 * @returns {Vec2|Vec3} Destination canvas coordinates.
 */
exports.project_point = function(camobj, point, dest) {
    if (!dest)
        var dest = new Float32Array(2);

    return m_cam.project_point(camobj, point, dest);
}

}
