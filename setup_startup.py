"""Setup script to configure Jarvis autostart"""

from jarvis.startup import StartupManager


def main():
    """Main setup function"""
    startup_manager = StartupManager()

    print("\n" + "="*60)
    print("🚀 JARVIS STARTUP CONFIGURATION")
    print("="*60)
    print("\nChoose an option:")
    print("  1. Enable Jarvis autostart (starts on PC boot)")
    print("  2. Disable Jarvis autostart")
    print("  3. Check startup status")
    print("  4. Exit")

    choice = input("\nEnter your choice (1-4): ").strip()

    if choice == "1":
        if startup_manager.enable_startup():
            print("\n✅ Success! Jarvis will now start when your PC boots up.")
        else:
            print("\n❌ Failed to enable startup.")

    elif choice == "2":
        if startup_manager.disable_startup():
            print("\n✅ Success! Jarvis has been removed from startup.")
        else:
            print("\n❌ Failed to disable startup.")

    elif choice == "3":
        startup_manager.print_status()

    elif choice == "4":
        print("\nGoodbye!")
        return

    else:
        print("\n❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
