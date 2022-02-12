"""
Author: Fatih Baday <bfatih27@gmail.com>
Purpose: To import and export tensorflow csv type.
"""
# Importing libraries.
import os
import shutil
import logging
import pandas as pd
import all_label_converter.commonformat as cf
import all_label_converter.cores.utils as utils

from all_label_converter.cores.config import Config


class TFCsvExport:
    def __init__(self, objs, folder_path: str):
        self.objs = objs
        self.folder_path = folder_path
        self.start()

    def start(self):
        df = pd.DataFrame(columns=['filename', 'width', 'height', 'class',
                                   'xmin', 'ymin', 'xmax', 'ymax'])

        for obj in self.objs:
            file_name = obj.obj['filename']
            width = obj.obj['width']
            height = obj.obj['height']
            for anno in list(obj.obj['boxes'].values()):
                xmin = anno['bndbox']['xmin']
                ymin = anno['bndbox']['ymin']
                xmax = anno['bndbox']['xmax']
                ymax = anno['bndbox']['ymax']

                class_n = anno['name']
                obj_list = [file_name, width, height, class_n,
                            xmin, ymin, xmax, ymax]
                df = df.append(pd.Series(obj_list, index=df.columns), ignore_index=True)

        file_path = os.path.join(self.folder_path,
                                 Config.settings["standard_file_name"]["annotations_tfcsv"])
        # noinspection PyTypeChecker
        df.to_csv(file_path, index=False)

        for obj_ax in self.objs:
            original = os.path.join(obj_ax.obj["filepath"], obj_ax.obj["filename"])
            target = os.path.join(self.folder_path, obj_ax.obj["filename"])
            shutil.copyfile(original, target)


class TFCsvImport:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.objs = None

        # Check folder path is exist or not.
        if not utils.check_path_exist(self.folder_path):
            logging.error("The process has been terminated. Unsuccessful!")
            return

        # Check annotations file is exist.
        if not utils.check_file_exist(self.folder_path,
                                      Config.settings["standard_file_name"]["annotations_tfcsv"]):
            logging.error("The process has been terminated. Unsuccessful!")
            return

        self.objs = []

        try:
            df = pd.read_csv(os.path.join(self.folder_path, "tensorflow.csv"))
            boxes_objs_f = self._read_content(df, self.folder_path)

            for i, k in boxes_objs_f.items():
                self.objs.append(self._make_commonobject(k, self.folder_path))

        except Exception as error:
            logging.error("There was a problem importing the dataset!")
            logging.error(str(error))
            logging.error("The process has been terminated. Unsuccessful!")
            self.objs = None

    @staticmethod
    def _read_content(df_y, path_xa: str):
        """
        :purpose: Read file content and returns it to an object that is easier to understand.
        """
        boxes_img = {}
        for flname in list(df_y["filename"].unique()):
            df_x = df_y[df_y["filename"] == flname]
            file_name = flname
            width = df_x['width'].unique()[0]
            height = df_x['height'].unique()[0]
            _, _, depth = utils.get_image_size(path_xa, file_name)

            for ik in list(df_x.index):
                bndbox = {'xmin': int(df_x.loc[ik, 'xmin']),
                          'ymin': int(df_x.loc[ik, 'ymin']),
                          'xmax': int(df_x.loc[ik, 'xmax']),
                          'ymax': int(df_x.loc[ik, 'ymax'])}

                if file_name not in list(boxes_img.keys()):
                    boxes_img[file_name] = {'name': file_name,
                                            'width': int(width),
                                            'height': int(height),
                                            'depth': int(depth),
                                            'boxes': {0: {'name': df_x.loc[ik, 'class'],
                                                          'bndbox': bndbox,
                                                          }}}

                else:
                    max_count = max([ix for ix in boxes_img[file_name]["boxes"].keys() if type(ix) == int])
                    boxes_img[file_name]["boxes"][max_count + 1] = {'name': df_x.loc[ik, 'class'],
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
