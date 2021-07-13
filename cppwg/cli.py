#!/usr/bin/env python

import os
from argparse import ArgumentParser
from glob import glob
from cppwg import CppWrapperGenerator


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--source_root",
        "-s",
        type=str,
        help="Root of the source directory.",
        default=os.getcwd(),
    )
    parser.add_argument(
        "--wrapper_root",
        "-w",
        type=str,
        help="Root of the wrapper directory.",
        default=os.getcwd(),
    )
    parser.add_argument(
        "--castxml_binary",
        "-c",
        type=str,
        help="Path to the castxml binary.",
        default="castxml",
    )
    parser.add_argument(
        "--package_info",
        "-p",
        type=str,
        help="Path to package_info.yaml",
        default=os.join(os.getcwd(), "package_info.yaml"),
    )
    parser.add_argument(
        "--includes",
        "-i",
        type=str,
        help="Path to the includes directory.",
        default=os.getcwd(),
    )
    args = parser.parse_args()

    includes = glob(args.includes + "/*/")

    generator = CppWrapperGenerator(
        args.source_root,
        includes,
        args.wrapper_root,
        args.castxml_binary,
        args.package_info,
    )
    generator.generate_wrapper()
