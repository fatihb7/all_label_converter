"""
Author: Fatih Baday <bfatih27@gmail.com>
Purpose: To import and export createml labelling type.
"""
# Importing libraries.
import os
import json
import shutil
import logging
import all_label_converter.commonformat as cf
import all_label_converter.cores.utils as utils

from all_label_converter.cores.config import Config


class CreateMLExport:
    def __init__(self, objs, path: str):
        self.folder_path = path
        self.objs = objs
        self.start()

    def start(self):
        annotations_createml = []
        for obj in self.objs:
            file_name = obj.obj['filename']
            annos_createml = {'image': file_name,
                              'annotations': []}
            for kx in list(obj.obj['boxes'].values()):
                width = kx['bndbox']['xmax'] - kx['bndbox']['xmin']
                height = kx['bndbox']['ymax'] - kx['bndbox']['ymin']
                annos_createml['annotations'].append({'label': kx['name'],
                                                      'coordinates': {'x': kx['bndbox']['xmin'] + int(width / 2),
                                                                      'y': kx['bndbox']['ymin'] + int(height / 2),
                                                                      'width': width,
                                                                      'height': height,
                                                                      }})
            annotations_createml.append(annos_createml)

        with open(os.path.join(self.folder_path,
                               Config.settings["standard_file_name"]["annotations_createml"]), 'w') as json_file:
            json_string = json.dumps(annotations_createml, indent=2)
            json_file.write(json_string)

        for obj_ax in self.objs:
            original = os.path.join(obj_ax.obj["filepath"], obj_ax.obj["filename"])
            target = os.path.join(self.folder_path, obj_ax.obj["filename"])
            shutil.copyfile(original, target)


class CreateMLImport:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.objs = None

        # Check folder path is exist or not.
        if not utils.check_path_exist(self.folder_path):
            logging.error("The process has been terminated. Unsuccessful!")
            return

        # Check annotations file is exist.
        if not utils.check_file_exist(self.folder_path,
                                      Config.settings["standard_file_name"]["annotations_createml"]):
            logging.error("The process has been terminated. Unsuccessful!")
            return

        self.objs = []
        try:
            file = open(os.path.join(self.folder_path, "_annotations.createml.json"))
            json_file = json.load(file)
            boxes_objs_f = self._read_content(json_file, self.folder_path)

            for i, k in boxes_objs_f.items():
                self.objs.append(self._make_commonobject(k, self.folder_path))

        except Exception as error:
            logging.error("There was a problem importing the dataset!")
            logging.error(str(error))
            logging.error("The process has been terminated. Unsuccessful!")
            self.objs = None

    @staticmethod
    def _read_content(list_of_json: list, path_xa: str):
        """
        :purpose: Read file content and returns it to an object that is easier to understand.
        """
        boxes_img = {}

        for ixa in list_of_json:
            file_name = ixa['image']
            height, width, depth = utils.get_image_size(path_xa, file_name)
            counter = 0
            for kxa in ixa['annotations']:
                xmin = int(kxa['coordinates']['x'] - (kxa['coordinates']['width'] / 2))
                ymin = int(kxa['coordinates']['y'] - (kxa['coordinates']['height'] / 2))
                bndbox = {'xmin': xmin,
                          'ymin': ymin,
                          'xmax': int(xmin + float(kxa['coordinates']['width'])),
                          'ymax': int(ymin + float(kxa['coordinates']['height']))}
                if counter == 0:
                    boxes_img[file_name] = {'name': file_name,
                                            'width': width,
                                            'height': height,
                                            'depth': depth,
                                            'boxes': {counter: {'name': kxa['label'],
                                                                'bndbox': bndbox,
                                                                }}}
                    counter += 1

                else:
                    max_count = max([ix for ix in boxes_img[file_name]["boxes"].keys() if type(ix) == int])
                    boxes_img[file_name]["boxes"][max_count + 1] = {'name': kxa['label'],
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
        boxes_f = boxes_obj["boxes"]  # must look.
        obj_f = cf.Data(boxes=boxes_f, image_info=image_info_f)
        return obj_f
