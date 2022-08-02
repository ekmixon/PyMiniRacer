"""Script to add without pymalloc version of the wheel"""

import os
import re
import sys

from auditwheel.wheeltools import InWheelCtx, _dist_info_dir
from wheel import pkginfo


def get_filenames(directory):
    """Get all the file to copy"""
    for filename in os.listdir(directory):
        if re.search(r"cp\d{2}mu?-manylinux1_\S+\.whl", filename):
            yield filename


def copy_file(filename, destination):
    """Copy the file and put the correct tag"""

    print(f"Updating file {filename}")
    out_dir = os.path.abspath(destination)

    tags = filename[:-4].split("-")

    tags[-2] = tags[-2].replace("m", "")

    new_name = "-".join(tags) + ".whl"
    wheel_flag = "-".join(tags[2:])

    with InWheelCtx(os.path.join(destination, filename)) as ctx:
        info_fname = os.path.join(_dist_info_dir(ctx.path), 'WHEEL')
        infos = pkginfo.read_pkg_info(info_fname)
        print("Current Tags: ", ", ".join([v for k, v in infos.items()
                                           if k == "Tag"]))
        print("Adding Tag", wheel_flag)
        del infos['Tag']
        infos.add_header('Tag', wheel_flag)
        pkginfo.write_pkg_info(info_fname, infos)

        ctx.out_wheel = os.path.join(out_dir, new_name)

        print(f"Saving new wheel into {ctx.out_wheel}")


def main():
    directory = sys.argv[1] if len(sys.argv) == 2 else "dist"
    for filename in get_filenames(directory):
        copy_file(filename, directory)


if __name__ == "__main__":
    main()
