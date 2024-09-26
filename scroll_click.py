import pyautogui
import time
import random
import threading

def display_clock():
    while True:
        current_time = time.strftime("%H:%M:%S", time.localtime())
        print(f"\rCurrent Time: {current_time}", end="")
        time.sleep(1)

def countdown_timer(duration):
    while duration:
        mins, secs = divmod(duration, 60)
        # timer = f"{mins:02d}:{secs:02d}"
        # print(f"\rCountdown: {timer}", end="")
        time.sleep(1)
        duration -= 1
    print(duration)

def scroll_bot(duration):
    start_time = time.time()  # Record the start time
    countdown_thread = threading.Thread(target=countdown_timer, args=(duration,), daemon=True)
    countdown_thread.start()

    while True:
        # Scroll down
        pyautogui.scroll(-150)  # Negative value scrolls down
        time.sleep(10)  # Wait for 10 seconds
        print("scroll down")
        
        # Scroll up
        pyautogui.scroll(150)  # Positive value scrolls up
        time.sleep(10)  # Wait for 10 seconds
        print("scroll up")
        
        # Check if the specified time has passed
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            move_and_click()
            start_time = time.time()  # Reset the timer
            # Restart countdown if you want it to repeat
            countdown_thread = threading.Thread(target=countdown_timer, args=(duration,), daemon=True)
            countdown_thread.start()

def move_and_click():
    # Generate random x and y coordinates within screen resolution
    x = random.randint(0, pyautogui.size().width)
    y = random.randint(0, pyautogui.size().height)

    # Move the mouse to the random position
    pyautogui.moveTo(x, y, duration=1)  # Moves mouse to (x, y) in 1 second
    print(f"Mouse moved to: ({x}, {y})")

    # Left click at the current mouse position
    pyautogui.click()
    print("Mouse clicked")

if __name__ == "__main__":
    try:
        # Start the clock in a separate thread
        clock_thread = threading.Thread(target=display_clock, daemon=True)
        clock_thread.start()

        # Ask user to input the time in seconds
        duration = int(input("Enter the time (in seconds) after which the mouse should move and click: "))
        scroll_bot(duration)
    except KeyboardInterrupt:
        print("Scrolling and clicking stopped.")
