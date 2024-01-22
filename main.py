# This is a sample Python script.
import base64
import struct

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests

BEGIN_RAW_CODES_ = """
begin remote
\tname\tfujitsu_heat_ac
\tflags\tRAW_CODES
\teps\t30
\taeps\t1
\tfrequency\t38400
\tgap\t104300
\t\tbegin raw_codes
"""

RAW_CODES_END_REMOTE_ = """
\t\tend raw_codes
end remote
"""


def main():
    # based on the work from https://github.com/emilsoman/pronto_broadlink/blob/master/pronto2broadlink.py
    smart_ir_config = requests.get(
        "https://raw.githubusercontent.com/smartHomeHub/SmartIR/master/codes/climate/1281.json")
    smart_ir_config.raise_for_status()

    current_command = ""
    commands_ = smart_ir_config.json()["commands"]
    pulse_commands = process_command_level(commands_, current_command)
    lirc_commands = {}
    for pulse_command in pulse_commands:
        lirc_commands[pulse_command[0]] = list(map(lambda x: int(x * 92 / 3), pulse_command[1]))
    print(lirc_commands)
    generate_lircd_file(lirc_commands)


def generate_lircd_file(lirc_commands):
    with open("fujitsu-ar-rah1u.lircd.conf", 'w') as f:
        f.write(BEGIN_RAW_CODES_)
        for lirc_command in lirc_commands:
            raw_codes = map(lambda x: str(x), lirc_commands[lirc_command][:-1])
            raw_codes_str = ' '.join(raw_codes)
            if lirc_command.startswith("heat_cool"):
                lirc_command = lirc_command.replace("heat_cool", "auto")
            f.write(f"\n\t\t\tname {lirc_command}")
            f.write(f"\n\t\t\t\t{raw_codes_str}\n")
            # for index, raw_code in enumerate(raw_codes):
            #     if (index) % 8 == 0:
            #         f.write(f"\n\t\t\t\t")
            #     f.write(f" {raw_code}")

        f.write(RAW_CODES_END_REMOTE_)


def process_command_level(commands_, current_command, list_of_commands=None):
    if list_of_commands is None:
        list_of_commands = list()
    if current_command != "":
        current_command += "-"
    for command in commands_.keys():
        sub_command_or_string = commands_[command]
        if isinstance(sub_command_or_string, str):
            list_of_commands.append(print_command_lirc(current_command + command, sub_command_or_string))
        if isinstance(sub_command_or_string, dict):
            process_command_level(sub_command_or_string, current_command + command, list_of_commands)
    return list_of_commands


def print_command_lirc(command_name, command_str):
    int_array = [x for x in base64.b64decode(command_str)]
    length_of_signal = struct.unpack_from("<H", bytes(int_array[2:4]))[0]
    important_code = list()
    i = 0
    while i < length_of_signal:
        if int_array[i + 4] == 0:
            important_code.append(struct.unpack_from(">H", bytes(int_array[i + 5:i + 7]))[0])
            i += 3
            continue
        important_code.append(int_array[i + 4])
        i += 1
    return command_name, important_code


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
