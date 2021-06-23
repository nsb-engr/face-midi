import mido
import re

CONFIG_FILE = "./config.py"
2
def set_midi_port():
    ports = mido.get_output_names()
    print("Availavle ports are ...")
    print("-----------------------")
    for i, port in enumerate(ports):
        print("{}:{}".format(i+1,port))
    print("-----------------------")
    n = int(input("Please select a port by number and press Enter.\n>"))
    if 0 < n <= len(ports):
        print("{}:{} is selected".format(n,ports[n-1]))
    else:
        raise ValueError("Please input listed values.")

    config_file = "./config.py"
    with open(config_file) as f:
        lines = f.read()
        lines = re.sub("PORTNAME = .*\n", "PORTNAME = \"{}\"\n".format(ports[n-1]), lines)
        
    with open("./config.py", "w") as f:
        f.write(lines)
    print("Port configuration has written to config.py.")


if __name__ == "__main__":
    set_midi_port()