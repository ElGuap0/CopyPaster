from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Key
from pynput.keyboard import Listener as KeyboardListener
from pynput import mouse
import pyautogui as pyag
import time
import pyperclip
import tkinter as tk

detection_time = 0.3

class CopyPaster:

    def __init__(self, gui_on = False):
       
        self.copied_text = ''
        self.count = 0
        self.disable_func = False
        self.start_mouse_listener()
        self.start_keyboard_listener()
        self.start_time = 0
        self.delta = 0
        self.text_just_pasted = False
       
        if gui_on == True:
            self.init_gui()
           
    def init_gui(self):
       
        self.root = tk.Tk()
        self.root.title('Copy Paste Utility')
        self.root.geometry("400x100")
        self.mode_label = tk.Label(self.root,text="Copying Disabled" if self.disable_func else "Copying Enabled")
        self.toggle_button = tk.Button(self.root, text = 'Toggle Copy Mode', command = self.toggle_mode)
        self.message_label = tk.Label(self.root,text="Right Click to interrupt")
        self.toggle_button.pack()
        self.mode_label.pack()
        self.message_label.pack()
        self.root.protocol('WM_DELETE_WINDOW', self.quit_all)
        self.root.mainloop()
       
    def toggle_mode(self):
        # enable/disable copying
        self.disable_func = not (self.disable_func)
        if self.disable_func == True:
            self.mouse_listener.stop()
            self.keyboard_listener.stop()
        else:
            self.start_keyboard_listener()
            self.start_mouse_listener()
        self.mode_label.config(text = "Copying Disabled" if self.disable_func else "Copying Enabled")
   
    def on_press(self, key):
        # keyboard listener checks here
        # print('{0} pressed'.format(key)) # debug
        self.check_key(key)
   
    def check_key(self, key):
        # add any control using keyboard input here
        #if key in [Key.format up, Key.down, Key.left, Key.right, Key.esc]:
        #if key in [Key.esc]:
        #    self.quit_all()
        pass
   
    def on_click(self, x, y, button, pressed):
        # copy text when mouse is held. paste when clicked.
       
        if self.disable_func == False:
           
            if button == mouse.Button.right:
                self.quit_all()
           
            elif self.copied_text == '':
               
                # pressed is true when the mouse clicks down.
                # pressed is false when the mouse was clicked down and then released.
                if pressed == True:
                    self.start_time = time.perf_counter()
                   
                    # if the text was just pasted reset the switch.
                    if self.text_just_pasted == True:
                        self.text_just_pasted = False
                    return
               
                # if the mouse is being released but the text was just pasted we do not want to start the timer
                if pressed == False and self.text_just_pasted == False:
                   
                    self.delta = time.perf_counter() - self.start_time
                   
                    if self.delta > detection_time:
                        self.copy_clipboard()
                        self.start_time = 0
                        self.delta = 0
               
            # if single click and text was successfully copied give one click to change the window
            # then try to paste with a single click
            if pressed == True:
               
                if self.copied_text !='':
                   
                    if self.count == 1:
                        self.paste_text()
                    else:
                        self.count += 1
               
    def paste_text(self):
       
        try:
           
            pyag.keyDown('ctrl');pyag.press('v');pyag.keyUp('ctrl')
            self.count = 0
            self.copied_text = ''
            self.write_op("Pasted")
            self.text_just_pasted = True
           
        except:
            self.write_op("Unable to paste")
            pyag.keyUp('ctrl')
            self.count = 0
   
    def copy_clipboard(self):
       
        self.keyboard_listener.stop()
       
        try:
            time.sleep(0.2)  # keeping this delay is critical
            pyag.keyDown('ctrl');pyag.press('c');pyag.keyUp('ctrl')
            self.copied_text = pyperclip.paste()
            self.write_op("Copied to clipboard")
           
        except:
            self.write_op("Copy Error")
            pyag.keyUp('ctrl')
           
        self.start_keyboard_listener()  
   
    def start_keyboard_listener(self):

        self.keyboard_listener = KeyboardListener(on_press=self.on_press)
        self.keyboard_listener.start()
   
    def start_mouse_listener(self):

        self.mouse_listener = MouseListener(on_click=self.on_click)
        self.mouse_listener.start()

    def write_op(self, text):
        if hasattr(self, 'root'):
            self.message_label.config(text = text)
        else:
            print(text)
           
    def quit_all(self):

        self.write_op("Exiting")
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        if hasattr(self, 'root'):
            self.root.destroy()
        del self

if __name__ == '__main__':
   
    cpaster=CopyPaster(True)
