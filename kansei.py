import tkinter as tk
import ctypes
import sp_clinet
import threading
import configparser

class Screen():

    def __init__(self,root):
        self.root=root
        self.width=1920
        self.height=1080
        self.root.resizable(width=False,height=False)
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        self.ip = "192.168.250.132"

        self.flag = False


    def main_frame(self):
        self.root.title("test")
        self.root.geometry(f"{self.width}x{self.height}")

        var=tk.IntVar(self.root)

        ###次の2つはラジオボタン###
        select_f1=tk.Frame(self.root,
                  width=350,
                  height=150,
                  bg="red")
        select_f1.place(x=190,y=50)
        auto_mode1=tk.Radiobutton(select_f1,text="自動",font=("normal",60),value=1,var=var)
        auto_mode1.place(relwidth=1.0,relheight=1.0)
        
        select_f2=tk.Frame(self.root,
                  width=350,
                  height=150,
                  bg="red")
        select_f2.place(x=190,y=250)
        auto_mode2=tk.Radiobutton(select_f2,text="遠隔",font=("normal",60),value=2,var=var)
        auto_mode2.place(relwidth=1.0,relheight=1.0)

        ###画像###
        self.select_img = tk.Frame(self.root,
                  width=480,
                  height=360,
                  bg="red")
        self.select_img.place(x=720,y=50)
        self.flag = True
        # self.canvas = tk.Canvas(select_img,width=480,height=360,bg="blue")
        # self.canvas.place(x=0,y=0)
        # self.img = tk.PhotoImage(file = "testimg.png",
        #                     width=480,
        #                     height=360,)
        # self.canvas.create_image(0, 0,anchor=tk.NW, image = self.img)

        ###実行中の動作の表示###
        select_f3=tk.Frame(self.root,
                  width=360,
                  height=270,
                  bg="red")
        select_f3.place(x=1380,y=70)
        text1=tk.Label(select_f3,text="実行中の動作\nを表示します",font=("normal",40))
        text1.place(relwidth=1.0,relheight=1.0)
        ###実際に表示させる文(無名関数)###
        def check(a):
            if a==1:
                b="左旋回中"
                self.window.send_command("left")
            elif a==2:
                b="前進中"
                self.window.send_command("forward")
            elif a==3:
                b="後退中"
                self.window.send_command("back")
            elif a==4:
                b="右旋回中"
                self.window.send_command("right")
            text1=tk.Label(select_f3,text=b,font=("normal",60))###textをbにする###
            text1.place(relwidth=1.0,relheight=1.0)

        ###左ボタン###
        select_f4=tk.Frame(self.root,
                  width=400,
                  height=400,
                  bg="red")
        select_f4.place(x=150,y=550)
        auto_mode5=tk.Button(select_f4,text="左旋回",font=("normal",60),command=lambda:check(1))
        auto_mode5.place(relwidth=1.0,relheight=1.0)

        ###前進ボタン###
        select_f5=tk.Frame(self.root,
                  width=350,
                  height=100,
                  bg="red")
        select_f5.place(x=700,y=550)
        auto_mode6=tk.Button(select_f5,text="前進",font=("normal",60),command=lambda:check(2))
        auto_mode6.place(relwidth=1.0,relheight=1.0)

        ###後退ボタン###
        select_f6=tk.Frame(self.root,
                  width=350,
                  height=100,
                  bg="red")
        select_f6.place(x=700,y=750)
        auto_mode7=tk.Button(select_f6,text="後退",font=("normal",60),command=lambda:check(3))
        auto_mode7.place(relwidth=1.0,relheight=1.0)

        ###スケールメーター###
        select_f7=tk.Frame(self.root,
                  width=100,
                  height=300,
                  bg="red")
        select_f7.place(x=1150,y=550)
        auto_mode8=tk.Scale(select_f7,from_=100,to=0,tickinterval=10,)
        auto_mode8.place(relwidth=1.5,relheight=1.0)

        ###右ボタン###
        select_f8=tk.Frame(self.root,
                  width=400,
                  height=400,
                  bg="red")
        select_f8.place(x=1380,y=550)
        auto_mode9=tk.Button(select_f8,text="右旋回",font=("normal",60),command=lambda:check(4))
        auto_mode9.place(relwidth=1.0,relheight=1.0)

    def rec(self):
        while True:    
            if self.flag:
                self.window = sp_clinet.Window(self.root,self.select_img,480,360)
                break

    def fin(self):
        self.window.close()




def main():
    root=tk.Tk()
    screen=Screen(root=root)
    screen.main_frame()
    screen.rec()
    thread = threading.Thread(target=screen.rec)
    thread.start()
    root.mainloop()
    thread.join()
    screen.fin()


if __name__=="__main__":
    main()