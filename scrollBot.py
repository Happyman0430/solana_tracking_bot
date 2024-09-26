import pyautogui
import time

def scroll_bot():
    while True:
        # Scroll down
        pyautogui.scroll(-250)  # Negative value scrolls down
        time.sleep(10)  # Wait for 5 seconds
        print("scroll down")
        # Scroll up
        pyautogui.scroll(-250)  # Negative value scrolls down
        time.sleep(10)  # Wait for 5 seconds
        print("scroll down")
        # Scroll up
        pyautogui.scroll(250)  # Positive value scrolls up
        time.sleep(10)  # Wait for 5 seconds
        print("scroll up") 
        pyautogui.scroll(250)  # Positive value scrolls up
        time.sleep(10)  # Wait for 5 seconds
        print("scroll up") 
if __name__ == "__main__":
    try:
        scroll_bot()
    except KeyboardInterrupt:
        print("Scrolling stopped.")
