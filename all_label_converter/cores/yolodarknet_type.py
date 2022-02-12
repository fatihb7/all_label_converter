"""
Author: Fatih Baday <bfatih27@gmail.com>
Purpose: To import and export yolo (darknet) type.
"""
# Importing libraries.
import os
import shutil
import logging
import all_label_converter.commonformat as cf
import all_label_converter.cores.utils as utils

from all_label_converter.cores.config import Config


class YoloDarknetExport:
    def __init__(self, objs, folder_path):
        self.objs = objs
        self.folder_path = folder_path

        self.start()

    def start(self):
        """
        :return:
        """
        class_names = []
        for obj_ax in self.objs:
            for i in [y["name"] for x, y in obj_ax.obj["boxes"].items()]:
                class_names.append(i)

        class_names = list(set(class_names))
        with open(os.path.join(self.folder_path, "_darknet.labels"), 'w') as file:
            for class_name in class_names:
                file.write(class_name + "\n")

        for obj in self.objs:
            file_name = obj.obj['filename']
            width = obj.obj['width']
            height = obj.obj['height']
            write_list = []

            for anno in list(obj.obj['boxes'].values()):
                xmin = anno['bndbox']['xmin']
                ymin = anno['bndbox']['ymin']
                xmax = anno['bndbox']['xmax']
                ymax = anno['bndbox']['ymax']

                class_name = anno['name']
                class_index = str(class_names.index(class_name))
                write_list += [[class_index,
                                str(float(xmin + xmax) / 2 / width),
                                str(float(ymin + ymax) / 2 / height),
                                str(float(xmax - xmin) / width),
                                str(float(ymax - ymin) / height)]]

            with open(os.path.join(self.folder_path, os.path.splitext(os.path.basename(file_name))[0] + ".txt"), "w")\
                    as file:
                for write_element in write_list:
                    file.write(" ".join(write_element) + "\n")

        for obj_ax in self.objs:
            original = os.path.join(obj_ax.obj["filepath"], obj_ax.obj["filename"])
            target = os.path.join(self.folder_path, obj_ax.obj["filename"])
            shutil.copyfile(original, target)


class YoloDarknetImport:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.objs = None

        # Check folder path is exist or not.
        if not utils.check_path_exist(self.folder_path):
            logging.error("The process has been terminated. Unsuccessful!")
            return

        # Check annotations file is exist.
        if not utils.check_file_exist(self.folder_path,
                                      Config.settings["standard_file_name"]["annotations_yolodarknet"]):
            logging.error("The process has been terminated. Unsuccessful!")
            return

        self.objs = []

        try:
            images_files = [file_name for file_name in os.listdir(self.folder_path) if file_name.endswith(".jpg")]
            boxes_objs_f = self._read_content(self.folder_path, images_files)

            for i, k in boxes_objs_f.items():
                self.objs.append(self._make_commonobject(k, self.folder_path))

        except Exception as error:
            logging.error("There was a problem importing the dataset!")
            logging.error(str(error))
            logging.error("The process has been terminated. Unsuccessful!")
            self.objs = None

    @staticmethod
    def _read_content(path_a: str, images_files_a: list):
        """
        :purpose: Read file content and returns it to an object that is easier to understand.
        """
        boxes_img = {}
        darknet_labels = []
        with open(os.path.join(path_a,
                               Config.settings["standard_file_name"]["annotations_yolodarknet"])) as file:
            for row in file:
                darknet_labels.append(row.strip())

        for file_name in images_files_a:
            # image_path = os.path.join(path_a, file_name)
            anno_path = os.path.join(path_a, os.path.splitext(os.path.basename(file_name))[0] + ".txt")

            width, height, depth = utils.get_image_size(path_a, file_name)

            annotations = []
            with open(anno_path, "r") as file:
                for row in file:
                    annotations.append(row.strip())

            for anno in annotations:
                anno_float = [float(i) for i in anno.split(" ")]
                xmax = (width * (2 * anno_float[1] + anno_float[3])) / 2
                xmin = (width * (2 * anno_float[1] - anno_float[3])) / 2
                ymax = (height * (2 * anno_float[2] + anno_float[4])) / 2
                ymin = (height * (2 * anno_float[2] - anno_float[4])) / 2

                bndbox = {"xmin": xmin,
                          "ymin": ymin,
                          "xmax": xmax,
                          "ymax": ymax}
                class_name = darknet_labels[int(anno_float[0])]

                if file_name not in list(boxes_img.keys()):
                    boxes_img[file_name] = {'name': file_name,
                                            'width': int(width),
                                            'height': int(height),
                                            'depth': int(depth),
                                            'boxes': {0: {'name': class_name,
                                                          'bndbox': bndbox,
                                                          }}}

                else:
                    max_count = max([ix for ix in boxes_img[file_name]["boxes"].keys() if type(ix) == int])
                    boxes_img[file_name]["boxes"][max_count + 1] = {'name': class_name,
                                                                    'bndbox': bndbox,
                                                                    }

        return boxes_img

    @staticmethod
    def _make_commonobject(boxes_obj, path_x: str):
        """
        :purpose: Convert common object and occur "image_info_f" variables.
        """
        image_info_f = {"height": boxes_obj["height"],
                        "width": boxes_obj["width"],
                        "depth": boxes_obj["depth"],
                        "filename": boxes_obj["name"],
                        "filepath": path_x}
        boxes_f = boxes_obj["boxes"]
        obj_f = cf.Data(boxes=boxes_f, image_info=image_info_f)
        return obj_f
