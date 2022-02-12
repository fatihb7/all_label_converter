"""
Author: Fatih Baday <bfatih27@gmail.com>
Purpose: All labels convert to common object.
"""


class Data:
    def __init__(self, boxes, image_info):
        self.obj = None
        self.obj = self.set_obj(boxes, image_info)

    @staticmethod
    def set_obj(boxes_f, image_info_f):
        obj = {"boxes": boxes_f,
               "width": image_info_f["width"],
               "height": image_info_f["height"],
               "depth": image_info_f["depth"],
               "filename": image_info_f["filename"],
               "filepath": image_info_f["filepath"]}
        return obj
