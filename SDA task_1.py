from abc import ABC, abstractmethod

# Abstract Product: Button
class Button(ABC):
    @abstractmethod
    def render(self):
        pass

# Abstract Product: TextField
class TextField(ABC):
    @abstractmethod
    def display(self):
        pass
# Windows-specific Widgets
class WindowsButton(Button):
    def render(self):
        print("Rendering Windows Button")

class WindowsTextField(TextField):
    def display(self):
        print("Displaying Windows TextField")

# macOS-specific Widgets
class MacButton(Button):
    def render(self):
        print("Rendering macOS Button")

class MacTextField(TextField):
    def display(self):
        print("Displaying macOS TextField")

# Linux-specific Widgets
class LinuxButton(Button):
    def render(self):
        print("Rendering Linux Button")

class LinuxTextField(TextField):
    def display(self):
        print("Displaying Linux TextField")
        
# Abstract Factory Interface
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_text_field(self) -> TextField:
        pass

# Concrete Factory for Windows
class WindowsFactory(UIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_text_field(self) -> TextField:
        return WindowsTextField()

# Concrete Factory for macOS
class MacFactory(UIFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_text_field(self) -> TextField:
        return MacTextField()

# Concrete Factory for Linux
class LinuxFactory(UIFactory):
    def create_button(self) -> Button:
        return LinuxButton()

    def create_text_field(self) -> TextField:
        return LinuxTextField()
def main(factory: UIFactory):
    button = factory.create_button()
    text_field = factory.create_text_field()

    button.render()
    text_field.display()

# Client chooses a factory dynamically based on OS
if __name__ == "__main__":
    os_choice = input("Choose OS (windows/mac/linux): ").strip().lower()

    if os_choice == "windows":
        factory = WindowsFactory()
    elif os_choice == "mac":
        factory = MacFactory()
    elif os_choice == "linux":
        factory = LinuxFactory()
    else:
        print("Invalid choice. Defaulting to Windows.")
        factory = WindowsFactory()

    main(factory)
