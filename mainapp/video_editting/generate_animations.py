import random

animation_options = {
    "pan_in": {
        "easing": "ease-in-out",
        "type": "pan",
        "scope": "element",
        "direction": "right",
        "start_scale": "120%",
        "end_scale": "100%",
        "time": 0,
        "fade": False,
        "duration": 2,
    },
    "pan_out": {
        "easing": "ease-in-out",
        "type": "pan",
        "scope": "element",
        "direction": "left",
        "start_scale": "100%",
        "end_scale": "120%",
        "time": 0,
        "fade": False,
        "duration": 2,
    },
    "shake_horizontal": {
        "easing": "ease-in-out",
        "type": "shake",
        "scope": "element",
        "direction": "horizontal",
        "fade": False,
        "duration": 2,
    },
    "shake_vertical": {
        "easing": "ease-in-out",
        "type": "shake",
        "scope": "element",
        "direction": "vertical",
        "fade": False,
        "duration": 2,
    },
    "bounce_horizontal": {
        "easing": "ease-in-out",
        "type": "bounce",
        "scope": "element",
        "direction": "horizontal",
        "fade": False,
        "duration": 2,
    },
    "bounce_vertical": {
        "easing": "ease-in-out",
        "type": "bounce",
        "scope": "element",
        "direction": "vertical",
        "fade": False,
        "duration": 2,
    },
    "wiggle_horizontal": {
        "easing": "ease-in-out",
        "type": "wiggle",
        "scope": "element",
        "direction": "horizontal",
        "fade": False,
        "duration": 2,
    },
    "wiggle_vertical": {
        "easing": "ease-in-out",
        "type": "wiggle",
        "scope": "element",
        "direction": "vertical",
        "fade": False,
        "duration": 2,
    },
    "zoom_in": {
        "easing": "ease-in-out",
        "type": "scale",
        "scope": "element",
        "start_scale": "100%",
        "end_scale": "120%",
        "fade": False,
        "duration": 2,
    },
    "zoom_out": {
        "easing": "ease-in-out",
        "type": "scale",
        "scope": "element",
        "start_scale": "120%",
        "end_scale": "100%",
        "fade": False,
        "duration": 2,
    },
    "pan_right_extreme": {
        "easing": "ease-in-out",
        "type": "pan",
        "scope": "element",
        "direction": "right",
        "start_scale": "100%",
        "end_scale": "120%",
        "time": 0,
        "fade": False,
        "duration": 2,
    },
    # Custom options
    "zoom_in_extreme": {
        "easing": "ease-in-out",
        "type": "scale",
        "scope": "element",
        "start_scale": "100%",
        "end_scale": "150%",
        "fade": False,
        "duration": 2,
    },
    "zoom_out_extreme": {
        "easing": "ease-in-out",
        "type": "scale",
        "scope": "element",
        "start_scale": "150%",
        "end_scale": "100%",
        "fade": False,
        "duration": 2,
    },
}

transition_animations = {
    "slide_up": {
        "duration": 1,
        "easing": "cubic-in-out",
        "transition": True,
        "type": "slide",
        "fade": False,
        "direction": "90°",
    },
    "slide_down": {
        "duration": 1,
        "easing": "cubic-in-out",
        "transition": True,
        "type": "slide",
        "fade": False,
        "direction": "270°",
    },
    "slide_left": {
        "duration": 1,
        "easing": "cubic-in-out",
        "transition": True,
        "type": "slide",
        "fade": False,
        "direction": "180°",
    },
    "slide_right": {
        "duration": 1,
        "easing": "cubic-in-out",
        "transition": True,
        "type": "slide",
        "fade": False,
        "direction": "0°",
    },
    "scale_up": {
        "duration": 1,
        "easing": "cubic-in-out",
        "transition": True,
        "type": "scale",
        "fade": False,
        "start_scale": "100%",
        "end_scale": "120%",
    },
    "scale_down": {
        "duration": 1,
        "easing": "cubic-in-out",
        "transition": True,
        "type": "scale",
        "fade": False,
        "start_scale": "120%",
        "end_scale": "100%",
    },
    "zoom_in": {
        "easing": "ease-in-out",
        "type": "scale",
        "scope": "element",
        "start_scale": "100%",
        "end_scale": "120%",
        "fade": False,
        "transition": True,
    },
    "zoom_out": {
        "easing": "ease-in-out",
        "type": "scale",
        "scope": "element",
        "start_scale": "120%",
        "end_scale": "100%",
        "fade": False,
        "transition": True,
    },
    "wipe_up": {
        "duration": 1,
        "easing": "cubic-in-out",
        "transition": True,
        "type": "wipe",
        "fade": False,
        "direction": "90°",
    },
    "wipe_down": {
        "duration": 1,
        "easing": "cubic-in-out",
        "transition": True,
        "type": "wipe",
        "fade": False,
        "direction": "270°",
    },
    "wipe_left": {
        "duration": 1,
        "easing": "cubic-in-out",
        "transition": True,
        "type": "wipe",
        "fade": False,
        "direction": "180°",
    },
    "wipe_right": {
        "duration": 1,
        "easing": "cubic-in-out",
        "transition": True,
        "type": "wipe",
        "fade": False,
        "direction": "0°",
    },
    "squash": {
        "duration": 1,
        "easing": "cubic-in-out",
        "transition": True,
        "type": "squash",
        "fade": False,
    },
    "spin": {
        "duration": 1,
        "easing": "cubic-in-out",
        "transition": True,
        "type": "spin",
        "fade": False,
        "angle": "360°",
    },
    "flip_horizontal": {
        "duration": 1,
        "easing": "cubic-in-out",
        "transition": True,
        "type": "flip",
        "fade": False,
        "direction": "horizontal",
    },
    "flip_vertical": {
        "duration": 1,
        "easing": "cubic-in-out",
        "transition": True,
        "type": "flip",
        "fade": False,
        "direction": "vertical",
    },
}


def set_animation_durations(time):
    for key in animation_options.keys():
        animation_options[key]["duration"] = time * 5


def set_transition_durations(t_time):
    for key in transition_animations.keys():
        transition_animations[key]["duration"] = t_time


def create_animation(time):
    print("Inside create_animation function")
    t_time = time * 0.05
    set_animation_durations(time=time)
    set_transition_durations(t_time=t_time)
    anim_key = random.choice(list(animation_options.keys()))
    trans_key = random.choice(list(transition_animations.keys()))
    print("animation : ", anim_key)
    print("transition : ", trans_key)
    animation = animation_options[anim_key]
    transition = transition_animations[trans_key]
    return animation, transition
