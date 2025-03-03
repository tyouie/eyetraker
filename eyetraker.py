#-*- coding: cp950 -*-
import pygame
import time
import cv2
import datetime
import os
import tkinter as tk
from tkinter import simpledialog, messagebox

def getuser():
    UserName=input("input username : ")
    return UserName


# ���I�Ѽ�
DOT_RADIUS = 10
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# ��l���ṳ�Y
def setup_camera(camera_id, width=640, height=480):
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print(f"�L�k���}�ṳ�Y {camera_id}")
        return None
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return cap

# �Ыؼv���O�s��Ƨ�
def create_output_dir(UserName):
    output_dir = r"C:/Users/wegrty/source/repos/eyetraker/eyetraker/user/"+UserName
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

# ���I�{�{�P���s��X
def flash_and_record(positions,screen,font,WIDTH,HEIGHT,cap, writer, game_writer, output_dir):
    times=0
    for pos in positions:
        # �ˬd�O�_�h�X
        if times==9:
            break
            #return False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                   break

        # �e���I
        screen.fill(BLACK)
        pygame.draw.circle(screen, RED, pos, DOT_RADIUS)
        coord_text = font.render(f"Coordinates: {pos[0]}, {pos[1]}", True, WHITE)
        screen.blit(coord_text, (20, 20))
        pygame.display.flip()

        # ��l�Ƽv�����W
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        video_path = os.path.join(output_dir, f"tracking_{timestamp}.avi")
        game_video_path = os.path.join(output_dir, f"game_{timestamp}.avi")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        frame_rate = 30
        frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                      int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        writer.open(video_path, fourcc, frame_rate, frame_size)
        game_writer.open(game_video_path, fourcc, frame_rate, (WIDTH, HEIGHT))

        # �}�l���s���I��ܴ���
        start_time = time.time()
        while time.time() - start_time < 3:  # 3����s�ɶ�
            # ���s�ṳ�Y�e��
            ret, frame = cap.read()
            if not ret:
                print("�L�kŪ���ṳ�Y�e���I")
                break
            frame = cv2.flip(frame, 1)  # �蹳�e��
            writer.write(frame)

             #���s�C���e��
            #game_surface = pygame.surfarray.array3d(screen)
            #game_frame = cv2.cvtColor(game_surface.swapaxes(0, 1), cv2.COLOR_RGB2BGR)
            #game_writer.write(game_frame)

        # �M�����I�õ���
        writer.release()
        game_writer.release()
        screen.fill(BLACK)
        pygame.display.flip()
        time.sleep(2)  # 2���j
        times+=1
        print(times)
    return True

# �D�{��
def main(output_dir):
    # ��l���ṳ�Y
    camera_id = 0
    cap = setup_camera(camera_id)
    if not cap:
        print("�ṳ�Y��l�ƥ��ѡI")
        return

    print(output_dir)
    writer = cv2.VideoWriter()
    game_writer = cv2.VideoWriter()

    
    # ��l�� pygame
    pygame.init()
    # �]�w���ù��Ҧ�

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN,display=0)#display =1
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Red Dot Tracker")
    print(WIDTH,HEIGHT)

    # ���I����m
    positions = [
        (WIDTH // 4, HEIGHT // 4),  # ���W
        (WIDTH // 2, HEIGHT // 4),  # �W��
        (3 * WIDTH // 4, HEIGHT // 4),  # �k�W
        (WIDTH // 4, HEIGHT // 2),  # ����
        (WIDTH // 2, HEIGHT // 2),  # ����
        (3 * WIDTH // 4, HEIGHT // 2),  # ���k
        (WIDTH // 4, 3 * HEIGHT // 4),  # ���U
        (WIDTH // 2, 3 * HEIGHT // 4),  # �U��
        (3 * WIDTH // 4, 3 * HEIGHT // 4),  # �k�U
    ]

    # �r��]�w
    font = pygame.font.SysFont(None, 36)

    running = True
    try:
        flash_and_record(positions,screen,font,WIDTH,HEIGHT,cap, writer, game_writer, output_dir)

    except KeyboardInterrupt:
        print("�{���Q���_")

    finally:
        cap.release()
        writer.release()
        game_writer.release()
        pygame.quit()


# GUI �ɭ�
class gui:
    def __init__(self, root):
        self.root = root
        self.root.title("Face ID System")
        self.root.geometry("300x250")

        # ���U���s
        self.start_button = tk.Button(root, text="�}�l�շ�", command=self.mainfunc, width=20, height=2)
        self.start_button.pack(pady=10)
        #exit
        self.exit_button = tk.Button(root, text="�h�X", command=root.quit, width=20, height=2)
        self.exit_button.pack(pady=10)
    def mainfunc(self):
        user_name = simpledialog.askstring("���U", "�п�J�ϥΪ̦W�١G")
        if user_name:
            output_dir=create_output_dir(user_name)
            main(output_dir)

if __name__ == "__main__":
    root = tk.Tk()
    app = gui(root)
    root.mainloop()
#    main()
