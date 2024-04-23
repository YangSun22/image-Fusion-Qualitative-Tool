import sys, cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene
from PyQt5.QtGui import QPixmap, QImage
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
import Ui_image_tools
import os
import math
import numpy as np

class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.ui = Ui_image_tools.Ui_MainWindow()
        self.ui.setupUi(self)
        # 定义菜单open打开图片
        #self.ui.Save_button.clicked.connect(self.open2show)
        self.ui.graphicsView.installEventFilter(self) 
        #root_dir="imgs\\VIS_MEF_ISO\\"
        root_dir = "imgs\\ATT_ATTMAP\\select"   
       # root_dir="imgs\\Scale_Shift\\"
        self.img_H = 0
        self.img_W = 0
        self.i = 0
        data_name = 'MandP' #'LLVIP_New'#'MEF'
        self.temp_name ='13-ResConv_Upsample_NewLoader_negSobel_MulitTask_448_1107En_Scale_3_Shift_0'
        self.method_list,self.img_list=self.getimglist(root_dir,data_name)
        print(self.method_list,self.img_list)
        self.showImage(self.method_list,self.img_list[0])
        self.points = []
        self.save_dir = "savedir\\"          #默认保存地址，Win系统
        self.ui.before_button.clicked.connect(self.changeimageAfter)
        self.ui.after_button.clicked.connect(self.changeimageBefore)
        self.ui.SavePath.setText(self.save_dir)
        self.ui.Save_button.clicked.connect(self.saveimg)

    def changeimageAfter(self):
        self.i = self.i -1
        print("self.i",self.i)
        self.showImage(self.method_list,self.img_list[self.i])

    def changeimageBefore(self):
        self.i = self.i +1
        print("self.i",self.i)
        self.showImage(self.method_list,self.img_list[self.i])
    
    def saveimg(self):
        save_dir = self.ui.SavePath.text()
        
        
        img_name = self.img_list[self.i].replace('.','_')
        save_dir = os.path.join(save_dir, img_name)
        print("save_dir:",save_dir)
        #获得源图像
        if len(self.points)==4:
            
            x0 = int(min(self.points[0][0],self.points[1][0]))
            y0 =int( min(self.points[0][1],self.points[1][1]))
            x1 = int( max(self.points[0][0],self.points[1][0]))
            y1 = int( max(self.points[0][1],self.points[1][1]))

            x2 = int(min(self.points[2][0],self.points[3][0]))
            y2 =int( min(self.points[2][1],self.points[3][1]))
            x3 = int( max(self.points[2][0],self.points[3][0]))
            y3 = int( max(self.points[2][1],self.points[3][1]))
        # img_tensor_list = []
            for m in self.method_list:
                if m != "None":
                    img_dir = os.path.join(m, self.img_list[self.i])
                    #print(img_dir)
                    try:
                        if "DeFusion" in img_dir:
                            img_dir = img_dir.split(".")[0] + ".jpg"
                        img = cv2.imread(img_dir)
                        img = cv2.rectangle(img,(x0,y0) , (x1,y1), (0, 0, 255), 2)
                        img = cv2.rectangle(img,(x2,y2) , (x3,y3), (0, 0, 255), 2)
                        img_part = img[y0+2:y1-1,x0+2:x1-1]
                        img_part2 = img[y2+2:y3-1,x2+2:x3-1]
                    except:
                        method_name = m.split("\\")[-1]
                        img_name = self.img_list[self.i].split(".")[0][:-2]
                        #print(img_name)
                        ext = self.img_list[self.i].split(".")[1]
                        img_name_temp = img_name+"_"+method_name+"."+ext
                        img_dir = os.path.join(m, img_name_temp)
                       # print(img_dir)
                        img = cv2.imread(img_dir)
                        img = cv2.rectangle(img,(x0,y0) , (x1,y1), (0, 0, 255), 2)
                        img = cv2.rectangle(img,(x2,y2) , (x3,y3), (0, 0, 255), 2)
                        img_part = img[y0+2:y1-1,x0+2:x1-1]
                        img_part2 = img[y2+2:y3-1,x2+2:x3-1]
                    # try:
                    #     img = cv2.imread(img_dir)
                    #     img = cv2.rectangle(img,(x0,y0) , (x1,y1), (0, 0, 255), 2)
                    #     img = cv2.rectangle(img,(x2,y2) , (x3,y3), (0, 0, 255), 2)
                    #     img_part = img[y0+2:y1-1,x0+2:x1-1]
                    #     img_part2 = img[y2+2:y3-1,x2+2:x3-1]
                    # except:
                    #     img_name= 
                    #     img_dir = os.path.join(m, self.img_list[self.i].replace('_B.', '.'))
                    #     print(img_dir)
                    #     img = cv2.imread(img_dir)
                    #     img = cv2.rectangle(img,(x0,y0) , (x1,y1), (0, 0, 255), 2)
                    #     img = cv2.rectangle(img,(x2,y2) , (x3,y3), (0, 0, 255), 2)
                    #     img_part = img[y0+2:y1-1,x0+2:x1-1]
                    #     img_part2 = img[y2+2:y3-1,x2+2:x3-1]
                    m= m.split('\\')
                    if len(m)==2:
                        m = m[-1]
                    else:
                        m = m[2]
                    out_name = m.replace('/','_') + ".jpg"
                    out_part_name = m.replace('/','_') + "_part.jpg"
                    out_part2_name = m.replace('/','_') + "_part2.jpg"
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)
                    print(os.path.join(save_dir, out_name))
                    #print(img.shape)
                    cv2.imwrite(os.path.join(save_dir, out_name), img,[int(cv2.IMWRITE_JPEG_QUALITY),100])
                    cv2.imwrite(os.path.join(save_dir, out_part_name), img_part,[int(cv2.IMWRITE_JPEG_QUALITY),100])
                    cv2.imwrite(os.path.join(save_dir, out_part2_name), img_part2,[int(cv2.IMWRITE_JPEG_QUALITY),100])
            print("Save img, Done!")
           # cvimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        elif len(self.points)==0:
             for m in self.method_list:
                if m != "None":
                    img_dir = os.path.join(m, self.img_list[self.i])
                    #print(img_dir)
                    img = cv2.imread(img_dir)
                    # img = cv2.rectangle(img,(x0,y0) , (x1,y1), (0, 0, 255), 2)
                    # img = cv2.rectangle(img,(x2,y2) , (x3,y3), (0, 0, 255), 2)
                    # img_part = img[y0+2:y1-1,x0+2:x1-1]
                    # img_part2 = img[y2+2:y3-1,x2+2:x3-1]
                    m= m.split('\\')
                    if len(m)==2:
                        m = m[-1]
                    else:
                        m = m[2]
                    out_name = m.replace('/','_') + ".jpg"
                    # out_part_name = m.replace('/','_') + "_part.jpg"
                    # out_part2_name = m.replace('/','_') + "_part2.jpg"
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)
                    print(os.path.join(save_dir, out_name))
                    print(img.shape)
                    cv2.imwrite(os.path.join(save_dir, out_name), img,[int(cv2.IMWRITE_JPEG_QUALITY),100])
                    # cv2.imwrite(os.path.join(save_dir, out_part_name), img_part,[int(cv2.IMWRITE_JPEG_QUALITY),100])
                    # cv2.imwrite(os.path.join(save_dir, out_part2_name), img_part2,[int(cv2.IMWRITE_JPEG_QUALITY),100])
             print("Save img, Done!")
            #img_tensor_list.append(cvimg)
       



    def eventFilter(self, watched, event):    
        """重写eventfilter事件"""
        #print("1",event.type(),QtCore.QEvent.MouseButtonPress)
        if event.type() == QtCore.QEvent.MouseButtonPress:
            #print("2",event.button(),QtCore.Qt.LeftButton,watched,self.ui.graphicsView)
            if event.button() == QtCore.Qt.LeftButton and watched == self.ui.graphicsView:
               # print("3",event.button(),self.ui.graphicsView.GetPoints())
                ps = self.ui.graphicsView.GetPoints()
                
                if len(ps) != 0:
                    nowp = ps[-1]
                    print("影像选点测试,影像上一个点第" +
                                 str(len(ps)) +
                                 "个点,坐标为:(" +
                                 str('%.3f'%nowp[0]) + ", " +
                                 str('%.3f'%nowp[1]) + ")")
                    if len(ps)==2:
                        self.points = ps
                        x0 = min(self.points[0][0],self.points[1][0])
                        y0 = min(self.points[0][1],self.points[1][1])
                        x1 =  max(self.points[0][0],self.points[1][0])
                        y1 =  max(self.points[0][1],self.points[1][1])
                        self.ui.x0.setText(str(x0))
                        self.ui.x1.setText(str(x1))
                        self.ui.y0.setText(str(y0))
                        self.ui.y1.setText(str(y1))
           
        return False

    def getimglist(self,root_dir="./imgs",data_name = 'MEF'):
        method_list = []
        img_list = []
        #temp_name = '13-MMoE_Base'
        #temp_name = '13-MMoE_Base'
       
        data_name = data_name
        for method in os.listdir(root_dir):
            method_dir = os.path.join(root_dir, method)
            if len(os.listdir(method_dir))<10:
                method_dir = os.path.join(method_dir, data_name)
                method_list.append(method_dir)
            else:
                method_list.append(method_dir)
            if method==self.temp_name:
                for file in os.listdir(method_dir):
                    img_list.append(file)
        return method_list,img_list
    
    def showImage(self,method_list,img_name_i):
        img_tensor_list = []
        for m in method_list:
            if m !="None":
                img_dir = os.path.join(m, img_name_i)
                print(img_dir)
                try:
                    if "DeFusion" in img_dir:
                        img_dir = img_dir.split(".")[0] + ".jpg"
                    img = cv2.imread(img_dir)
                    cvimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                except:
                    method_name = m.split("\\")[-1]
                    img_name = img_name_i.split(".")[0][:-2]
                    print(img_name)
                    ext = img_name_i.split(".")[1]
                    img_name_temp = img_name+"_"+method_name+"."+ext
                    img_dir = os.path.join(m, img_name_temp)
                    print(img_dir)
                    img = cv2.imread(img_dir)
                    #print(img)
                    cvimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                #print(img)
                #cvimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img_tensor_list.append(cvimg)
        list_len = len(img_tensor_list)
        H = int(list_len**0.5)
        W = math.ceil((list_len/H))
        print(list_len,H,W)
        for i in range(H*W-list_len):
            img_tensor_list.append(np.zeros(img_tensor_list[0].shape))
            if len(method_list)!=H*W:
               method_list.append("None")
            print(method_list)
        img_H,img_W,_ = img_tensor_list[0].shape
        self.img_H,self.img_W = img_H,img_W
        img_np = np.array(img_tensor_list)
        img_np = img_np.reshape((H,W,img_H,img_W,3))
        img_np = img_np.transpose(0,2,1,3,4).reshape((H*img_H,W*img_W,3))

        

        self.ui.graphicsView.SetImage(img_np,img_H,img_W,method_list)
        self.ui.RootPath.setText(img_name_i)
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = mainWindow()
   # ui = Ui_image_tools.Ui_MainWindow()
   # ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())