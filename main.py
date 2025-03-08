from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.core.window import Window
import math

class CalculatorLayout(BoxLayout):
    display_text = StringProperty("0")
    history = ListProperty([])
    is_dark_theme = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current = ""
        self.last_result = None
        Window.bind(on_key_down=self.on_key_down)  

    def on_key_down(self, window, keycode, scancode, codepoint, modifier):
        char = codepoint
        key = keycode

        if char:
            if char in "0123456789" or (key in range(256, 266)):  
                self.button_press(char if char else str(key - 256))
            elif char == "." or key == 266:  
                self.button_press(".")
            elif char in "+-*/%=":
                self.button_press(char)
            elif key in (270, 269, 268, 267, 271):  
                self.button_press({270: "+", 269: "-", 268: "*", 267: "/", 271: "="}[key])
        if key == 8:  
            self.delete()
        elif key == 27:  
            self.clear()
        elif key == 261: 
            self.clear_message()

    def button_press(self, value):
        if self.display_text == "Error":
            self.clear()

        if value in "0123456789.":
            self.current += value
        elif value in "+-*/%":
            if self.current:
                self.current += f" {value} "
        elif value == "=":
            try:
                result = str(eval(self.current))
                self.display_text = result
                self.history.append(f"{self.current} = {result}")
                self.current = result
            except Exception:
                self.display_text = "Error"
                self.current = ""
        elif value in ("sin", "cos", "tan", "log", "sqrt", "square", "cube", "factorial", "inverse", "power"):
            try:
                num = float(self.current) if self.current else 0
                if value == "sin":
                    result = math.sin(math.radians(num))
                elif value == "cos":
                    result = math.cos(math.radians(num))
                elif value == "tan":
                    result = math.tan(math.radians(num))
                elif value == "log":
                    result = math.log10(num) if num > 0 else float("inf")
                elif value == "sqrt":
                    result = math.sqrt(num) if num >= 0 else float("inf")
                elif value == "square":
                    result = num ** 2
                elif value == "cube":
                    result = num ** 3
                elif value == "factorial":
                    result = math.factorial(int(num)) if num >= 0 and num.is_integer() else float("inf")
                elif value == "inverse":
                    result = 1 / num if num != 0 else float("inf")
                elif value == "power":
                    base, exp = map(float, self.current.split("^")) if "^" in self.current else (num, 2)
                    result = base ** exp
                self.display_text = str(result)
                self.history.append(f"{value}({self.current}) = {result}")
                self.current = str(result)
            except Exception:
                self.display_text = "Error"
                self.current = ""
        elif value in ("pi", "e"):
            self.current = str(math.pi if value == "pi" else math.e)
        self.update_display()

    def clear(self):
        self.current = ""
        self.display_text = "0"

    def delete(self):
        if self.current:
            self.current = self.current[:-1].strip()
            self.update_display()

    def clear_message(self):
        if self.display_text == "Error":
            self.clear()

    def update_display(self):
        self.display_text = self.current if self.current else "0"

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        if self.is_dark_theme:
            Window.clearcolor = (0.1, 0.1, 0.1, 1)
            self.ids.display.color = (1, 1, 1, 1)
        else:
            Window.clearcolor = (1, 1, 1, 1)
            self.ids.display.color = (0, 0, 0, 1)

    def show_history(self):
        content = BoxLayout(orientation="vertical")
        history_label = "\n".join(self.history[-10:]) if self.history else "No history yet."
        content.add_widget(Label(text=history_label, halign="left", valign="top"))
        content.add_widget(Button(text="Close", size_hint_y=None, height=50, on_press=lambda x: popup.dismiss()))
        popup = Popup(title="Calculation History", content=content, size_hint=(0.8, 0.8))
        popup.open()

class CalculatorApp(App):
    def build(self):
        return CalculatorLayout()

if __name__ == "__main__":
    CalculatorApp().run()