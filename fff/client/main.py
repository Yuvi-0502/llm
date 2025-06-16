from app.controllers.main_controller import MainController

def main():
    try:
        controller = MainController()
        controller.run()
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
        print("Please try again or contact support if the problem persists.")

if __name__ == "__main__":
    main() 