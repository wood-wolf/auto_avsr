import hydra
from pytorch_lightning import seed_everything
import os


@hydra.main(config_path="conf", config_name="config")
def main(cfg):
    print(cfg.ckpt_path)
    seed_everything(42, workers=True)
    # dataloader = DataModule(cfg).train_dataloader()
    # print(dataloader[0])


if __name__ == '__main__':
    os.environ['HYDRA_FULL_ERROR'] = '1'
    main()
