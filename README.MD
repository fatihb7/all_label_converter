# Label Converter

Hello everyone, I'm trying to develop a solution to the problem I've had before while working on Computer vision with this repo.

To train different models, there must be different types of labeling, for example coco, voc etc.


### Added labelling types.

- [x] COCO
- [x] Pascal VOC
- [x] Create ML
- [x] YOLO Darknet
- [x] Tensorflow Object Detection CSV
- [ ] Tensorflow TFRecord

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install all_label_converter
```

## Usage

```python
import all_label_converter

common_objects = all_label_converter.import_dataset('{files_path}', '{type_dataset_ex_coco}')
all_label_converter.export_dataset(common_objects, "{target_dataset}", "{target_file_path}")
```
And you can see dataset translated according to your request.


## License
[MIT](https://choosealicense.com/licenses/mit/)