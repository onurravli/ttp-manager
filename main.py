import os
import argparse

mods = [{id: 0, "mod": "Silent"}, {id: 1, "mod": "Turbo"}, {id: 2, "mod": "On Demand"}]


def check_root():
    return os.geteuid() == 0


def get_os():
    return os.uname()[0]


def get_mod() -> int:
    file_path = "/sys/devices/platform/asus-nb-wmi/throttle_thermal_policy"
    if file_path:
        with open(file_path, "r") as f:
            return int(f.read().strip())
    else:
        return -1


def set_mod(mod: str):
    file_path = "/sys/devices/platform/asus-nb-wmi/throttle_thermal_policy"
    if check_root():
        if file_path:
            if mod in ["silent", "turbo", "on_demand"]:
                with open(file_path, "w") as f:
                    if mod == "silent":
                        mod_id = 0
                    elif mod == "turbo":
                        mod_id = 1
                    elif mod == "on_demand":
                        mod_id = 2
                    f.write(str(mod_id))
            else:
                print("Invalid mod!")
        else:
            print("File not found!")
    else:
        print("You need to run this program as root!")
        exit(1)


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-s", "--set", help="Set the mod", type=str, choices=["silent", "turbo", "on_demand"])
    argparser.add_argument("-g", "--get", help="Get the mod", action="store_true")
    args = argparser.parse_args()
    if args.set:
        set_mod(args.set)
    elif args.get:
        print(f"Current mod: {mods[get_mod()]['mod']}")
    else:
        argparser.print_help()


if __name__ == "__main__":
    if get_os() == "Linux":
        main()
    else:
        print("This program works in Linux only!")
        exit(1)
