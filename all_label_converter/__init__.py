"""
Purpose: Label converter
Author: Fatih Baday <bfatih27@gmail.com>
"""

# Loading libraries.
import logging


def export_dataset(objects_f: list, type_f: str, path_f: str):
    """
    :param objects_f: list of common objects.
    :param type_f: type of dataset to be exported
    :param path_f: folder path of the dataset to be exported
    :return: None
    """
    if type_f == "voc":
        try:
            from all_label_converter.cores.voc_type import VocExport
            VocExport(objects_f, path_f)
            logging.info("Success! Exporting dataset voc format!")
        except Exception as error:
            logging.error("There is problem with export type voc!")
            logging.error(str(error))
            logging.error("The process has been terminated. Unsuccessful!")

    elif type_f == "coco":
        try:
            from all_label_converter.cores.coco_type import CocoExport
            CocoExport(objects_f, path_f)
            logging.info("Success! Exporting dataset coco format!")
        except Exception as error:
            logging.error("There is problem with export type coco!")
            logging.error(str(error))
            logging.error("The process has been terminated. Unsuccessful!")

    elif type_f == "createml":
        try:
            from all_label_converter.cores.createml_type import CreateMLExport
            CreateMLExport(objs=objects_f, path=path_f)
            logging.info("Success! Exporting dataset coco format!")
        except Exception as error:
            logging.error("There is problem with export type coco!")
            logging.error(str(error))
            logging.error("The process has been terminated. Unsuccessful!")

    elif type_f == "tensorflowcsv":
        try:
            from all_label_converter.cores.tfcsv_type import TFCsvExport
            TFCsvExport(objs=objects_f, folder_path=path_f)
            logging.info("Success! Exporting Tensorflow Object Detection CSV!")
        except Exception as error:
            logging.error("There is problem with export type Tensorflow Object Detection CSV!")
            logging.error(str(error))
            logging.error("The process has been terminated. Unsuccessful!")

    elif type_f == "yolodarknet":
        try:
            from all_label_converter.cores.yolodarknet_type import YoloDarknetExport
            YoloDarknetExport(objs=objects_f, folder_path=path_f)
            logging.info("Success! Exporting YOLO Darknet!")
        except Exception as error:
            logging.error("There is problem with export type YOLO Darknet!")
            logging.error(str(error))
            logging.error("The process has been terminated. Unsuccessful!")

    else:
        logging.error("Wrong dataset type!")
        logging.error("The process has been terminated. Unsuccessful!")


def import_dataset(path_m: str, type_m: str):
    """
    :param path_m: the path of the dataset to import.
    :param type_m: dataset type.
    :return: common dataset objects.
    """
    objects_m = None
    if type_m == "voc":
        from all_label_converter.cores.voc_type import VocImport
        voc_obj = VocImport(folder_path=path_m)
        objects_m = voc_obj.objs
    elif type_m == "coco":
        from all_label_converter.cores.coco_type import CocoImport
        coco_obj = CocoImport(folder_path=path_m)
        objects_m = coco_obj.objs
    elif type_m == "createml":
        from all_label_converter.cores.createml_type import CreateMLImport
        cml_obj = CreateMLImport(folder_path=path_m)
        objects_m = cml_obj.objs
    elif type_m == "tensorflowcsv":
        from all_label_converter.cores.tfcsv_type import TFCsvImport
        tfcsv_obj = TFCsvImport(folder_path=path_m)
        objects_m = tfcsv_obj.objs
    elif type_m == "yolodarknet":
        from all_label_converter.cores.yolodarknet_type import YoloDarknetImport
        yolodarknet_obj = YoloDarknetImport(folder_path=path_m)
        objects_m = yolodarknet_obj.objs
    else:
        logging.error(msg="Wrong dataset type!")
        logging.error(msg="The process has been terminated. Unsuccessful!")

    return objects_m
