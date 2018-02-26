#!/usr/bin/env python

import fileinput
import sys
from datetime import date

version_file = "./resources/version.txt"
file_list = [version_file]


class PyBump(object):

    __allowed_bump_types = ["major", "minor", "patch", "version"]
    _major = 0
    _minor = 0
    _patch = 0

    def __init__(self):
        """Reads from a resources/version.txt file to load the major, minor and
        patch version numbers.

        The file is assumed to be in xml format, with the version in a
        <Version>x.x.x</Version> tag, because, well, that's how I hardcoded
        it."""
        file = fileinput.input(files=version_file)
        for line in file:
            if "<Version>" in line:
                start_index = line.find("<Version>")
                first_index = line.find(".", start_index)
                second_index = line.find(".", first_index + 1)
                end_index = line.find("</Version>")

                # TODO: this is icky, I know, but I was young and wild and free
                self._major = int(line[start_index + 9:first_index])
                self._minor = int(line[first_index + 1:second_index])
                self._patch = int(line[second_index + 1:end_index])

        file.close()

    def bump(self):
        print("The current version is {}".format(self.__get_version__()))

        bump_type = str(sys.argv[1]) if (len(sys.argv) > 1) else ""

        while bump_type not in self.__allowed_bump_types:
            bump_type = input(
                "Is this a major bump (breaking changes), a minor "
                "bump (backwards compatible changes), or a patch "
                "bump (backwards compatible bug fixes)? ")
            # I can't remember why I did this...
            while bump_type not in self.__allowed_bump_types:
                bump_type = input("In case it wasn't clear, the options are: "
                                  "major|minor|patch: ")

            break

        """Perhaps someone just wants to show the version (rather than looking
        in ./resources/version.txt) - we can break early then"""
        if bump_type == "version":
            quit()

        self.__bump_version(bump_type)

        print("Bumping version to {}.{}.{}: a {} bump".format(
            self._major, self._minor, self._patch, bump_type))

        """In the project for which this was originally written, there were a
        plethora of files in which the version number was maintained. This was
        a far safer way of handling version number changes."""
        for current_file in file_list:
            print("Bumping version in " + current_file)
            with open(current_file, 'r+') as f:
                lines = f.readlines()
                f.seek(0)
                f.truncate()
                for line in lines:
                    if "<Version>" in line:
                        start_index = line.find("<Version>")
                        end_index = line.find("</Version>")
                        version = line[start_index:end_index + 10]
                        line = line.replace(
                            version, "<Version>{0}.{1}.{2}</Version>".format(
                                self._major, self._minor, self._patch))

                    if "<ReleaseDate>" in line:
                        today = date.today().isoformat()
                        start_index = line.find("<ReleaseDate>")
                        end_index = line.find("</ReleaseDate>")
                        version = line[start_index:end_index + 14]
                        line = line.replace(
                            version, "<ReleaseDate>{0}</ReleaseDate>".format(
                                today))
                    f.write(line)

        print("Bump complete")

    def __get_version__(self):
        """Returns a formatted version major.minor.patch (e.g. 3.2.1)"""
        return "{}.{}.{}".format(self._major, self._minor, self._patch)

    def __bump_version(self, bump_type):
        """Bumps the version of the instance according to bump type"""
        if bump_type not in self.__allowed_bump_types:
            raise ValueError("Supported arguments are: {}, {}, {}, {}".format(
                *self.__allowed_bump_types))

        if bump_type == "major":
            self._major += 1
            self._minor = 0
            self._patch = 0
        elif bump_type == "minor":
            self._minor += 1
            self._patch = 0
        elif bump_type == "patch":
            self._patch += 1


if __name__ == '__main__':
    pybump = PyBump()
    pybump.bump()
