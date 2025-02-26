import pygame
import time
import cv2
import datetime
import os

# 初始化 pygame
pygame.init()

# 設定全螢幕模式

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN,display=1)
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

# 紅點參數
DOT_RADIUS = 10
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 字體設定
font = pygame.font.SysFont(None, 36)

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
def create_output_dir():
    output_dir = r"E:/eyeErack/Point"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

# 紅點閃爍與錄製整合
def flash_and_record(cap, writer, game_writer, output_dir):
    for pos in positions:
        # 檢查是否退出
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False

        # 畫紅點
        screen.fill(BLACK)
        pygame.draw.circle(screen, RED, pos, DOT_RADIUS)
        coord_text = font.render(f"Coordinates: {pos[0]}, {pos[1]}", True, WHITE)
        screen.blit(coord_text, (20, 20))
        pygame.display.flip()

        # 初始化影片文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        video_path = os.path.join(output_dir, f"tracking_{timestamp}.avi")
        game_video_path = os.path.join(output_dir, f"game_{timestamp}.avi")
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

            # 錄製遊戲畫面
            game_surface = pygame.surfarray.array3d(screen)
            game_frame = cv2.cvtColor(game_surface.swapaxes(0, 1), cv2.COLOR_RGB2BGR)
            game_writer.write(game_frame)

        # 清除紅點並等待
        writer.release()
        game_writer.release()
        screen.fill(BLACK)
        pygame.display.flip()
        time.sleep(2)  # 2秒間隔

    return True

# 主程式
def main():
    # 初始化攝像頭
    camera_id = 0
    cap = setup_camera(camera_id)
    if not cap:
        print("攝像頭初始化失敗！")
        return

    output_dir = create_output_dir()
    writer = cv2.VideoWriter()
    game_writer = cv2.VideoWriter()

    running = True
    try:
        while running:
            running = flash_and_record(cap, writer, game_writer, output_dir)

    except KeyboardInterrupt:
        print("程式被中斷")

    finally:
        cap.release()
        writer.release()
        game_writer.release()
        pygame.quit()

if __name__ == "__main__":
    main()
