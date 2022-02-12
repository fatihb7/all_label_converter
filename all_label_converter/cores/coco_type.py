"""
Author: Fatih Baday <bfatih27@gmail.com>
Purpose: To import and export coco labelling type.
"""
# Importing libraries.
import os
import json
import shutil
import logging
import all_label_converter.commonformat as cf
import all_label_converter.cores.utils as utils

from datetime import datetime
from all_label_converter.cores.config import Config


class CocoExport:
    def __init__(self, objs, folder_path: str):
        self.objs = objs
        self.folder_path = folder_path
        self.start()

    def start(self):
        """
        :purpose: Do all process in function.
        """
        id_count = 0
        categories = []
        categories_name = []

        for obj_ax in self.objs:
            for i in [y["name"] for x, y in obj_ax.obj["boxes"].items()]:
                if i not in categories_name:
                    categories_name.append(i)

        for i in categories_name:
            categories.append({"id": id_count,
                               "name": i,
                               "supercategory": "none"})
            id_count += 1

        images = []
        id_count = 0

        for obj_ax in self.objs:
            images.append({"id": id_count,
                           "license": "1",
                           "file_name": obj_ax.obj["filename"],
                           "height": obj_ax.obj["height"],
                           "width": obj_ax.obj["width"],
                           "data_captured": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+03:00")})
            id_count += 1

        id_count = 0
        annotations = []

        for obj_ax in self.objs:
            for key, value in obj_ax.obj["boxes"].items():
                category_id = list(filter(lambda x: x["name"] == value["name"], categories))[0]["id"]
                image_id = list(filter(lambda x: x["file_name"] == obj_ax.obj["filename"], images))[0]["id"]
                bbox = [value["bndbox"]["xmin"],
                        value["bndbox"]["ymin"],
                        value["bndbox"]["xmax"] - value["bndbox"]["xmin"],
                        value["bndbox"]["ymax"] - value["bndbox"]["ymin"]]

                area = bbox[2] * bbox[3]
                annotations.append({"id": id_count,
                                    "image_id": image_id,
                                    "category_id": category_id,
                                    "bbox": bbox,
                                    "area": area,
                                    "segmentation": [],
                                    "iscrowd": 0})
                id_count += 1

        annotations_json = {"info": {"year": str(datetime.now().year),
                                     "version": "1",
                                     "description": "Converted dataset by use label-converter",
                                     "contributor": "",
                                     "url": "",
                                     "data_created": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+03:00")},
                            "licenses": [{
                                "id": 1,
                                "url": "",
                                "name": "Unknown"}],
                            "categories": categories,
                            "images": images,
                            "annotations": annotations}

        with open(os.path.join(self.folder_path,
                               Config.settings["standard_file_name"]["annotations_coco"]), 'w') as json_file:
            json_string = json.dumps(annotations_json, indent=2)
            json_file.write(json_string)

        for obj_ax in self.objs:
            original = os.path.join(obj_ax.obj["filepath"], obj_ax.obj["filename"])
            target = os.path.join(self.folder_path, obj_ax.obj["filename"])
            shutil.copyfile(original, target)


class CocoImport:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.objs = None

        # Check folder path is exist or not.
        if not utils.check_path_exist(self.folder_path):
            logging.error("The process has been terminated. Unsuccessful!")
            return

        # Check annotations file is exist.
        if not utils.check_file_exist(self.folder_path,
                                      Config.settings["standard_file_name"]["annotations_coco"]):
            logging.error("The process has been terminated. Unsuccessful!")
            return

        self.objs = []
        try:
            with open(os.path.join(self.folder_path,
                                   Config.settings["standard_file_name"]["annotations_coco"])) as file:
                json_file = json.load(file)

            boxes_objs = self._read_content(json_file)
            for i, k in boxes_objs.items():
                self.objs.append(self._make_commonobject(k, self.folder_path))

        except Exception as error:
            logging.error("There was a problem importing the dataset!")
            logging.error(str(error))
            logging.error("The process has been terminated. Unsuccessful!")
            self.obj = None

    @staticmethod
    def _read_content(json_file: dict):
        """
        :purpose: Read file content and returns it to an object that is easier to understand.
        :param json_file: Annotations json file with dict type.
        :return boxes_objs: Json file in a specific format with dict type.
        """
        categories = json_file["categories"].copy()
        categories = {x["id"]: x for x in categories}

        images = json_file["images"].copy()
        annotations = json_file["annotations"].copy()

        boxes_objs = {}
        for i_f in annotations:
            if i_f["image_id"] not in boxes_objs.keys():
                boxes_objs[i_f["image_id"]] = {"boxes": {0: {"name": categories[i_f["category_id"]]["name"],
                                                             "bndbox": {"xmin": i_f["bbox"][0],
                                                                        "ymin": i_f["bbox"][1],
                                                                        "xmax": i_f["bbox"][0] + i_f["bbox"][2],
                                                                        "ymax": i_f["bbox"][1] + i_f["bbox"][3]}}},
                                               "width":
                                                   [kl["width"] for kl in images if kl["id"] == i_f["image_id"]]
                                                   [0],
                                               "height":
                                                   [kx["height"] for kx in images if kx["id"] == i_f["image_id"]]
                                                   [0],
                                               "name":
                                                   [ky["file_name"] for ky in images if ky["id"] == i_f["image_id"]]
                                                   [0]}
            else:
                max_count = max([ix for ix in boxes_objs[i_f["image_id"]]["boxes"].keys() if type(ix) == int])
                boxes_objs[i_f["image_id"]]["boxes"][max_count + 1] = {
                    "name": categories[i_f["category_id"]]["name"],
                    "bndbox": {"xmin": i_f["bbox"][0],
                               "ymin": i_f["bbox"][1],
                               "xmax": i_f["bbox"][0] + i_f["bbox"][
                                   2],
                               "ymax": i_f["bbox"][1] + i_f["bbox"][
                                   3]}}

        return boxes_objs

    @staticmethod
    def _make_commonobject(boxes_obj, path_x: str):
        """
        :purpose: Convert common object and occur "image_info_f" variables.
        :param boxes_obj: Boxes object with dict type.
        :param path_x: Folderp path that included image files.
        :return: Common objects.
        """
        image_info_f = {"height": boxes_obj["height"],
                        "width": boxes_obj["width"],
                        "depth": 3,
                        "filename": boxes_obj["name"],
                        "filepath": path_x}
        boxes_f = boxes_obj["boxes"]  # must look.
        obj_f = cf.Data(boxes=boxes_f, image_info=image_info_f)
        return obj_f
