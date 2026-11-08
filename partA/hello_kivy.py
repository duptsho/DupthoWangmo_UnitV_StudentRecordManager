from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class HelloApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=25, spacing=15)
        self.message = Label(text="Hello from Kivy!")
        button = Button(text="Click me", size_hint=(1, 0.35))
        button.bind(on_press=self.show_message)
        layout.add_widget(self.message)
        layout.add_widget(button)
        return layout

    def show_message(self, instance):
        self.message.text = "Hello! You clicked the button."

if __name__ == "__main__":
    HelloApp().run()
