#!/usr/bin/env -S uv run --script
# /// script
# dependencies = []
# ///
# vim: ft=python

import argparse
import os
import shutil
import socket
import subprocess
import sys
import atexit
import tempfile
import time

SOCKET_PATH = "/tmp/show-image.sock"


def cleanup_socket(path):
    """Remove socket file on exit."""
    if os.path.exists(path):
        os.unlink(path)


def open_serve(socket_path, invert=False):
    """Launch show-image server in a new kitty split pane."""
    # Get the path to this script
    script_path = os.path.realpath(__file__)

    # Check if running inside kitty
    if "KITTY_WINDOW_ID" not in os.environ or "TMUX_PANE" in os.environ:
        print("Not running in kitty terminal, cannot open split pane automatically", file=sys.stderr)
        print(f"Please ask the user to start `{script_path} --serve` manually in kitty", file=sys.stderr)
        print(f"No use this skill again if user confirmed they are not using kitty")
        return False

    # Find uv executable
    uv_cmd = shutil.which("uv")
    if not uv_cmd:
        print("Error: uv not found in PATH", file=sys.stderr)
        return False

    # Build command
    cmd = [
        "kitty", "@",
        "launch",
        "--location=vsplit",      # vertical split
        "--title=show-image-server",
        "--cwd=current",           # in same environment
        "--keep-focus",            # keep focus in current pane
        uv_cmd, "run", "--script", script_path, "--serve", f"--socket-path={socket_path}"
    ]
    if invert:
        cmd.append("--invert")

    # Use kitty remote control to launch a new split pane
    result = subprocess.run(cmd, capture_output=True)

    if result.returncode != 0:
        print(f"Failed to launch kitty pane: {result.stderr.decode()}", file=sys.stderr)
        return False

    # Wait briefly for server to start
    for _ in range(50):  # wait up to 5 seconds
        if os.path.exists(socket_path):
            return True
        time.sleep(0.1)

    return False


def serve_mode(socket_path, invert=False):
    """Run server: listen for image paths and display them with kitten icat."""
    atexit.register(cleanup_socket, socket_path)

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        sock.bind(socket_path)
    except OSError as e:
        print(f"Error: {e}. Socket already in use?", file=sys.stderr)
        sys.exit(1)

    sock.listen(1)
    mode_str = " (inverted)" if invert else ""
    print(f"show-image server listening on {socket_path}{mode_str}", file=sys.stderr)

    try:
        while True:
            conn, _ = sock.accept()
            try:
                # Read all paths from this connection until client closes it
                data = b""
                while True:
                    chunk = conn.recv(1)
                    if not chunk:
                        break
                    if chunk == b"\n":
                        if data:
                            path = data.decode("utf-8")
                            real_path = os.path.realpath(path)

                            if os.path.isfile(real_path):
                                print(real_path)
                                display_path = real_path
                                if invert:
                                    # Create temp file for inverted image
                                    suffix = os.path.splitext(real_path)[1]
                                    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                                        tmp_path = tmp.name
                                    subprocess.run(
                                        ["convert", real_path, "-negate", tmp_path],
                                        check=True,
                                        capture_output=True
                                    )
                                    display_path = tmp_path

                                try:
                                    if "KITTY_WINDOW_ID" in os.environ:
                                        subprocess.run(["kitty", "+kitten", "icat", display_path])
                                    else:
                                        subprocess.run(["timg", "-ph", display_path])
                                finally:
                                    if invert and display_path != real_path:
                                        os.unlink(display_path)
                            else:
                                print(f"File not found: {real_path}", file=sys.stderr)
                        data = b""
                    else:
                        data += chunk
            finally:
                conn.close()
    except KeyboardInterrupt:
        print("\nShutting down server", file=sys.stderr)
    finally:
        sock.close()


def put_mode(socket_path, image_paths, invert=False):
    """Send image paths to server, starting server if needed."""
    if not os.path.exists(socket_path):
        if not open_serve(socket_path, invert):
            # Server failed to start, exit silently
            sys.exit(0)

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        sock.connect(socket_path)
        for image_path in image_paths:
            real_path = os.path.realpath(image_path)
            sock.sendall(real_path.encode("utf-8") + b"\n")
    finally:
        sock.close()


def main():
    parser = argparse.ArgumentParser(description="Send image paths to a viewing terminal")
    parser.add_argument("--serve", action="store_true", help="Run in server mode")
    parser.add_argument(
        "--socket-path", default=SOCKET_PATH, help="Path to Unix socket (default: %(default)s)"
    )
    parser.add_argument("--invert", action="store_true", help="Invert colors before displaying")
    parser.add_argument("image_paths", nargs="*", help="Paths to image files (put mode only)")

    args = parser.parse_args()

    if args.serve:
        serve_mode(args.socket_path, args.invert)
    elif args.image_paths:
        put_mode(args.socket_path, args.image_paths, args.invert)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
