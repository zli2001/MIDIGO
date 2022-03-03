#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

from PyQt5.QtGui import QPixmap, QEnterEvent, QIcon

from titleUI import TITLE
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSlot, QPoint


class TitleWin(QWidget,TITLE):
    def __init__(self,parent=None,widget_2_sub=None):
        super(TitleWin,self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self._init_TitleWin()#标题栏窗口初始化

        self._initDrag()  # 设置鼠标跟踪判断扳机默认值
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.my_Qss()  # 美化
        self.widget.installEventFilter(self)  # 初始化事件过滤器
        self.widget_2.installEventFilter(self)

        if widget_2_sub:
            self.widget_2_sub = widget_2_sub
            self.resize(self.widget_2_sub.width(), self.widget_2_sub.height() + self.widget.height())
            self.insert_widget()


    def _init_TitleWin(self):
        self.setWindowFlags(Qt.FramelessWindowHint)#设置窗体无边框
        self.setAttribute(Qt.WA_TranslucentBackground)#设置背景透明



    def insert_widget(self):
        # widget_2控件初始化与创建垂直布局QVBoxLayout
        self.widget_2_vcroLayout = QVBoxLayout(self.widget_2)
        self.widget_2_vcroLayout.setContentsMargins(0, 0, 0, 0)  # 设置布局外部大小
        self.widget_2_vcroLayout.setSpacing(0)  # 设置布局控件间距
        self.widget_2_vcroLayout.setObjectName("widget_2_vcroLayout")
        # 设置垂直布局对齐方式
        self.widget_2_vcroLayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.widget_2.setLayout(self.widget_2_vcroLayout)  # 这一步暂时没有发现有什么用，

        self.widget_2_vcroLayout.addWidget(self.widget_2_sub)  # 增添内容控件

    def _initDrag(self):
            # 设置鼠标跟踪判断扳机默认值
        self._move_drag = False
        #self._corner_drag = False
        #self._bottom_drag = False
        #self._right_drag = False


    def on_minBtn_clicked(self):
            # 最小化
        self.showMinimized()

    def on_closeBtn_clicked(self):
            # 关闭程序
        self.close()

    def eventFilter(self, obj, event):
            # 事件过滤器,用于解决鼠标进入其它控件后还原为标准鼠标样式
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
        return super(TitleWin, self).eventFilter(obj, event)  # 注意 ,MyWindow是所在类的名称
            # return QWidget.eventFilter(self, obj, event)  # 用这个也行，但要注意修改窗口类型

    """def resizeEvent(self, QResizeEvent):
            # 自定义窗口调整大小事件
            # 改变窗口大小的三个坐标范围
            self._right_rect = [QPoint(x, y) for x in range(self.width() - 5, self.width() + 5)
                                for y in range(self.widget.height() + 20, self.height() - 5)]
            self._bottom_rect = [QPoint(x, y) for x in range(1, self.width() - 5)
                                 for y in range(self.height() - 5, self.height() + 1)]
            self._corner_rect = [QPoint(x, y) for x in range(self.width() - 5, self.width() + 1)
                                 for y in range(self.height() - 5, self.height() + 1)]"""

    def mousePressEvent(self, event):
            # 重写鼠标点击的事件
       """ if (event.button() == Qt.LeftButton) and (event.pos() in self._corner_rect):
                # 鼠标左键点击右下角边界区域
            self._corner_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._right_rect):
                # 鼠标左键点击右侧边界区域
            self._right_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._bottom_rect):
                # 鼠标左键点击下侧边界区域
            self._bottom_drag = True
            event.accept()
        elif"""
       if (event.button() == Qt.LeftButton) and (event.y() < self.widget.height()):
                # 鼠标左键点击标题栏区域
            self._move_drag = True
            self.move_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
            # 判断鼠标位置切换鼠标手势
        """if QMouseEvent.pos() in self._corner_rect:  # QMouseEvent.pos()获取相对位置
            self.setCursor(Qt.SizeFDiagCursor)
        elif QMouseEvent.pos() in self._bottom_rect:
            self.setCursor(Qt.SizeVerCursor)
        elif QMouseEvent.pos() in self._right_rect:
            self.setCursor(Qt.SizeHorCursor)

            # 当鼠标左键点击不放及满足点击区域的要求后，分别实现不同的窗口调整
            # 没有定义左方和上方相关的5个方向，主要是因为实现起来不难，但是效果很差，拖放的时候窗口闪烁，再研究研究是否有更好的实现
        if Qt.LeftButton and self._right_drag:
                # 右侧调整窗口宽度
            self.resize(QMouseEvent.pos().x(), self.height())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._bottom_drag:
                # 下侧调整窗口高度
            self.resize(self.width(), QMouseEvent.pos().y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._corner_drag:
                #  由于我窗口设置了圆角,这个调整大小相当于没有用了
                # 右下角同时调整高度和宽度
            self.resize(QMouseEvent.pos().x(), QMouseEvent.pos().y())
            QMouseEvent.accept()"""

        if Qt.LeftButton and self._move_drag:
                # 标题栏拖放窗口位置
            self.move(QMouseEvent.globalPos() - self.move_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
            # 鼠标释放后，各扳机复位
        self._move_drag = False
        #self._corner_drag = False
        #self._bottom_drag = False
        #self._right_drag = False

    def my_Qss(self):
        # 给标题栏控件设置别的属性名，这样就不会在美化时和新加进来的内容栏窗口的控件有冲突了
        self.widget.setProperty('other_name', 'title_bar_widget')
        self.widget_2.setProperty('other_name', 'title_bar_widget_2')
        self.label.setProperty('other_name', 'title_bar_lable')
        self.label_2.setProperty('other_name', 'title_bar_lable_2')
        self.pushButton.setProperty('other_name', 'title_bar_pushButton')
        self.pushButton_3.setProperty('other_name', 'title_bar_pushButton_3')

        # Qss美化
        qssStyle = '''
                   QWidget[other_name='title_bar_widget']{background-color:white;
                   border-left:3px solid lightgray;
                   border-right:3px solid lightgray;
                   border-top:3px solid lightgray;
                  border-bottom:1px solid lightgray;
                   border-top-left-radius: 20px;
                   border-top-right-radius: 20px;
                   
                   }
                  
                  
                   QPushButton[other_name='title_bar_pushButton']
                   {
                   background:#6DDF6D;border-radius:5px;
                   border:none;
                   font-family:"华光准圆_CNKI";
                   text-align:center;
                   }
                   QPushButton[other_name='title_bar_pushButton']:hover{background:green;}


                   QPushButton[other_name='title_bar_pushButton_3']
                   {
                   background:#F76677;border-radius:5px;
                   border:none;
                   font-family:"华光准圆_CNKI";
                   text-align:center;
                   }
                   QPushButton[other_name='title_bar_pushButton_3']:hover{background:red;}
                   '''
        self.setStyleSheet(qssStyle)


if __name__=="__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWin=TitleWin()
    myWin.show()
    sys.exit(app.exec_())