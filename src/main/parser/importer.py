# !/usr/bin/python3
# coding: utf-8

# Copyright 2015-2018
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import shutil

from PIL import Image


def get_work_dir():
    dir = os.getcwd()

    if "server" in dir:
        dir = dir.replace("src/main/server", "")

    if not dir.endswith("/"):
        dir = dir + "/"

    return dir


INPUT_FOLDER = os.path.join(get_work_dir(), "data/img")
TMP_FOLDER = os.path.join(get_work_dir(), "data/tmp")
OUTPUT_FOLDER = os.path.join(get_work_dir(), "data/txt")


def prepare_folders():
    """
    :return: void
        Creates necessary folders
    """

    for folder in [
        INPUT_FOLDER, TMP_FOLDER, OUTPUT_FOLDER
    ]:
        if not os.path.exists(folder):
            os.makedirs(folder)

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


def find_images(folder):
    """
    :param folder: str
        Path to folder to search
    :return: generator of str
        List of images in folder
    """

    for file in os.listdir(folder):
        full_path = os.path.join(folder, file)
        if os.path.isfile(full_path):
            try:
                _ = Image.open(full_path)  # if constructor succeeds
                yield file
            except:
                pass


def rotate_image(input_file, output_file, angle=90):
    """
    :param input_file: str
        Path to image to rotate
    :param output_file: str
        Path to output image
    :param angle: float
        Angle to rotate
    :return: void
        Rotates image and saves result
    """

    cmd = "convert -rotate " + "' " + str(angle) + "' "
    cmd += "'" + input_file + "' '" + output_file + "'"
    # print("Running", cmd)
    os.system(cmd)  # sharpen


def sharpen_image(input_file, output_file):
    """
    :param input_file: str
        Path to image to prettify
    :param output_file: str
        Path to output image
    :return: void
        Prettifies image and saves result
    """

    rotate_image(input_file, output_file)  # rotate
    cmd = "convert -auto-level -sharpen 0x4.0 -contrast "
    cmd += "'" + output_file + "' '" + output_file + "'"
    #print("Running", cmd)
    os.system(cmd)  # sharpen


def run_tesseract(input_file, output_file):
    """
    :param input_file: str
        Path to image to OCR
    :param output_file: str
        Path to output file
    :return: void
        Runs tesseract on image and saves result
    """

    cmd = "tesseract -l deu "
    cmd += "'" + input_file + "' '" + output_file + "'"
    #print("Running", cmd)
    os.system(cmd)


def main():
    prepare_folders()
    images = list(find_images(INPUT_FOLDER))
    #print("Found the following images in", INPUT_FOLDER)
    #print(images)

    for image in images:
        input_path = os.path.join(
            INPUT_FOLDER,
            image
        )
        tmp_path = os.path.join(
            TMP_FOLDER,
            image
        )
        out_path = os.path.join(
            OUTPUT_FOLDER,
            image + ".out"
        )

        sharpen_image(input_path, tmp_path)
        run_tesseract(tmp_path, out_path)


if __name__ == '__main__':
    main()
