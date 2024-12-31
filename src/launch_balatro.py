import webbrowser


def launch_balatro() -> bool:
    balatro_steam_url = "steam://run/2379780"

    try:
        if webbrowser.open(balatro_steam_url):
            print("Launching Balatro through Steam...")
            return True
        else:
            print("Failed to launch Balatro. Please check if Steam is installed.")
            return False
    except Exception as e:
        print(f"Error launching Balatro: {e}")
        return False
