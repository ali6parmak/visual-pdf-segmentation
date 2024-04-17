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


def main(args):
    cfg = setup(args)
    if args.eval_only:
        model = MyTrainer.build_model(cfg)
        DetectionCheckpointer(model, save_dir=cfg.OUTPUT_DIR).resume_or_load(
            cfg.MODEL.WEIGHTS, resume=args.resume
        )
        res = MyTrainer.test(cfg, model)
        return res

    trainer = MyTrainer(cfg)
    trainer.resume_or_load(resume=args.resume)
    return trainer.train()


def get_args():
    parser = default_argument_parser()
    parser.add_argument("--debug", action="store_true", help="enable debug mode")
    args = parser.parse_args()
    args.config_file = join(PROJECT_ROOT_PATH, "src", "model_configuration", "VGT_cascade_PTM.yaml")
    args.eval_only = True
    args.num_gpus = 1
    args.opts = ['MODEL.WEIGHTS', join(PROJECT_ROOT_PATH, 'models', 'D4LA_VGT_model.pth'),
                 'OUTPUT_DIR', join(PROJECT_ROOT_PATH, 'model_output')]
    args.debug = False
    return args


def prepare_model_path():
    os.makedirs(join(PROJECT_ROOT_PATH, "model_output"), exist_ok=True)
    with open(join(PROJECT_ROOT_PATH, "src", "model_configuration", "VGT_cascade_PTM.yaml"), "r") as file:
        yaml_content = yaml.safe_load(file)

    embedding_model_path = join(PROJECT_ROOT_PATH, "models", "layoutlm-base-uncased") + '/'
    yaml_content["MODEL"]["WORDGRID"]["MODEL_PATH"] = embedding_model_path

    with open(join(PROJECT_ROOT_PATH, "src", "model_configuration", "VGT_cascade_PTM.yaml"), "w") as file:
        yaml.dump(yaml_content, file)


def register_data():
    register_coco_instances(
        "predict_data",
        {},
        JSON_TEST_FILE_PATH,
        IMAGES_ROOT_PATH
    )


def predict():
    prepare_model_path()
    args = get_args()
    register_data()
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    os.environ["TORCH_DISTRIBUTED_DEBUG"] = "DETAIL"

    launch(
        main,
        args.num_gpus,
        num_machines=args.num_machines,
        machine_rank=args.machine_rank,
        dist_url=args.dist_url,
        args=(args,),
    )


if __name__ == '__main__':
    predict()
