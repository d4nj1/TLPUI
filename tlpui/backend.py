"""Backend helper methods."""
import os


def detect_display():
    """
    Detect the appropriate GDK backend (wayland or x11).

    Prefers Wayland when the session is Wayland and the Wayland
    display socket is available. Otherwise falls back to x11.
    """
    session = os.environ.get("XDG_SESSION_TYPE", "").lower()

    # True Wayland session + available display socket
    if session == "wayland" and "WAYLAND_DISPLAY" in os.environ:
        return "wayland"

    # Fallback: if DISPLAY exists, use X11
    if "DISPLAY" in os.environ:
        return "x11"

    # If nothing else detected, default to x11
    print("Could not detect display backend. Falling back to x11.")
    return "x11"
