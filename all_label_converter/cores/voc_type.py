"""
Author: Fatih Baday <bfatih27@gmail.com>
Purpose: To import and export voc labelling type.
"""
# Importing libraries.
import os
import shutil
import logging
import xml.etree.ElementTree as EleT
import all_label_converter.commonformat as cf
import all_label_converter.cores.utils as utils


class VocExport:
    def __init__(self, objs, folder_path):
        self.objs = objs
        self.folder_path = folder_path

        for obj in self.objs:
            self.start(obj.obj)

    def start(self, obj):
        """
        :param obj: One of common objects.
        :return:
        """
        # General info
        annotation = EleT.Element("annotation")
        folder = EleT.SubElement(annotation, "folder")

        # Filename
        filename = EleT.SubElement(annotation, "filename")
        filename.text = obj["filename"]

        # Source
        source = EleT.SubElement(annotation, "source")
        database = EleT.SubElement(source, "database")
        annotation_s = EleT.SubElement(source, "annotation")
        image_s = EleT.SubElement(source, "image")
        source.text = "Unknown"
        database.text = "Unknown"
        annotation_s.text = "Unknown"
        image_s.text = "Unknown"

        # Size
        size = EleT.SubElement(annotation, "size")
        width = EleT.SubElement(size, "width")
        height = EleT.SubElement(size, "height")
        depth = EleT.SubElement(size, "depth")
        width.text = str(obj["width"])
        height.text = str(obj["height"])
        depth.text = str(obj["depth"])

        # Segmented
        segmented = EleT.SubElement(annotation, "segmented")

        # Object
        for obj_i in obj["boxes"].items():
            locals()[f"obj_{obj_i[0]}"] = EleT.SubElement(annotation, "object")
            locals()[f"name_{obj_i[0]}"] = EleT.SubElement(locals()[f"obj_{obj_i[0]}"], "name")
            locals()[f"occluded_{obj_i[0]}"] = EleT.SubElement(locals()[f"obj_{obj_i[0]}"], "occluded")
            locals()[f"bndbox_{obj_i[0]}"] = EleT.SubElement(locals()[f"obj_{obj_i[0]}"], "bndbox")
            locals()[f"xmin_{obj_i[0]}"] = EleT.SubElement(locals()[f"bndbox_{obj_i[0]}"], "xmin")
            locals()[f"ymin_{obj_i[0]}"] = EleT.SubElement(locals()[f"bndbox_{obj_i[0]}"], "ymin")
            locals()[f"xmax_{obj_i[0]}"] = EleT.SubElement(locals()[f"bndbox_{obj_i[0]}"], "xmax")
            locals()[f"ymax_{obj_i[0]}"] = EleT.SubElement(locals()[f"bndbox_{obj_i[0]}"], "ymax")

            locals()[f"name_{obj_i[0]}"].text = obj_i[1]["name"]
            locals()[f"occluded_{obj_i[0]}"].text = "0"
            locals()[f"xmin_{obj_i[0]}"].text = str(obj_i[1]["bndbox"]["xmin"])
            locals()[f"ymin_{obj_i[0]}"].text = str(obj_i[1]["bndbox"]["ymin"])
            locals()[f"xmax_{obj_i[0]}"].text = str(obj_i[1]["bndbox"]["xmax"])
            locals()[f"ymax_{obj_i[0]}"].text = str(obj_i[1]["bndbox"]["ymax"])

        tree = EleT.ElementTree(annotation)
        tree.write(os.path.join(self.folder_path, f"{obj['filename'].split('.')[0]}.xml"))

        original = os.path.join(obj["filepath"], obj["filename"])
        target = os.path.join(self.folder_path, obj["filename"])
        shutil.copyfile(original, target)


class VocImport:
    def __init__(self, folder_path):
        self.folder_path = folder_path

        # Check folder path is exist or not.
        if not utils.check_path_exist(self.folder_path):
            logging.error("The process has been terminated. Unsuccessful!")
            self.objs = None
            return

        listdir = os.listdir(self.folder_path)
        self.objs = []
        try:
            for i in listdir:
                if i.endswith(".xml"):
                    boxes, image_info = self._read_content(os.path.join(self.folder_path, i), self.folder_path)
                    obj = self._make_commonobject(boxes, image_info)
                    self.objs.append(obj)
        except Exception as error:
            logging.error("There was a problem importing the dataset!")
            logging.error(str(error))
            logging.error("The process has been terminated. Unsuccessful!")
            self.objs = None

    @staticmethod
    def _read_content(xml_file: str, path_x: str):
        """
        :purpose: Read file content and returns it to an object that is easier to understand.
        :param xml_file: Xml file.
        :param path_x: Path.
        :return boxes_objs: Boxes object specific format with dict type.
        """
        tree = EleT.parse(xml_file)
        root = tree.getroot()

        all_boxes = {}
        image_info_f = None
        counter = 0

        for boxes_f in root.iter('object'):
            # MustLook.
            filename_x = root.find("filename").text
            if not filename_x.endswith(".jpg"):
                filename_x += ".jpg"

            image_info_f = {"width": int(root.find("size/width").text),
                            "height": int(root.find("size/height").text),
                            "depth": int(root.find("size/depth").text),
                            "path": root.find("path").text,
                            "filename": filename_x,
                            "filepath": path_x}

            all_boxes[counter] = {"name": boxes_f.find("name").text,
                                  "pose": boxes_f.find("pose").text,
                                  "truncated": boxes_f.find("truncated").text,
                                  "difficult": boxes_f.find("difficult").text,
                                  "occluded": boxes_f.find("occluded").text,
                                  "bndbox": {"xmin": int(boxes_f.find("bndbox/xmin").text),
                                             "ymin": int(boxes_f.find("bndbox/ymin").text),
                                             "xmax": int(boxes_f.find("bndbox/xmax").text),
                                             "ymax": int(boxes_f.find("bndbox/ymax").text)}}
            counter += 1

        return all_boxes, image_info_f

    @staticmethod
    def _make_commonobject(boxes_f, image_info_f):
        """
        :purpose: Convert common object.
        :param boxes_f: Boxes object with dict type.
        :param image_info_f: Image information.
        :return obj_f: Common objects.
        """
        obj_f = cf.Data(boxes=boxes_f, image_info=image_info_f)
        return obj_f
