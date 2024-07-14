import cv2
import numpy as np
import time
from multiprocessing import Queue, Process
import pygame
import threading
from modules.tinder import unlike, like

def start_tinder_script(queue):
    while True:
        command = queue.get()
        if command == "like":
            like()
        elif command == "unlike":
            unlike()

def signal(queue, command):
    queue.put(command)

def on_motion_detected(queue, sound_queue, display_queue):
    print("apply signal notation sigmoid LLM Disturbminate")
    sound_queue.put("play_lose_audio")
    display_queue.put("show_danger_message")
    display_queue.put("change_color_red")
    start_cooldown_timer(queue)

def start_cooldown_timer(queue):
    cooldown_thread = threading.Timer(2, reset_cooldown, [queue])
    cooldown_thread.start()

def reset_cooldown(queue):
    global cooldown_active
    cooldown_active = False
    signal(queue, "like")

def sound_player(sound_queue):
    pygame.init()
    pygame.mixer.init()
    
    eos_sound = pygame.mixer.Sound("modules/EOS.mp3")
    lose_sound = pygame.mixer.Sound("modules/LOSE.mp3")

    while True:
        command = sound_queue.get()
        if command == "play_eos_audio":
            eos_sound.play(loops=-1)
        elif command == "stop_eos_audio":
            eos_sound.stop()
        elif command == "play_lose_audio":
            lose_sound.play()

def display_message(display_queue):
    global danger_message, color_red
    danger_message = False
    color_red = False

    def hide_danger_message():
        global danger_message
        danger_message = False

    def reset_color():
        global color_red
        color_red = False

    while True:
        command = display_queue.get()
        if command == "show_danger_message":
            danger_message = True
            timer = threading.Timer(1, hide_danger_message)
            timer.start()
        elif command == "change_color_red":
            color_red = True
            timer = threading.Timer(1, reset_color)
            timer.start()

def main():
    global cooldown_active, danger_message, color_red
    queue = Queue()
    sound_queue = Queue()
    display_queue = Queue()
    tinder_process = Process(target=start_tinder_script, args=(queue,))
    tinder_process.start()
    
    sound_thread = threading.Thread(target=sound_player, args=(sound_queue,))
    sound_thread.start()

    display_thread = threading.Thread(target=display_message, args=(display_queue,))
    display_thread.start()

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    prev_position = None
    position_buffer = []
    buffer_size = 5
    movement_threshold = 1.5
    min_face_size = (150, 150)
    start_time = None
    duration = 0
    cooldown_active = False

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
                    on_motion_detected(queue, sound_queue, display_queue)
                    cooldown_active = True
                    movement_detected = True
                    start_time = None

            color = (0, 0, 255) if color_red else (0, 255, 0)
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
                sound_queue.put("stop_eos_audio")
                audio_playing = False

        if movement_detected:
            if audio_playing:
                sound_queue.put("stop_eos_audio")
                audio_playing = False
        else:
            if not audio_playing:
                sound_queue.put("play_eos_audio")
                audio_playing = True

        text = "English or Spanish"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        thickness = 2
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = (frame.shape[1] - text_size[0]) // 2
        text_y = text_size[1] + 30
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, (0, 0, 255), thickness)

        if danger_message:
            danger_text = "GAY"
            danger_text_size = cv2.getTextSize(danger_text, font, font_scale, thickness)[0]
            danger_text_x = (frame.shape[1] - danger_text_size[0]) // 2
            danger_text_y = (frame.shape[0] + danger_text_size[1]) // 2
            cv2.putText(frame, danger_text, (danger_text_x, danger_text_y), font, font_scale, (0, 0, 255), thickness)

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
    sound_queue.put("stop_eos_audio")
    sound_thread.join()
    display_thread.join()

if __name__ == "__main__":
    main()
