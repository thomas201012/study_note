# lvgl学习笔记
## 项目中lvgl运行流程，及界面、控件创建思路。
## 以dock_hub为例
### 多界面及开机显示创建、显示思路。
+ 在`ui.init()`中，完成了lvgl和显示亮度的初始化后，通过`apps.init()`和`__loop()`这两个函数分别完成开机初始化和主页面的加载。其中`__loop()`为死循环函数，以便后续界面的切换。
    + `apps.init()`完成了以下的步骤：
        + 1、`self.appWaitShowLogo(True)`:开机界面初始化。
        + 2、app的初始化：将需要加载的界面存储至`ui_apps`列表中，方便后续的跳转
        + 3、开机演示一段时间，并完成加载条的加载。
        + 4、`self.appWaitShowLogo(False)` :关闭开机界面。
        + 5、`self.appEnter()`:显示一段字符，表示正在等待主页面加载（一般不会显示）
    + `__loop()`完成了以下功能：
        + 1、`gc.collect()`:内存清理，垃圾回收。
        + 2、`apps.refresh()`:界面的切换及初始化（每次切换都会重新初始化界面）
            + 1、`pNotifiction.on_refresh()`:通知弹窗的显示。
            + 2、`self.ui_apps[self.ui_index].on_refresh()`：完成相对应界面的跳转，并进行界面的初始化。
---
## 界面的创建
+ 想要完成一个界面的创建，首先需要在`ui/apps`中创建相应功能的文件夹，并在`apps/__init__.py/BUILD_IN_APPS`列表中添加相应的界面。
+ 在对应界面的文件夹中，需要创建一个`__init__.py`文件，文件中一般包含如下函数：
    + `on_enter()`：在界面切换时，会跳转至此程序，一般用来完成对界面的初始化等待。
    + `on_refresh()`：在界面完成切换后，会一直循环进入次函数，一般用来完成对界面的数据修改。
    + `_init()`：一般会在上面两个函数中进行调用，此函数用来存放界面的渲染函数。

---
## 常用API(micropython)
### 通用：
+ obj = lv.obj(parent)---创建通用组件
+ obj.set_size(x, y)---设置大小
+ obj.set_style_bg_color(lv.color_hex(0x0BB4ED), lv.PART.MAIN)---设置组件背景颜色
+ obj.set_style_bg_opa(lv.OPA._20, lv.PART.MAIN)---设置组件背景不透明度
+ obj.set_style_border_width(0, lv.PART.MAIN)---设置边框宽度，lv.PART.MAIN选择的是组件主体
+ obj.align(align, x_mod, y_mod)---设置对象位置,align--对齐方式，x_mod--对齐后x轴偏移像素点，y_mod--对齐后y轴偏移像素点
+ obj.align_to(parent, align, x_mod, y_mod)---设置关于parent对齐。
+ obj.set_style_layout(layout, lv.PART.MAIN)---设置布局风格
+ obj.set_style_flex_flow(flex_flow, lv.PART.MAIN)---设置对象的 Flex 布局流动属性
+ obj.set_style_flex_main_place(flex_main_place, lv.PART.MAIN)---设置对象的 Flex 主轴对齐方式
### 字体：
+ app_title = lv.label(parent)---创建字体组建，parent为组件的父类
+ app_title.set_style_text_font(lv.font_ascii_32, lv.PART.MAIN)---设置字体样式
+ app_title.set_style_text_color(lv.color_hex(0x0BB4ED), lv.PART.MAIN)---设置字体颜色
+ app_title.set_text(app_title_text)---设置字体内容



---