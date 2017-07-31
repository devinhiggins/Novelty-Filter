import subprocess
import os


class Entropy():
    def __init__(self):
        self.path = os.getcwd()
        self.script = "entropy.out"
        self.script_path = os.path.join(self.path, self.script)

    def get_entropy(self, filename, N=12, charmap="charToKMap.txt"):
        cmds = [self.script_path, filename, str(N), os.path.join(os.getcwd(), charmap)]
        output = subprocess.check_output(cmds)
        self.parse_output(output)
        return self.parsed_output

    def parse_output(self, output):
        self.parsed_output = {}
        output_lines = output.split("\n")

        self.parsed_output["entropy"] = output_lines[1].split()[1]
        self.parsed_output["error_c_entropy"] = output_lines[2].split()[-1]
        self.parsed_output["max_h"] = output_lines[3].split()[-1]
        self.parsed_output["I"] = output_lines[4].split()[1]
        self.parsed_output["eI"] = output_lines[4].split()[3]
