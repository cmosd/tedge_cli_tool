import os
import subprocess
from typing import List, Iterator
from rich.console import Console

console = Console()

ARCH_MAPPER = {
        "x86_64":  "x86_64-unknown-linux-gnu",
        "armhf": "arm-unknown-linux-gnueabihf",
        "arm64": "arm-unknown-linux-gnueabi"
}

TEDGE_PACKAGES = (
    "tedge",
    "tedge_agent",
    "tedge_mapper",
    "tedge_apt_plugin",
)

def checkout_branch(branch_name):
    command = "cd $TEDGE_DIR && "
    command += f"git checkout {branch_name}"
    result = run_command(command)
    console.print(result)


def run_command(command: str) -> str:
    process = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    result = process.stdout.read().decode("utf8")
    # `result` returns a newline after the command, so this will remove it
    if result.endswith("\n"):
        result = "\n".join(result.split("\n")[:-1])
    return result

def create_debian_packages(arch, release):
    """
    this function runs build based on arch.
    """
    ccb = CrossCommandBuilder(arch=arch, release=release)
    command = ccb.create_build_command()

    console.print("Running build")
    run_command(command=command)

    console.print("Creating debian packages")
    for command in ccb.yield_debian_package_command():
        debian_package_file = run_command(command)
        path = os.path.join(debian_package_file)
        console.print(path)

def upload_debian_to_host(arch, package_name, host_name):
    path_to_tedge = os.getenv("TEDGE_DIR")
    assert path_to_tedge

    path_to_tedge = os.path.join(path_to_tedge)
    path_to_tedge += f"/target/{arch}/debian/"
    for filename in os.listdir(path_to_tedge):
        file_version_onwards = filename.split(f"{package_name}_")

        if len(file_version_onwards) < 2:
            continue
        else:
            file_version_onwards = file_version_onwards[1]

        if file_version_onwards[0].isdigit():
            path_to_tedge += filename
            break

    run_command(f"scp {path_to_tedge} {host_name}:.")





class CrossCommandBuilder:
    def __init__(self, arch, release):
        self.cargo_cross = "cross"
        self.cross_action = "build"

        self.cargo_deb = "cargo deb"
        self.cargo_deb_default_args = [
            "--no-build",
            "--no-strip"
        ]
        self.arch = arch
        self.release = str(release) if release else None

    @staticmethod
    def _base_command() -> str:
        return "cd $TEDGE_DIR && "

    @staticmethod
    def _join_args(args: List[str]) -> str:
        return ' '.join(args)


    def create_build_command(self) -> str:
        command = self._base_command()
        if self.release:
            command += self._join_args([self.cargo_cross, self.cross_action, "--release", "--target", self.arch])
        else:
            command += self._join_args([self.cargo_cross, self.cross_action, "--target", self.arch])
        return command

    def yield_debian_package_command(self) -> Iterator[str]:
        for package in TEDGE_PACKAGES:
            command = self._base_command()
            command += self._join_args([self.cargo_deb, "--target", self.arch, *self.cargo_deb_default_args, "-p", package])
            yield command

