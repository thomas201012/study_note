import logging
import asyncio
import lvgl as lv
import core.constants as c
from micropython import const



log = logging.getLogger("SENSOR_HIS")
locale = c.importVariant(".ui.locale")
_apps = c.importVariant('.ui.apps')
_ = getattr(locale.gettext, "_")

_scr = None
_app_mgr = None
_sn = ""
tm_history_data = ""
hu_history_data = ""
chart = None
value = 0

ecg_sample = [
    -2, 2, 0, -15, -39, -63, -71, -68, -67, -69, -84, -95, -104, -107, -108, -107, -107, -107, -107, -114, -118, -117,
    -112, -100, -89, -83, -71, -64, -58, -58, -62, -62, -58, -51, -46, -39, -27, -10, 4, 7, 1, -3, 0, 14, 24, 30, 25, 19,
    13, 7, 12, 15, 18, 21, 13, 6, 9, 8, 17, 19, 13, 11, 11, 11, 23, 30, 37, 34, 25, 14, 15, 19, 28, 31, 26, 23, 25, 31,
    39, 37, 37, 34, 30, 32, 22, 29, 31, 33, 37, 23, 13, 7, 2, 4, -2, 2, 11, 22, 33, 19, -1, -27, -55, -67, -72, -71, -63,
    -49, -18, 35, 113, 230, 369, 525, 651, 722, 730, 667, 563, 454, 357, 305, 288, 274, 255, 212, 173, 143, 117, 82, 39,
    -13, -53, -78, -91, -101, -113, -124, -131, -131, -131, -129, -128, -129, -125, -123, -123, -129, -139, -148, -153,
    -159, -166, -183, -205, -227, -243, -248, -246, -254, -280, -327, -381, -429, -473, -517, -556, -592, -612, -620,
    -620, -614, -604, -591, -574, -540, -497, -441, -389, -358, -336, -313, -284, -222, -167, -114, -70, -47, -28, -4, 12,
    38, 52, 58, 56, 56, 57, 68, 77, 86, 86, 80, 69, 67, 70, 82, 85, 89, 90, 89, 89, 88, 91, 96, 97, 91, 83, 78, 82, 88, 95,
    96, 105, 106, 110, 102, 100, 96, 98, 97, 101, 98, 99, 100, 107, 113, 119, 115, 110, 96, 85, 73, 64, 69, 76, 79,
    78, 75, 85, 100, 114, 113, 105, 96, 84, 74, 66, 60, 75, 85, 89, 83, 67, 61, 67, 73, 79, 74, 63, 57, 56, 58, 61, 55,
    48, 45, 46, 55, 62, 55, 49, 43, 50, 59, 63, 57, 40, 31, 23, 25, 27, 31, 35, 34, 30, 36, 34, 42, 38, 36, 40, 46, 50,
    47, 32, 30, 32, 52, 67, 73, 71, 63, 54, 53, 45, 41, 28, 13, 3, 1, 4, 4, -8, -23, -32, -31, -19, -5, 3, 9, 13, 19,
    24, 27, 29, 25, 22, 26, 32, 42, 51, 56, 60, 57, 55, 53, 53, 54, 59, 54, 49, 26, -3, -11, -20, -47, -100, -194, -236,
    -212, -123, 8, 103, 142, 147, 120, 105, 98, 93, 81, 61, 40, 26, 28, 30, 30, 27, 19, 17, 21, 20, 19, 19, 22, 36, 40,
    35, 20, 7, 1, 10, 18, 27, 22, 6, -4, -2, 3, 6, -2, -13, -14, -10, -2, 3, 2, -1, -5, -10, -19, -32, -42, -55, -60,
    -68, -77, -86, -101, -110, -117, -115, -104, -92, -84, -85, -84, -73, -65, -52, -50, -45, -35, -20, -3, 12, 20, 25,
    26, 28, 28, 30, 28, 25, 28, 33, 42, 42, 36, 23, 9, 0, 1, -4, 1, -4, -4, 1, 5, 9, 9, -3, -1, -18, -50, -108, -190,
    -272, -340, -408, -446, -537, -643, -777, -894, -920, -853, -697, -461, -251, -60, 58, 103, 129, 139, 155, 170, 173,
    178, 185, 190, 193, 200, 208, 215, 225, 224, 232, 234, 240, 240, 236, 229, 226, 224, 232, 233, 232, 224, 219, 219,
    223, 231, 226, 223, 219, 218, 223, 223, 223, 233, 245, 268, 286, 296, 295, 283, 271, 263, 252, 243, 226, 210, 197,
    186, 171, 152, 133, 117, 114, 110, 107, 96, 80, 63, 48, 40, 38, 34, 28, 15, 2, -7, -11, -14, -18, -29, -37, -44, -50,
    -58, -63, -61, -52, -50, -48, -61, -59, -58, -54, -47, -52, -62, -61, -64, -54, -52, -59, -69, -76, -76, -69, -67,
    -74, -78, -81, -80, -73, -65, -57, -53, -51, -47, -35, -27, -22, -22, -24, -21, -17, -13, -10, -11, -13, -20, -20,
    -12, -2, 7, -1, -12, -16, -13, -2, 2, -4, -5, -2, 9, 19, 19, 14, 11, 13, 19, 21, 20, 18, 19, 19, 19, 16, 15, 13, 14,
    9, 3, -5, -9, -5, -3, -2, -3, -3, 2, 8, 9, 9, 5, 6, 8, 8, 7, 4, 3, 4, 5, 3, 5, 5, 13, 13, 12, 10, 10, 15, 22, 17,
    14, 7, 10, 15, 16, 11, 12, 10, 13, 9, -2, -4, -2, 7, 16, 16, 17, 16, 7, -1, -16, -18, -16, -9, -4, -5, -10, -9, -8,
    -3, -4, -10, -19, -20, -16, -9, -9, -23, -40, -48, -43, -33, -19, -21, -26, -31, -33, -19, 0, 17, 24, 9, -17, -47,
    -63, -67, -59, -52, -51, -50, -49, -42, -26, -21, -15, -20, -23, -22, -19, -12, -8, 5, 18, 27, 32, 26, 25, 26, 22,
    23, 17, 14, 17, 21, 25, 2, -45, -121, -196, -226, -200, -118, -9, 73, 126, 131, 114, 87, 60, 42, 29, 26, 34, 35, 34,
    25, 12, 9, 7, 3, 2, -8, -11, 2, 23, 38, 41, 23, 9, 10, 13, 16, 8, -8, -17, -23, -26, -25, -21, -15, -10, -13, -13,
    -19, -22, -29, -40, -48, -48, -54, -55, -66, -82, -85, -90, -92, -98, -114, -119, -124, -129, -132, -146, -146, -138,
    -124, -99, -85, -72, -65, -65, -65, -66, -63, -64, -64, -58, -46, -26, -9, 2, 2, 4, 0, 1, 4, 3, 10, 11, 10, 2, -4,
    0, 10, 18, 20, 6, 2, -9, -7, -3, -3, -2, -7, -12, -5, 5, 24, 36, 31, 25, 6, 3, 7, 12, 17, 11, 0, -6, -9, -8, -7, -5,
    -6, -2, -2, -6, -2, 2, 14, 24, 22, 15, 8, 4, 6, 7, 12, 16, 25, 20, 7, -16, -41, -60, -67, -65, -54, -35, -11, 30,
    84, 175, 302, 455, 603, 707, 743, 714, 625, 519, 414, 337, 300, 281, 263, 239, 197, 163, 136, 109, 77, 34, -18, -50,
    -66, -74, -79, -92, -107, -117, -127, -129, -135, -139, -141, -155, -159, -167, -171, -169, -174, -175, -178, -191,
    -202, -223, -235, -243, -237, -240, -256, -298, -345, -393, -432, -475, -518, -565, -596, -619, -623, -623, -614,
    -599, -583, -559, -524, -477, -425, -383, -357, -331, -301, -252, -198, -143, -96, -57, -29, -8, 10, 31, 45, 60, 65,
    70, 74, 76, 79, 82, 79, 75, 62,
]

def event_handler(e):
    global value
    e_code = e.get_code()
    if e_code == lv.EVENT.CLICKED:
        print("lv.EVENT.CLICKED")
    elif e_code == lv.EVENT.KEY:
        e_key = e.get_key()
        print("lv.EVENT.KEY")
        if e_key == lv.KEY.RIGHT:
            value += 1
        elif e_key == lv.KEY.LEFT:
            value -= 1
        if value <= 0: value = 0
        if value >= 10: value = 10
        chart.set_zoom_x(lv.IMG_ZOOM.NONE * value)

def hu_event_cb(e):

    dsc = lv.obj_draw_part_dsc_t.__cast__(e.get_param())
    if dsc.part == lv.PART.TICKS and dsc.id == lv.chart.AXIS.PRIMARY_X: 
        month = ["17:27", "18:27", "19:27", "20:27", "20:27"]
        # dsc.text is defined char text[16], I must therefore convert the Python string to a byte_array
        print("PRIMARY_X", dsc.value)
        dsc.text = bytes(month[dsc.value],"ascii") 
    if dsc.part == lv.PART.TICKS and dsc.id == lv.chart.AXIS.PRIMARY_Y: 
        # dsc.text is defined char text[16], I must therefore convert the Python string to a byte_array
        print("PRIMARY_Y", dsc.value)
        dsc.text = bytes(str(int(dsc.value / 100)) + "%","ascii") 

async def tm_ui_init():
    global chart, value
    if _scr: _scr.clean()

    title = lv.label(_scr)
    title.set_text("Humidity History")
    title.set_style_text_font(lv.font_ascii_bold_28, 0)
    title.set_long_mode(lv.label.LONG.SCROLL_CIRCULAR)
    title.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
    title.align(lv.ALIGN.TOP_LEFT, 10, 1)
    title.add_event(event_handler, lv.EVENT.ALL, None)
    lv.group_get_default().set_editing(False)
    lv.group_focus_obj(title)

    line_points = [{"x": 0, "y": 0}, {"x": 320, "y": 0}]
    line = lv.line(_scr)
    line.set_points(line_points, len(line_points))  # Set the points
    line.align(lv.ALIGN.TOP_LEFT, 0, 30)
    line.set_style_line_width(2, 0)
    line.set_style_line_color(lv.color_hex(0xBBBBBB), 0)
    # Create a chart
    max_value = max(ecg_sample)
    min_value = min(ecg_sample)

    value = 0
    chart = lv.chart(_scr)
    chart.set_size(250, 180)
    chart.align(lv.ALIGN.CENTER, 25, 5)
    chart.set_range(lv.chart.AXIS.PRIMARY_Y, min_value, max_value)
    chart.set_div_line_count(5, 0)
    chart.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
    chart.set_style_bg_opa(0, lv.PART.MAIN | lv.STATE.DEFAULT)
    chart.set_style_text_color(lv.color_hex(0x111111), lv.PART.MAIN | lv.STATE.DEFAULT)
    chart.set_style_text_font(lv.font_ascii_16, 0)

    chart.set_axis_tick(lv.chart.AXIS.PRIMARY_X, 5, 5, 5, 1, True, 30)
    chart.set_axis_tick(lv.chart.AXIS.PRIMARY_Y, 10, 5, 6, 5, True, 80)
    chart.add_event(hu_event_cb, lv.EVENT.DRAW_PART_BEGIN, None)
    
    ser = chart.add_series(lv.palette_main(lv.PALETTE.BLUE), lv.chart.AXIS.PRIMARY_Y)
    
    pcnt = len(ecg_sample)
    chart.set_point_count(pcnt)
    chart.set_ext_y_array(ser, ecg_sample)

def tm_event_cb(e):
    global value
    dsc = lv.obj_draw_part_dsc_t.__cast__(e.get_param())
    e_code = e.get_code()
    if dsc.part == lv.PART.TICKS and dsc.id == lv.chart.AXIS.PRIMARY_X: 
        month = ["17:27", "18:27", "19:27", "20:27", "20:27"]
        # dsc.text is defined char text[16], I must therefore convert the Python string to a byte_array
        print("PRIMARY_X", dsc.value)
        dsc.text = bytes(month[dsc.value],"ascii") 
    if dsc.part == lv.PART.TICKS and dsc.id == lv.chart.AXIS.PRIMARY_Y: 
        # dsc.text is defined char text[16], I must therefore convert the Python string to a byte_array
        print("PRIMARY_Y", dsc.value)
        dsc.text = bytes(str(round(dsc.value / 100, 1)) + "\u00B0F","ascii") 

async def tm_ui_init():
    global chart, value
    if _scr: _scr.clean()

    title = lv.label(_scr)
    title.set_text("Temperature History")
    title.set_style_text_font(lv.font_ascii_bold_28, 0)
    title.set_long_mode(lv.label.LONG.SCROLL_CIRCULAR)
    title.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
    title.align(lv.ALIGN.TOP_LEFT, 10, 1)
    title.add_event(event_handler, lv.EVENT.ALL, None)
    lv.group_get_default().add_obj(title)
    lv.group_get_default().set_editing(False)
    lv.group_focus_obj(title)


    line_points = [{"x": 0, "y": 0}, {"x": 320, "y": 0}]
    line = lv.line(_scr)
    line.set_points(line_points, len(line_points))  # Set the points
    line.align(lv.ALIGN.TOP_LEFT, 0, 30)
    line.set_style_line_width(2, 0)
    line.set_style_line_color(lv.color_hex(0xBBBBBB), 0)
    # Create a chart
    max_value = max(ecg_sample)
    min_value = min(ecg_sample)

    value = 0
    chart = lv.chart(_scr)
    chart.set_size(250, 180)
    chart.align(lv.ALIGN.CENTER, 25, 5)
    chart.set_range(lv.chart.AXIS.PRIMARY_Y, min_value, max_value)
    chart.set_div_line_count(5, 0)
    chart.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
    chart.set_style_bg_opa(0, lv.PART.MAIN | lv.STATE.DEFAULT)
    chart.set_style_text_color(lv.color_hex(0x111111), lv.PART.MAIN | lv.STATE.DEFAULT)
    chart.set_style_text_font(lv.font_ascii_16, 0)

    chart.set_axis_tick(lv.chart.AXIS.PRIMARY_X, 5, 5, 5, 1, True, 30)
    chart.set_axis_tick(lv.chart.AXIS.PRIMARY_Y, 10, 5, 6, 5, True, 80)
    chart.add_event(tm_event_cb, lv.EVENT.DRAW_PART_BEGIN, None)
    
    ser = chart.add_series(lv.palette_main(lv.PALETTE.BLUE), lv.chart.AXIS.PRIMARY_Y)
    
    pcnt = len(ecg_sample)
    chart.set_point_count(pcnt)
    chart.set_ext_y_array(ser, ecg_sample)

async def start(scr, app_mgr, sn):
    global _scr, _app_mgr,  _sn, tm_history_data, hu_history_data
    _sn = sn
    _scr = scr
    _app_mgr = app_mgr
    _app_mgr.leave_root_page()
    tm_history_data = {}
    hu_history_data = {}
    await tm_ui_init()
