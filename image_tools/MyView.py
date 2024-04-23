# yangzhen
# 2021.12.04
 
 
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw
import numpy as np
import copy
import PyQt5
 
class MyQGraphicsView(qw.QGraphicsView):
    def __init__(self, parent):
        super(MyQGraphicsView, self).__init__(parent)
        self.setMouseTracking(True)
 
        self.points = [] # 选择的点
        self.points_item =[]
        self.startpos = qc.QPoint(0, 0) # 鼠标中键按下时起始点
        self.endpos = qc.QPoint(0, 0) # 鼠标中键弹起时终点
        self.scalenum = 1 # 缩放系数
        # self.scaleflag = 0 # 放大还是缩小(0:不动，1:放大，-1:缩小)
        self.nposx = 0 # 视图移动参数x
        self.nposy = 0 # 视图移动参数y
        # self.mindex = 1 # 当前区域编号
        self.flag = 0 # 是否进行选点的flag
        self.linkflag = 0 # 是否进行联动
        #self.setAttribute(PyQt5.WA_NoMousePropagation, False)
 
   
 
    def InitializeView(self):
        """View初始化"""
        self.points.clear()
        self.allpoints.clear()
        self.flag = 0
        self.scalenum = 1
        self.setCursor(qc.Qt.ArrowCursor)
 
    def SetChoosePoint(self, flag):
        """设置是否选点"""
        self.flag = flag
        if flag == 0:
            self.setCursor(qc.Qt.ArrowCursor)
        if flag == 1 or flag == 2:
            self.setCursor(qc.Qt.CrossCursor)
 
    def GetFlag(self):
        """获取当前是在做什么"""
        return self.flag
 
    def GetPoints(self):
        """获取点集"""
        return self.points
 
    def ClearPoints(self):
        """删除点集"""
        self.points.clear()
 
     
 
    def PersentLiner(self, data, ratio):
        mdata = data.copy()
        rows, cols = data.shape[0:2]
        counts = rows*cols
        mdata = mdata.reshape(counts, 1)
        tdata = np.sort(mdata, axis=0)
        cutmin = tdata[int(counts*ratio), 0]
        cutmax = tdata[int(counts*(1-ratio)), 0]
        ndata = 255.0*(data.astype(np.float32) - cutmin)/float(cutmax-cutmin)
        ndata[data < cutmin] = 0
        ndata[data > cutmax] = 255
        return ndata
 
    def SetImage(self, data,imgH,imgW,Method_list):
        """设置影像"""
        # if (data.type() == )
        self.ClearPoints()
        for item in self.points_item:
            self.scene.removeItem(item)
        self.imgH =imgH
        self.imgW =imgW
        
        rows, cols, depth = data.shape
        self.H = rows
        self.W = cols
        # 如果通道数大于3个,只保留前边三个通道
        if depth > 3:
            img = data[:, :, 0:3].copy()
            img = img[:, :, ::-1]
        else:
            img = data.copy()
        rows, cols, depth = img.shape
        # 如果不是uint8的数据，需要先拉伸
        img = img.astype(np.uint8)
        print(img)
        dtp = img.dtype
        if dtp != np.uint8:
            print("Not int 8")
            for i in range(depth):
                img[:,:,i] = self.PersentLiner(img[:,:,i].copy(), 0.02)
            img = img.astype(np.uint8)
        # numpy矩阵转换成QImage
        if depth == 3:
            nimg = qg.QImage(img.data, cols, rows, cols*depth,\
                             qg.QImage.Format_RGB888)
        elif depth == 2:
            b1 = np.float32(img[:, :, 0])
            b2 = np.float32(img[:, :, 1])
            img = np.uint8((b1+b2)/2.)
            nimg = qg.QImage(img.data, cols, rows, cols*depth,\
                             qg.QImage.Format_Grayscale8)
        elif depth == 1:
            nimg = qg.QImage(img.data, cols, rows, cols*depth,\
                             qg.QImage.Format_Grayscale8)
        pix = qg.QPixmap.fromImage(nimg)
        item = qw.QGraphicsPixmapItem(pix)
        
        showscene = qw.QGraphicsScene()
        showscene.addItem(item)         
        self.setScene(showscene)
        self.scene = showscene
        self.setTransform(qg.QTransform())

        # 添加文本
        font = qg.QFont("Roman times", 20, qg.QFont.Bold)
        H_len = self.H//self.imgH
        #print(self.H,self.imgH,H_len)
        W_len = self.W//self.imgW
        #print(self.W,self.imgW,W_len)
        #print(x0,y0,w,h)
        for i in range(H_len):
            for j in range(W_len):
                x = j*self.imgW
                y = i*self.imgH
                #print(x,y,H_len,W_len,i*H_len + j)
                method_name = Method_list[i*W_len + j]
                if len(method_name)>30:
                     method_name =  method_name[-30:]
                text = qw.QGraphicsTextItem(method_name)
                text.setPos(x, y)
                text.setDefaultTextColor(qg.QColor(248, 201, 0))
                text.setFont(font)
                self.scene.addItem(text)
        
        
    
    def wheelEvent(self, event):
        if (event.angleDelta().y() > 0.5):
            self.scale(1.3, 1.3)
            self.scalenum = self.scalenum * 1.3
            # self.scaleflag = 1
        elif (event.angleDelta().y() < 0.5):
            self.scale(1/1.3, 1/1.3)
            # self.scaleflag = -1
            self.scalenum = self.scalenum / 1.3
        if self.linkflag == 1:
            self.linkwidget.SetLinkPara(self.GetLinkPara())
 
    def mousePressEvent(self, event):
        print("Press!")
        button = event.button()
        modifier = event.modifiers()
        # 按住ctrl时变更鼠标样式
        if button == qc.Qt.RightButton:
            self.setCursor(qc.Qt.PointingHandCursor)
            self.startpos = self.mapToScene(event.pos())
           # print(self.startpos)
        elif button == qc.Qt.LeftButton :
            p = self.mapToScene(event.pos())
            #print(p)
            new_x = p.x()%(self.imgW)
            new_y = p.y()%(self.imgH)
            new_p = [new_x,new_y]
            #print(new_p)
            pen = qg.QPen()
            pen.setColor(qg.QColor(255, 0, 0))
            pen.setWidth(2)
            if len(self.points)==4:
                self.ClearPoints()
                for item in self.points_item:
                    self.scene.removeItem(item)
                #self.scene.clear()
            
            self.points.append(new_p)
            # 画点
            if len(self.points)%2==0:
                str_pos = len(self.points)-2
                x0 = min(self.points[str_pos][0],self.points[str_pos+1][0])
                y0 = min(self.points[str_pos][1],self.points[str_pos+1][1])
                w = max(self.points[str_pos][0],self.points[str_pos+1][0])-min(self.points[str_pos][0],self.points[str_pos+1][0])
                h = max(self.points[str_pos][1],self.points[str_pos+1][1])-min(self.points[str_pos][1],self.points[str_pos+1][1])
                H_len = self.H//self.imgH
                #print(self.H,self.imgH,H_len)
                W_len = self.W//self.imgW
                #print(self.W,self.imgW,W_len)
                #print(x0,y0,w,h)
                for i in range(H_len):
                    for j in range(W_len):
                        x = x0 +j*self.imgW
                        y = y0 +i*self.imgH
                        #print(x,y,w,h)
                        item = self.scene.addRect(x,y,w,h, pen)
                        self.points_item.append(item)
            
            
        event.ignore()
        # 鼠标右键完成当前区域选点
    
 
    
    def mouseReleaseEvent(self, event):
        button = event.button()
        modifier = event.modifiers()
        # 鼠标中键弹起时进行视图移动
        if button == qc.Qt.RightButton:
            # 变更鼠标样式
            if self.flag == 0:
                self.setCursor(qc.Qt.ArrowCursor)
            elif self.flag == 1 or self.flag == 2:
                self.setCursor(qc.Qt.CrossCursor)
            # 记录当前点进行视图移动
            self.endpos = self.mapToScene(event.pos())
            # 获取滚动条当前位置
            oposx = self.horizontalScrollBar().value()
            oposy = self.verticalScrollBar().value()
            # 计算鼠标移动的距离
            offset = self.endpos - self.startpos
            # 根据移动的距离计算新的滚轮位置
            nposx = oposx - offset.x()*self.scalenum
            nposy = oposy - offset.y()*self.scalenum
            # 设置新的滚轮位置
            self.horizontalScrollBar().setValue(nposx)
            self.verticalScrollBar().setValue(nposy)
            # 记录一下备用
            self.nposx = nposx
            self.nposy = nposy
            # # 进行联动
            # if self.linkflag == 1:
            #     self.linkwidget.SetLinkPara(self.GetLinkPara())