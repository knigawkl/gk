import bios


def read_cfg(cfg_path: str) -> dict:
    config = bios.read(cfg_path)
    return config