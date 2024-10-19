import subprocess

class Bontail:
    @staticmethod
    def format(image, size):
        try:
            subprocess.run(["dd", "if=/dev/zero", f"of={image}", "bs=1M", f"count={size}"], check=True)
            subprocess.run(['mkfs.ext4', image])
        except subprocess.CalledProcessError as e:
            print(f"Error formatting image: {e}")

    @staticmethod
    def mount(image, mountpoint):
        try:
            subprocess.run(["mount", image, mountpoint], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error mounting image: {e}")

    @staticmethod
    def umount(mountpoint):
        try:
            subprocess.run(["umount", "-l", mountpoint], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error unmounting: {e}")

    @staticmethod
    def bootstrap(mountpoint, distribution):
        try:
            if distribution == "arch":
                subprocess.run(["pacstrap", "-K", mountpoint], check=True)
            else:
                subprocess.run(["debootstrap", "bookworm", mountpoint, "https://deb.debian.org/debian"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error bootstrapping: {e}")

    @staticmethod
    def chroot(mountpoint, command="/bin/bash"):
        try:
            subprocess.run(["chroot", mountpoint, command], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error entering chroot: {e}")
if __name__ == "__init__":
    print(":: bontail is not a standalone")