import cv2
import datetime
import os

def setup_camera(camera_id, width=640, height=480):
    """初始化攝像頭"""
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print(f"無法打開攝像頭 {camera_id}")
        return None
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return cap

def create_output_dir():
    """創建影片保存資料夾"""
    output_dir = r"E:/eyeErack/Vid"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def main():
    # 設定左鏡頭 (假設為攝像頭 0)
    left_cam_id = 0
    left_cam = setup_camera(left_cam_id)

    if not left_cam:
        print("請檢查左鏡頭連接！")
        return

    # 初始化錄製狀態
    recording = False
    left_writer = None
    output_dir = create_output_dir()

    # 設定影片參數
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 使用 XVID 編碼
    frame_rate = 30  # 每秒幀數
    frame_size = (int(left_cam.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(left_cam.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    print("按 'r' 開始錄製，按 'q' 保存當前影片，按 'ESC' 完全退出程式。")

    while True:
        # 擷取影像
        ret, left_frame = left_cam.read()

        if not ret:
            print("無法讀取影像，請檢查左鏡頭！")
            break

        # 鏡像處理
        left_frame = cv2.flip(left_frame, 1)

        # 顯示左鏡頭影像
        cv2.imshow("Left Camera", left_frame)

        # 鍵盤事件
        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'):  # 開始錄製
            if not recording:
                recording = True
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                left_video_path = os.path.join(output_dir, f"left_camera_{timestamp}.avi")
                left_writer = cv2.VideoWriter(left_video_path, fourcc, frame_rate, frame_size)
                print(f"開始錄製：{left_video_path}")

        elif key == ord('q'):  # 保存當前影片
            if recording:
                recording = False
                left_writer.release()
                print("當前影片已保存。")

        elif key == 27:  # 按下 ESC 鍵退出程式
            if recording:
                recording = False
                left_writer.release()
            break

        # 如果正在錄製，將影像寫入影片檔案
        if recording:
            left_writer.write(left_frame)

    # 清理資源
    left_cam.release()
    if left_writer:
        left_writer.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
