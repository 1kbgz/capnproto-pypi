from os import environ, walk
from sys import platform
from platform import machine
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomHook(BuildHookInterface):
    def initialize(self, version, build_data):
        build_data["pure_python"] = False
        arch = environ.get("AUDITWHEEL_ARCH", machine())
        if "darwin" in platform:
            if "arm" in arch:
                build_data["tag"] = "py3-none-macosx_11_0_arm64"
            else:
                build_data["tag"] = "py3-none-macosx_11_0_x86_64"
        elif "linux" in platform:
            if "arm" in arch or "aarch" in arch:
                build_data["tag"] = "py3-none-linux_aarch64"
            else:
                build_data["tag"] = "py3-none-linux_x86_64"
        else:
            build_data["tag"] = "py3-none-win_amd64"

        # recursively add all files in `capnproto` to the shared-data key
        # put all include in include/, bin in bin/, lib in lib/, lib64 in lib64/
        build_data["shared_data"] = {}
        for subdir in ["include", "bin", "lib", "lib64"]:
            # Walk through the files themselves
            for dirpath, _, filenames in walk(f"capnproto/{subdir}"):
                for filename in filenames:
                    filepath = f"{dirpath}/{filename}"
                    target_path = filepath.replace("capnproto/", "")
                    build_data["shared_data"][filepath] = target_path
        return version, build_data
