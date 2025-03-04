from mimetypes import init
import pygame
import time
import cv2
import datetime
import os
import tkinter as tk
from tkinter import simpledialog, messagebox,filedialog

def getuser():
    UserName=input("input username : ")
    return UserName


# 紅點參數
DOT_RADIUS = 10
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# 初始化攝像頭
def setup_camera(camera_id, width=640, height=480):
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print(f"無法打開攝像頭 {camera_id}")
        return None
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return cap

# 創建影片保存資料夾
def create_output_dir(UserName,filepath):
    output_dir = filepath+"/"+UserName
    print(output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    #return output_dir

# 紅點閃爍與錄製整合
def flash_and_record(positions,screen,font,WIDTH,HEIGHT,cap, writer, game_writer, output_dir,exper):
    times=0
    for pos in positions:
        # 檢查是否退出
        if times==9:
            break
            #return False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                   break

        # 畫紅點
        screen.fill(BLACK)
        pygame.draw.circle(screen, RED, pos, DOT_RADIUS)
        coord_text = font.render(f"Coordinates: {pos[0]}, {pos[1]}", True, WHITE)
        screen.blit(coord_text, (20, 20))
        pygame.display.flip()

        # 初始化影片文件名
        #timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        video_path = os.path.join(output_dir, f"tracking_{exper}_{times}.avi")
        game_video_path = os.path.join(output_dir, f"game_{exper}_{times}.avi")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        frame_rate = 30
        frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                      int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        writer.open(video_path, fourcc, frame_rate, frame_size)
        game_writer.open(game_video_path, fourcc, frame_rate, (WIDTH, HEIGHT))

        # 開始錄製紅點顯示期間
        start_time = time.time()
        while time.time() - start_time < 3:  # 3秒錄製時間
            # 錄製攝像頭畫面
            ret, frame = cap.read()
            if not ret:
                print("無法讀取攝像頭畫面！")
                break
            frame = cv2.flip(frame, 1)  # 鏡像畫面
            writer.write(frame)

             #錄製遊戲畫面
            #game_surface = pygame.surfarray.array3d(screen)
            #game_frame = cv2.cvtColor(game_surface.swapaxes(0, 1), cv2.COLOR_RGB2BGR)
            #game_writer.write(game_frame)

        # 清除紅點並等待
        writer.release()
        game_writer.release()
        screen.fill(BLACK)
        pygame.display.flip()
        time.sleep(2)  # 2秒間隔
        times+=1
        print(times)
    return True

# 主程式
def main(output_dir,expertimes):
    # 初始化攝像頭
    camera_id = 0
    cap = setup_camera(camera_id)
    if not cap:
        print("攝像頭初始化失敗！")
        return

    print(output_dir)
    writer = cv2.VideoWriter()
    game_writer = cv2.VideoWriter()

    
    # 初始化 pygame
    pygame.init()
    # 設定全螢幕模式

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN,display=0)#display =1
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Red Dot Tracker")
    print(WIDTH,HEIGHT)

    # 紅點的位置
    positions = [
        (WIDTH // 4, HEIGHT // 4),  # 左上
        (WIDTH // 2, HEIGHT // 4),  # 上中
        (3 * WIDTH // 4, HEIGHT // 4),  # 右上
        (WIDTH // 4, HEIGHT // 2),  # 中左
        (WIDTH // 2, HEIGHT // 2),  # 中心
        (3 * WIDTH // 4, HEIGHT // 2),  # 中右
        (WIDTH // 4, 3 * HEIGHT // 4),  # 左下
        (WIDTH // 2, 3 * HEIGHT // 4),  # 下中
        (3 * WIDTH // 4, 3 * HEIGHT // 4),  # 右下
    ]

    # 字體設定
    font = pygame.font.SysFont(None, 36)

    running = True
    try:
        flash_and_record(positions,screen,font,WIDTH,HEIGHT,cap, writer, game_writer, output_dir,expertimes)

    except KeyboardInterrupt:
        print("程式被中斷")

    finally:
        cap.release()
        writer.release()
        game_writer.release()
        pygame.quit()


# GUI 界面
class gui:
    def __init__(self, root):
        self.root = root
        self.root.title("Face ID System")
        self.root.geometry("300x250")

        # 註冊按鈕
        self.start_button = tk.Button(root, text="開始校準", command=self.mainfunc, width=20, height=2)
        self.start_button.pack(pady=10)
        #creat new user file
        self.CreatUser_button=tk.Button(root, text="creat user file", command=self.CreactUserFile, width=20, height=2)
        self.CreatUser_button.pack(pady=10)
        #exit
        self.exit_button = tk.Button(root, text="退出", command=root.quit, width=20, height=2)
        self.exit_button.pack(pady=10)
    def mainfunc(self):
        
        FilePath=filedialog.askdirectory(parent=self.root,initialdir=r"C:/Users/wegrty/source/repos/eyetraker/")
        expertimes= simpledialog.askstring("", "請輸入第幾次試驗：")
        if FilePath :
            main(FilePath,expertimes)
        else:
            messagebox.showinfo("Warning","請選取目錄")
    def CreactUserFile(self):
        user_name = simpledialog.askstring("creact new user", "請輸入使用者名稱：")
        filepath=filedialog.askdirectory(parent=self.root,initialdir=r"C:/Users/wegrty/source/repos/eyetraker/")
        if user_name:
            create_output_dir(user_name,filepath)
            #main(output_dir)

if __name__ == "__main__":
    root = tk.Tk()
    app = gui(root)
    root.mainloop()
#    main()
