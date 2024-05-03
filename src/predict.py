import argparse

import yaml
import os
from os.path import join
from detectron2.checkpoint import DetectionCheckpointer
from detectron2.config import get_cfg
from detectron2.engine import default_argument_parser, default_setup, launch
from ditod import add_vit_config
from detectron2.data.datasets import register_coco_instances
from ditod import VGTTrainer as MyTrainer
from path_config import PROJECT_ROOT_PATH, IMAGES_ROOT_PATH, JSON_TEST_FILE_PATH


def setup(args):
    """
    Create configs and perform basic setups.
    """
    cfg = get_cfg()
    # add_coat_config(cfg)
    add_vit_config(cfg)
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)

    # cfg.MODEL.DEVICE = "cpu"
    cfg.freeze()
    default_setup(cfg, args)
    return cfg


def get_args(model_name: str):
    parser = default_argument_parser()
    args, unknown = parser.parse_known_args()
    args.config_file = join(PROJECT_ROOT_PATH, "src", "model_configuration", f"{model_name}_VGT_cascade_PTM.yaml")
    args.eval_only = True
    args.num_gpus = 1
    args.opts = ['MODEL.WEIGHTS', join(PROJECT_ROOT_PATH, 'models', f'{model_name}_VGT_model.pth'),
                 'OUTPUT_DIR', join(PROJECT_ROOT_PATH, f'model_output_{model_name}')]
    args.debug = False
    return args


doclaynet_args = get_args("doclaynet")
configuration = setup(doclaynet_args)
doclaynet_model = MyTrainer.build_model(configuration)
DetectionCheckpointer(doclaynet_model, save_dir=configuration.OUTPUT_DIR).resume_or_load(configuration.MODEL.WEIGHTS, resume=False)


def main(args):
    if 'sdfsdfsdfdoclaynet' in args.opts[1]:
        model = doclaynet_model
    else:
        model = MyTrainer.build_model(configuration)
        DetectionCheckpointer(model, save_dir=configuration.OUTPUT_DIR).resume_or_load(
            configuration.MODEL.WEIGHTS, resume=args.resume
        )
    res = MyTrainer.test(configuration, model)
    return res


def prepare_model_path(model_name: str):
    os.makedirs(join(PROJECT_ROOT_PATH, f"model_output_{model_name}"), exist_ok=True)
    with open(join(PROJECT_ROOT_PATH, "src", "model_configuration", f"{model_name}_VGT_cascade_PTM.yaml"), "r") as file:
        yaml_content = yaml.safe_load(file)

    embedding_model_path = join(PROJECT_ROOT_PATH, "models", "layoutlm-base-uncased") + '/'
    yaml_content["MODEL"]["WORDGRID"]["MODEL_PATH"] = embedding_model_path

    with open(join(PROJECT_ROOT_PATH, "src", "model_configuration", f"{model_name}_VGT_cascade_PTM.yaml"), "w") as file:
        yaml.dump(yaml_content, file)


def register_data():
    register_coco_instances(
        "predict_data",
        {},
        JSON_TEST_FILE_PATH,
        IMAGES_ROOT_PATH
    )


def predict(model_name: str):
    register_data()
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    os.environ["TORCH_DISTRIBUTED_DEBUG"] = "DETAIL"

    launch(
        main,
        doclaynet_args.num_gpus,
        num_machines=doclaynet_args.num_machines,
        machine_rank=doclaynet_args.machine_rank,
        dist_url=doclaynet_args.dist_url,
        args=(doclaynet_args,),
    )
