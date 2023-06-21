# Auto-AVSR: Audio-Visual Speech Recognition
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/auto-avsr-audio-visual-speech-recognition/lipreading-on-lrs2)](https://paperswithcode.com/sota/lipreading-on-lrs2?p=auto-avsr-audio-visual-speech-recognition)
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/auto-avsr-audio-visual-speech-recognition/automatic-speech-recognition-on-lrs2)](https://paperswithcode.com/sota/automatic-speech-recognition-on-lrs2?p=auto-avsr-audio-visual-speech-recognition)
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/auto-avsr-audio-visual-speech-recognition/audio-visual-speech-recognition-on-lrs3-ted)](https://paperswithcode.com/sota/audio-visual-speech-recognition-on-lrs3-ted?p=auto-avsr-audio-visual-speech-recognition)

## Authors

[Pingchuan Ma](https://mpc001.github.io/), [Alexandros Haliassos](https://dblp.org/pid/257/3052.html), [Adriana Fernandez-Lopez](https://scholar.google.com/citations?user=DiVeQHkAAAAJ), [Honglie Chen](https://scholar.google.com/citations?user=HPwdvwEAAAAJ), [Stavros Petridis](https://ibug.doc.ic.ac.uk/people/spetridis), [Maja Pantic](https://ibug.doc.ic.ac.uk/people/mpantic).

## Content
[AutoAVSR](#content)
- [Introduction](#introduction)
- [Demo](#demo)
- [Training](#Training)
- [Testing](#Testing)
- [Inference](#Inference)
- [Training on other datasets](#Training-on-other-datasets)

[Model zoo](#model-zoo)

[Citation](#citation)

[License](#license)

[Contact](#contact)


## Introduction

This is the repository of [Auto-AVSR: Audio-Visual Speech Recognition with Automatic Labels](https://arxiv.org/abs/2303.14307), which is the successor of [End-to-End Audio-Visual Speech Recognition with Conformers](https://arxiv.org/abs/2102.06657). In this repository, we provide training code, pre-trained models, for end-to-end audio-visual speech recognition. The network architecture is based on 3D convolution, ResNet-18 plus Conformer as encoder and Transformer as decoder. We use CTC and CE loss for joint training.

<div align="center"><img src="doc/pipeline.png" width="640"/></div>

## Demo

You can check out our gradio demo below to inference your video (English) with our audio-only, visual-only and audio-visual speech recognition models.

[![Generic badge](https://img.shields.io/badge/🤗-Open%20In%20Spaces-blue.svg)](https://huggingface.co/spaces/mpc001/auto_avsr)

## Preparing the environment

1. Clone the repository and navigate to it:

```Shell
git clone https://github.com/mpc001/auto_avsr
cd auto_avsr
```

2. Set up the environment:

```Shell
conda create -y -n autoavsr python=3.8
conda activate autoavsr
```

3. To install the necessary packages, please follow the steps below:

- Step 3.1. Install pytorch, torchvision, and torchaudio by following instructions [here](https://pytorch.org/get-started/).

- Step 3.2. Install fairseq.

    ```Shell
    git clone https://github.com/pytorch/fairseq
    cd fairseq
    pip install --editable ./
    ```

- Step 3.3. Install ffmpeg by running the following command:

    ```Shell
    conda install -c conda-forge ffmpeg
    ```

- Step 3.4. Install additional packages by running the following command:

    ```Shell
    pip install -r requirements.txt
    ```

- Step 3.5. [For VSR] Install [retinaface](./tools) or [mediapipe](https://pypi.org/project/mediapipe/) tracker.

4. Prepare the dataset. See the instructions in the [preparation](./preparation) folder.

## Logging

For logging training process, we use [wandb](https://wandb.ai/). To customize the yaml file, match the file name with the team name in your account, e.g. [cassini.yaml](conf/logger/cassini.yaml). Then, change the `logger` argument in [conf/config.yaml](conf/config.yaml). Lastly, Don't forget to specify the `project` argument in [conf/logger/cassini.yaml](conf/logger/cassini.yaml). If you do not use wandb, please append `log_wandb=False` in the command.

## Training

By default, we use `data/dataset=lrs3`, which corresponds to [lrs3.yaml](conf/data/dataset/lrs3.yaml) in the configuration folder. To set up experiments, please fill in the `root` argument in the yaml file. Alternatively, you can append `data.dataset.root=[root_dir]` in your command line.

### Training from a pre-trained model

To fine-tune a ASR/VSR from a pre-trained model, for instance, LRW, you can run the command below. Note that the argument `ckpt_path=[ckpt_path] transfer_frontend=True` is specifically used to load the weights of the pre-trained front-end component only.

```Shell
python main.py exp_dir=[exp_dir] exp_name=[exp_name] data.modality=[modality] ckpt_path=[ckpt_path] transfer_frontend=True optimizer.lr=[lr] trainer.num_nodes=[num_nodes]
```

- `exp_dir` and `exp_name`: The directory where the checkpoints will be saved, will be stored at the location `[exp_dir]`/`[exp_name]`.

- `data.modality`: The valid values for the input modality: `video`, `audio`, and `audiovisual`.

- `ckpt_path`: The absolute path to the pre-trained checkpoint file.

- `transfer_frontend`: This argument loads only the front-end module of `[ckpt_path]` for fine-tuning.

- `trainer.num_nodes`: The number of machines used. Default: 1.

- `optimizer.lr`: The learing rate used. Default: 1e-3.

- Note: The performance [below](#model-zoo) were trained using 4 machines (32 GPUs), except for the models that were trained using VoxCeleb2 and/or AVSpeech, which used 8 machines (64GPUs). Additionally, for the model that was pre-trained on LRW, we used the front-end module [VSR accuracy: 89.6%; ASR accuracy: 99.1%] from the [LRW model zoo](https://github.com/mpc001/Lipreading_using_Temporal_Convolutional_Networks#model-zoo) for initialisation.

### Training from scratch through curriculum learning

The end-to-end model trained from scratch results in poor performance. This is likely due to the vast amounts of long utterances featured in the LRS3. This issue can be resolved by progressively training the end-to-end model. This approach is commonly called **curriculum learning**.


**[Step 1]** Train the model using a 23-hour subset of LRS3 that includes only short utterances lasting no more than 4 seconds.

```Shell
python main.py exp_dir=[exp_dir] exp_name=[exp_name] data.modality=[modality] data.dataset.train_file=[train_file] optimizer.lr=[lr] trainer.num_nodes=[num_nodes]
```

**[Step 2]** Use the best checkpoint from Step 1 to initialise the model and train the model with the full LRS3 dataset.

```Shell
python main.py exp_dir=[exp_dir] exp_name=[exp_name] data.modality=[modality] data.dataset.train_file=[train_file] optimizer.lr=[lr] trainer.num_nodes=[num_nodes] ckpt_path=[ckpt_path]
```

`data.dataset.train_file`: The training set list. Default: `lrs3_train_transcript_lengths_seg24s.csv`, which contains utterances lasting no more than 24 seconds.

## Testing

```Shell
python main.py exp_dir=[exp_dir] exp_name=[exp_name] data.modality=[modality] ckpt_path=[ckpt_path] trainer.num_nodes=1 train=False
```
- `ckpt_path`: The absolute path of the ensembled checkpoint file. In this case, `ckpt_path` is always set the file `[exp_dir]/[exp_name]/model_avg_10.pth`. Default: `null`.

- `decode.snr_target={snr}` can be appended to the command line if you want to test your model in a noisy environment, where `snr` is the signal-to-noise level. Default: `999999`.

- `data.dataset.test_file={test_file}` can be appeneded to the command line if you want to test models on other datasets, where `test_file` is the testing set list. Default: `lrs3_test_transcript_lengths_seg24s.csv`.

## Inference

```Shell
python infer.py data.modality=[modality] ckpt_path=[ckpt_path] trainer.num_nodes=1 infer_path=[infer_path]
```

- `ckpt_path`: The absolute path of the ensembled checkpoint file. In this case, `ckpt_path` is always set the file `[exp_dir]/[exp_name]/model_avg_10.pth`. Default: `null`.

- `infer_path`: The absolute path to the file you'd like to transcribe.

## Training on other datasets

We provide a tutorial that will guide you through the process of training an ASR/VSR model on other datasets using our scripts. Please refer to [INSTRUCTIONS](./INSTRUCTIONS.md).

## Model zoo

The table below contains WER on the test of LRS3.

| Total Training Data             | Hours‡ |  WER  | URL                                                                                                          | Params (M) |
|:-------------------------------:|:------:|:-----:|:-------------------------------------------------------------------------------------------------------------|:----------:|
| **Visual-only**                 |        |       |                                                                                                              |            |
| LRS3                            |  438   |  36.6 | [GoogleDrive](https://bit.ly/3COKHDn) / [BaiduDrive](https://bit.ly/3PdZKxy) (key: xv9r)                     |    250     |
| LRS2+LRS3                       |  661   |  32.7 | [GoogleDrive](https://bit.ly/443AzBY) / [BaiduDrive](https://bit.ly/3PfLbd8) (key: 4uew)                     |    250     |
| LRW+LRS2+LRS3+VOX2+AVSP         |  3448  |  19.1 | [GoogleDrive](http://bit.ly/40EAtyX) / [BaiduDrive](https://bit.ly/3ZjbrV5) (key: dqsy)                      |    250     |
| **Audio-only**                  |        |       |                                                                                                              |            |
| LRS3                            |  438   |  2.0  | [GoogleDrive](https://bit.ly/3p5rV7o) / [BaiduDrive](https://bit.ly/4639mRL) (key: 2x2a)                     |    243     |
| LRS2+LRS3                       |  661   |  1.7  | [GoogleDrive](https://bit.ly/3Nz9rFE) / [BaiduDrive](https://bit.ly/3CxMIn3) (key: s1ra)                     |    243     |
| LRW+LRS2+LRS3                   |  818   |  1.6  | [GoogleDrive](https://bit.ly/3JhKzje) / [BaiduDrive](https://bit.ly/46amLrq) (key: 9i2w)                     |    243     |
| LRW+LRS2+LRS3+VOX2+AVSP         |  3448  |  1.0  | [GoogleDrive](http://bit.ly/3ZSdh0l) / [BaiduDrive](http://bit.ly/3Z1TlGU) (key: dvf2)                       |    243     |

‡The total hours are counted by including the datasets used for both pre-training and training.

## Citation

```bibtex
@inproceedings{ma2023auto,
  author={Ma, Pingchuan and Haliassos, Alexandros and Fernandez-Lopez, Adriana and Chen, Honglie and Petridis, Stavros and Pantic, Maja},
  booktitle={IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
  title={Auto-AVSR: Audio-Visual Speech Recognition with Automatic Labels},
  year={2023},
  pages={1-5},
  doi={10.1109/ICASSP49357.2023.10096889}
}
```

## License

It is noted that the code can only be used for comparative or benchmarking purposes. Users can only use code supplied under a [License](./LICENSE) for non-commercial purposes.

## Contact

```
[Pingchuan Ma](pingchuan.ma16[at]imperial.ac.uk)
```
