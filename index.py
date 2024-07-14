import cv2
import numpy as np
import time
from multiprocessing import Queue, Process
import pygame
import threading
from modules.tinder import unlike, like
"""
Note run this cmd on terminal for openned chrome for webdrifver

"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9999


"""
def start_tinder_script(queue):
    while True:
        command = queue.get()
        if command == "like":
            like()
        elif command == "unlike":
            unlike()

def signal(queue, command):
    queue.put(command)

def on_motion_detected(queue):
    print("apply signal notation sigmoid LLM Disturbminate")
    #play_lose_audio()
    start_cooldown_timer(queue)

def play_audio():
    pygame.mixer.music.load("modules/EOS.mp3")
    pygame.mixer.music.play(-1)

def stop_audio():
    pygame.mixer.music.stop()

def play_lose_audio():
    pygame.mixer.music.load("modules/LOSE.mp3")
    pygame.mixer.music.play()

def start_cooldown_timer(queue):
    cooldown_thread = threading.Timer(2, reset_cooldown, [queue])
    cooldown_thread.start()

def reset_cooldown(queue):
    global cooldown_active
    cooldown_active = False
    signal(queue, "like")

def main():
    global cooldown_active
    queue = Queue()
    tinder_process = Process(target=start_tinder_script, args=(queue,))
    tinder_process.start()

    pygame.init()
    pygame.mixer.init()

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    prev_position = None
    position_buffer = []
    buffer_size = 5
    movement_threshold = 1
    min_face_size = (100, 100)
    start_time = None
    duration = 0
    cooldown_active = False
    last_motion_time = time.time()

    audio_playing = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=min_face_size)
        movement_detected = False

        for (x, y, w, h) in faces:
            current_position = (x + w // 2, y + h // 2)
            position_buffer.append(current_position)
            if len(position_buffer) > buffer_size:
                position_buffer.pop(0)

            avg_position = np.mean(position_buffer, axis=0)

            if prev_position is not None:
                distance = np.linalg.norm(avg_position - prev_position)
                if distance > movement_threshold and not cooldown_active:
                    on_motion_detected(queue)
                    cooldown_active = True
                    movement_detected = True
                    start_time = None

            color = (0, 0, 255) if movement_detected else (0, 255, 0)
            if not movement_detected and start_time is None:
                start_time = time.time()
            if not movement_detected:
                duration = time.time() - start_time

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            prev_position = avg_position

        if len(faces) == 0:
            start_time = None
            duration = 0
            if audio_playing:
                stop_audio()
                audio_playing = False

        if movement_detected:
            if audio_playing:
                stop_audio()
                audio_playing = False
        else:
            if not audio_playing:
                play_audio()
                audio_playing = True

        text = "English or Spanish"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        thickness = 2
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = (frame.shape[1] - text_size[0]) // 2
        text_y = text_size[1] + 30
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, (0, 0, 255), thickness)

        timer_text = f"Time: {duration:.2f} sec"
        timer_font_scale = 1
        timer_thickness = 2
        timer_size = cv2.getTextSize(timer_text, font, timer_font_scale, timer_thickness)[0]
        timer_x = 10
        timer_y = frame.shape[0] - 10
        cv2.rectangle(frame, (timer_x - 5, timer_y - timer_size[1] - 5), (timer_x + timer_size[0] + 5, timer_y + 5), (255, 255, 255), -1)
        cv2.putText(frame, timer_text, (timer_x, timer_y), font, timer_font_scale, (0, 0, 0), timer_thickness)

        cv2.imshow('English or Spanish', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    tinder_process.terminate()

if __name__ == "__main__":
    main()
