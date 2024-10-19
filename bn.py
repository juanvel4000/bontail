from bontail import Bontail
import configparser
import os
import sys

bn = Bontail()
BNDIR = "/usr/share/bontail"
CFGDIR = f"{BNDIR}/config"
MNTDIR = f"{BNDIR}/mount"
IMGDIR = f"{BNDIR}/img"

# Ensure the script is run as root
if os.getuid() != 0:
    print("!! please run as root")
    sys.exit(1)

# Create necessary directories if they don't exist
if not os.path.isdir(BNDIR):
    print("!! creating bontail directories")
    os.makedirs(CFGDIR, exist_ok=True)
    os.makedirs(MNTDIR, exist_ok=True)
    os.makedirs(IMGDIR, exist_ok=True)
else:
    print(":: found bontail directory")

def configurate(entry, value, name):
    with open(f'{CFGDIR}/{name}.conf', 'a') as f:
        f.write(f"{entry} = {value}\n")

def create(name, size, distribution):
    IMAGE = f"{IMGDIR}/{name}.bn"
    MOUNTPOINT = f"{MNTDIR}/{name}"
    
    os.makedirs(MOUNTPOINT, exist_ok=True)
    
    bn.format(IMAGE, size)  # Size must be in Megabytes
    bn.mount(IMAGE, MOUNTPOINT)
    bn.bootstrap(MOUNTPOINT, distribution)
    bn.umount(MOUNTPOINT)
    
    with open(f"{CFGDIR}/{name}.conf", 'w') as file:
        file.write('[BONTAIL]\n')
    
    configurate('name', name, name)
    configurate('size', size, name)
    configurate('image', IMAGE, name)
    configurate('distro', distribution, name)
    configurate('mountpoint', MOUNTPOINT, name)

    print(f"Successfully created a {distribution} Bontail with {size}MB")

def chroot(name, command="/bin/bash"):
    config = configparser.ConfigParser()
    config.read(f"{CFGDIR}/{name}.conf")
    
    IMAGE = config['BONTAIL']['image']
    MOUNTPOINT = config['BONTAIL']['mountpoint']
    
    bn.mount(IMAGE, MOUNTPOINT)
    bn.chroot(MOUNTPOINT, command)
    bn.umount(MOUNTPOINT)

def menu():
    mainmenu = """
    bn
    ===
    1. Create a new Bontail
    2. Open a Bontail
    3. Configure
    4. Exit
    """
    while True:
        print(mainmenu)
        selection = input(":: ")
        if selection == "1":
            name = input("name :: ")
            size = input("size (in MB) :: ")
            distro = input("distro (arch/debian) :: ")
            if distro in ["arch", "debian"]:
                create(name, size, distro)
            else:
                print(":: invalid distro")
        elif selection == "2":
            name = input("bn :: ")
            if os.path.isfile(f"{CFGDIR}/{name}.conf"):
                print(f":: opening {name}")
                chroot(name)
            else:
                print(":: configuration not found")
        elif selection == "3":
            print("!! coming soon")
        elif selection == "4":
            sys.exit(0)
        else:
            print(":: invalid selection")

if __name__ == "__main__":
    menu()
