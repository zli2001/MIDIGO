#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PyQt5 import QtWidgets, QtCore
#from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QGridLayout, QWidget, QApplication,QMessageBox,QProgressDialog
#from PyQt5.QtCore import Qt, QSize
from testUI import TEST
from call_titleUI import TitleWin
import sys
import tools
import os
from generate import main
from PyQt5.QtCore import pyqtSlot
from evaluate import main_evaluate
import pygame
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class MyFigure(FigureCanvas):
    def __init__(self,width, height, dpi):
         # 创建一个Figure,该Figure为matplotlib下的Figure，不是matplotlib.pyplot下面的Figure
        self.fig=plt.figure(figsize=(width, height),dpi=dpi,facecolor='none')
        super(MyFigure,self).__init__(self.fig)
        plt.subplot(111,polar=True)
        self.fig.patch.set_facecolor('red')
        self.fig.patch.set_alpha(0)

class MainWin(QWidget,TEST):
    def __init__ (self,parent=None):
        super(MainWin, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.TurnPage()
        #gkx
        self.F = MyFigure(width=3, height=2, dpi=100)
        self.gridlayout = QGridLayout(self.groupBox)
        self.gridlayout.addWidget(self.F)

    #页面切换
    def TurnPage(self):
        self.Start.clicked.connect(self.on_Start_clicked)
        self.Tool.clicked.connect(self.on_Tool_clicked)
        self.BackHome.clicked.connect(self.on_BackHome_clicked)
        self.BackHome_2.clicked.connect(self.on_BackHome_2_clicked)
        self.BackHome_3.clicked.connect(self.on_BackHome_3_clicked)
        """self.next_1.clicked.connect(self.on_next_1_clicked)
        self.next_2.clicked.connect(self.on_next_2_clicked)
        self.next_3.clicked.connect(self.on_next_3_clicked)
        self.next_4.clicked.connect(self.on_next_4_clicked)
        self.next_5.clicked.connect(self.on_next_5_clicked)
        self.back_2.clicked.connect(self.on_back_2_clicked)
        self.back_3.clicked.connect(self.on_back_3_clicked)
        self.back_4.clicked.connect(self.on_back_4_clicked)
        self.back_5.clicked.connect(self.on_back_5_clicked)
        self.back_6.clicked.connect(self.on_back_6_clicked)"""
        # lzh
        self.PBun_71.clicked.connect(self.on_PBun71_clicked)
        self.PBun_72.clicked.connect(self.on_PBun72_clicked)
        self.PBun_81.clicked.connect(self.on_PBun81_clicked)
        self.PBun_82.clicked.connect(self.on_PBun82_clicked)
        self.PBun_91.clicked.connect(self.on_PBun91_clicked)
        self.PBun_92.clicked.connect(self.on_PBun92_clicked)
        """self.transform_7.clicked.connect(self.on_transform_7_clicked)
        self.transform_8.clicked.connect(self.on_transform_8_clicked)
        self.transform_10.clicked.connect(self.on_transform_10_clicked)"""
        self.mid_to_txt = {}
        self.txt_to_mid = {}
        self.tempofile = {}
        self.ifc1=0
        self.ifc2=0
        self.ifc3=0
        self.ifc4=0
        self.ifc5=0
        self.ifc6=0

        # gkx
        self.initialnote = ""  # 起始音符
        self.generatenote = ""  # 生成音符
        self.saveastxt= {} # 保存的txt文件路径
        self.ifsavedastxt=0
        self.ifsavedasmidi=0
        self.save2midi={}# 保存的midi文件夹路径
        self.midifilename=''
        self.is_switching=False
        self.is_pause=True
        freq = 44100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 1024  # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)



    # lzh
    # txt转mid---选择txt文件
    @pyqtSlot()
    def on_PBun71_clicked(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(),
                                                         "TXT Files(*.txt)")
        if fileName[0]:
            self.Browser_71.setText(fileName[0])
            self.txt_to_mid['file'] = fileName[0]
            self.ifc1=1

    # txt转mid---选择存放文件夹
    @pyqtSlot()
    def on_PBun72_clicked(self):
        dirName = directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", os.getcwd())  # 起始路径
        if dirName:
            self.txt_to_mid['path'] = dirName
            self.Browser_72.setText(dirName)
            self.ifc2=1

    # txt转mid---转换
    @pyqtSlot()
    def on_transform_7_clicked(self):
        if self.ifc1 and self.ifc2 :
            tools.text2midi(self.txt_to_mid['file'], self.txt_to_mid['path'])
            QMessageBox.information(self, "提示", "转换完成",QMessageBox.Yes)
        else:
            QMessageBox.information(self, "提示", "请先点击浏览选择路径",QMessageBox.Yes)


    # mid转txt---选择mid文件
    @pyqtSlot()
    def on_PBun81_clicked(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(),
                                                         "Music Files(*.mid)")
        if fileName[0]:
            self.Browser_81.setText(fileName[0])
            self.mid_to_txt['file'] = fileName[0]
            self.ifc3=1

    # mid转txt---选择存放文件夹
    @pyqtSlot()
    def on_PBun82_clicked(self):
        dirName = directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", os.getcwd())  # 起始路径
        if dirName:
            self.mid_to_txt['path'] = dirName
            self.Browser_82.setText(dirName)
            self.ifc4=1

     # 变速---转换
    @pyqtSlot()
    def on_transform_8_clicked(self):
        if self.ifc3 and self.ifc4:
            tools.midi_to_txt(self.mid_to_txt['file'], self.mid_to_txt['path'])
            QMessageBox.information(self, "提示", "转换完成", QMessageBox.Yes)
        else:
            QMessageBox.information(self, "提示", "请先点击浏览选择路径", QMessageBox.Yes)
    # 变速----选择mid文件
    @pyqtSlot()
    def on_PBun91_clicked(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(),
                                                         "Music Files(*.mid)")
        if fileName[0]:
            self.Browser_91.setText(fileName[0])
            self.tempofile['file'] = fileName[0]
            self.ifc5=1

    # 变速---选择存放文件夹
    @pyqtSlot()
    def on_PBun92_clicked(self):
        dirName = directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", os.getcwd())  # 起始路径
        if dirName:
            self.tempofile['path'] = dirName
            self.Browser_92.setText(dirName)
            self.ifc6=1

     # 变速---按键
    @pyqtSlot()
    def on_transform_10_clicked(self):
        if self.ifc5 and self.ifc6 and self.Edit_10.text():
            tools.tempo_transpose(self.tempofile['file'], self.tempofile['path'], int(self.Edit_10.text()))
            QMessageBox.information(self, "提示", "转换完成", QMessageBox.Yes)
        elif not self.Edit_10.text() and self.ifc6 and self.ifc5:
            QMessageBox.information(self, "提示", "请输入要转换的速度", QMessageBox.Yes)
        else:
            QMessageBox.information(self, "提示", "请先点击浏览选择路径", QMessageBox.Yes)
    @pyqtSlot()
    def on_Start_clicked(self):
        self.stackedWidget.setCurrentIndex(1)
    @pyqtSlot()
    def on_Tool_clicked(self):
        self.stackedWidget.setCurrentIndex(7)
    @pyqtSlot()
    def on_BackHome_clicked(self):
        self.stackedWidget.setCurrentIndex(0)
    @pyqtSlot()
    def on_BackHome_2_clicked(self):
        pygame.mixer.music.pause()
        self.stackedWidget.setCurrentIndex(0)
    @pyqtSlot()
    def on_BackHome_3_clicked(self):
        self.stackedWidget.setCurrentIndex(0)

    # gkx
    @pyqtSlot()
    def on_next_1_clicked(self):
        if self.EditNote.text()!='':
            self.initialnote=self.EditNote.text()
            QMessageBox.information(self, "提示", "生成过程耗时较久，请耐心等待，生成完毕将自动跳转至下一界面",
                                    QMessageBox.Yes)
            self.generatenote=main(self.EditNote.text())#调用generate.main生成音乐
            #self.generatenote=tools.remove_note(self.generatenote)
            self.ShowNotes.setText(self.generatenote)
            self.stackedWidget.setCurrentIndex(2)
            self.EditNote.setText('')
        else:
            QMessageBox.information(self, "提示", "还未输入起始符",QMessageBox.Yes)

    @pyqtSlot()
    def on_SaveT_clicked(self):
        #print('1')
        self.ifsavedastxt=0
        self.saveastxt=QtWidgets.QFileDialog.getOpenFileName(None, "选取文件", os.getcwd(),
                                                         "TXT Files(*.txt)")
        filename_savet=self.saveastxt[0]
        if filename_savet!='':
            f=open(filename_savet,mode='w')
            f.write(self.generatenote)
            f.close()
            self.ifsavedastxt=1
            QMessageBox.information(self, "提示", "保存完成", QMessageBox.Yes)

    @pyqtSlot()
    def on_next_2_clicked(self):
        self.stackedWidget.setCurrentIndex(3)

    @pyqtSlot()
    def on_next_3_clicked(self):
        #gkx
        if self.ifsavedastxt==1:
            matplotlib.rcParams["font.family"] = "SimHei"
            matplotlib.rcParams["font.sans-serif"] = ["SimHei"]
            data = self.evaluate = main_evaluate(self.saveastxt[0])
            nAttr = 6
            labels = np.array(["U检验", 'W检验', 'K检验', '级进-跳进比值检验', '波浪数检验', '调式检验'])
            angles = np.linspace(0, 2 * np.pi, nAttr, endpoint=False)
            data = np.concatenate((data, [data[0]]))
            angles = np.concatenate((angles, [angles[0]]))
            labels = np.concatenate((labels, [labels[0]]))  # 对labels进行封闭
            plt.plot(angles,data,linewidth=2)
            plt.fill(angles, data, facecolor="g", alpha=0.25)
            plt.thetagrids(angles * 180 / np.pi, labels)
            plt.figtext(0.5, 0.9, "综合评价图", ha="center")
            plt.grid(True)
            self.stackedWidget.setCurrentIndex(4)
        else:
            QMessageBox.information(self, "提示", "请先保存为txt文件", QMessageBox.Yes)



    @pyqtSlot()
    def on_next_4_clicked(self):
        self.stackedWidget.setCurrentIndex(5)

    #gkx
    @pyqtSlot()
    def on_SaveM_clicked(self):
        self.ifsavedasmidi=0
        dirName_saveasmidi= QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", os.getcwd())  # 起始路径
        if dirName_saveasmidi:
            self.save2midi['path'] = dirName_saveasmidi
            tools.text2midi(self.saveastxt[0],self.save2midi['path'])
            self.ifsavedasmidi=1
            QMessageBox.information(self, "提示", "保存完成", QMessageBox.Yes)

    @pyqtSlot()
    def on_play_pause_clicked(self):

        if  self.is_pause and (not self.is_switching):
            pygame.mixer.music.play()
            self.is_pause=False
            #x=int(pygame.mixer.music.get_pos())
            #self.horizontalSlider.setValue(x)
        elif (not self.is_pause) and (not self.is_switching):
            pygame.mixer.music.pause()
            self.is_pause=True
            self.is_switching=True
            #x = int(pygame.mixer.music.get_pos())
            #self.horizontalSlider.setValue(x)
        elif (self.is_pause) and self.is_switching:
            pygame.mixer.music.unpause()
            self.is_pause=False
            self.is_switching=False
            #x = int(pygame.mixer.music.get_pos())
            #self.horizontalSlider.setValue(x)

            

    @pyqtSlot()
    def on_next_5_clicked(self):
        if self.ifsavedasmidi==1:
            a = self.saveastxt[0]
            b = self.save2midi['path']
            self.midifilename = b + '/' + a[len(os.path.dirname(a)) + 1:].split('.')[0] + 'to_mid.mid'
            pygame.mixer.music.set_volume(0.8)
            clock = pygame.time.Clock()
            try:
                pygame.mixer.music.load(self.midifilename)
                print("Music file %s loaded!" % self.midifilename)
            except pygame.error:
                print("File %s not found! (%s)" % (self.midifilename, pygame.get_error()))
                return
            self.stackedWidget.setCurrentIndex(6)
        else:
            QMessageBox.information(self, "提示", "请先保存为midi文件", QMessageBox.Yes)

    def sliderChange(self,val):
        pygame.mixer.music.set_pos(int(val*1000))


    @pyqtSlot()
    def on_back_2_clicked(self):
        self.stackedWidget.setCurrentIndex(1)

    @pyqtSlot()
    def on_back_3_clicked(self):
        self.stackedWidget.setCurrentIndex(2)

    @pyqtSlot()
    def on_back_4_clicked(self):
        self.stackedWidget.setCurrentIndex(3)

    @pyqtSlot()
    def on_back_5_clicked(self):
        self.stackedWidget.setCurrentIndex(4)

    @pyqtSlot()
    def on_back_6_clicked(self):
        self.stackedWidget.setCurrentIndex(5)


if __name__ == "__main__":

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWin = TitleWin(widget_2_sub=MainWin())
    myWin.show()
    sys.exit(app.exec_())


