import bios
import argparse


def read_cfg(cfg_path: str) -> dict:
    return bios.read(cfg_path)


def get_parser() -> argparse.PARSER:
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf_path')
    return parser
