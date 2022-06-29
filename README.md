# Related Works

1) [**TS-RIR: Translated synthetic room impulse responses for speech augmentation (IEEE ASRU 2021)**](https://github.com/GAMMA-UMD/TS-RIR)
2) [**FAST-RIR: FAST NEURAL DIFFUSE ROOM IMPULSE RESPONSE GENERATOR (ICASSP 2022)**](https://github.com/anton-jeran/FAST-RIR)
3) [**MESH2IR: Neural Acoustic Impulse Response Generator for Complex 3D Scenes (ACM Multimedia 2022)**](https://anton-jeran.github.io/M2IR/)


# IR-GAN (INTERSPEECH 2021)

This is the official implementation of **IR-GAN**. This is the extension of **WaveGAN** to augment Room Impulse Response (RIR). You can find more details on this project here https://gamma.umd.edu/pro/speech/ir-gan.

Video : https://www.youtube.com/watch?v=_v5rDmDXvD0



## Requirements

```
tensorflow-gpu==1.12.0
scipy==1.0.0
matplotlib==3.0.2
librosa==0.6.2
ffmpeg ==4.2.1
cuda ==9.0.176
cudnn ==7.6.5
Matlab
```

## Datasets

In order to train **WaveGAN** to map low dimensional latent vectors to high dimensional space where room impulse response is present, use the following recorded RIR from **BUT ReverbDB**. Unzip **RIR** directory inside **IR-GAN** folder.

https://drive.google.com/file/d/1YX1XEpJ2W1cZD4Dn7d5CRBVPOFLUKG4B/view?usp=sharing


You can generate RIR using the following trained models (https://drive.google.com/file/d/1IktFk27UnJx7ycGlOnc71VX7GuFRwR7L/view?usp=sharing). Copy these trained models to **RIR_Generation folder**.

## IR Statistics Toolbox

We need following Matlab toolbox to calculate Room Impulse Response Statistics (https://www.mathworks.com/matlabcentral/fileexchange/42566-impulse-response-acoustic-information-calculator).

```
Christopher Hummersone (2020). Impulse response acoustic information calculator (https://github.com/IoSR-Surrey/MatlabToolbox), GitHub. Retrieved October 31, 2020.
```

## Train a WaveGAN

You can train **WaveGAN** to generate RIR using the following command

```
export CUDA_VISIBLE_DEVICES=0
python3 train_wavegan.py train ./train --data_dir RIR/ --data_first_slice --data_pad_end --data_fast_wav
```
## Generate RIR

Copy the trained models inside train directory or download the trained models() to **RIR Generation** folder. You can generate constrained RIR using the following command. 


```
python3 Augment_RIR.py
```

You can edit number of RIRs to be generated inside the file **Augment_RIR.py**

You can generate intermediate RIRs with given upper and lower limits of **Ditrect to reverberant ratio (DRR)** using the following command

```
python3 Vector_Arithmatic.py
```
you can edit the upper and lower limit inside the file **Vector_Arithmatic.py**


### Attribution

If you use this code in your research, please consider citing

```
@inproceedings{ratnarajah21_interspeech,
  author={Anton Ratnarajah and Zhenyu Tang and Dinesh Manocha},
  title={{IR-GAN: Room Impulse Response Generator for Far-Field Speech Recognition}},
  year=2021,
  booktitle={Proc. Interspeech 2021},
  pages={286--290},
  doi={10.21437/Interspeech.2021-230}
}
```

```
@inproceedings{donahue2019wavegan,
  title={Adversarial Audio Synthesis},
  author={Donahue, Chris and McAuley, Julian and Puckette, Miller},
  booktitle={ICLR},
  year={2019}
}
```

If you use recorded RIR from **BUT ReverbDB**, please consider citing
```
@article{DBLP:journals/jstsp/SzokeSMPC19,
  author    = {Igor Sz{\"{o}}ke and
               Miroslav Sk{\'{a}}cel and
               Ladislav Mosner and
               Jakub Paliesek and
               Jan Honza Cernock{\'{y}}},
  title     = {Building and Evaluation of a Real Room Impulse Response Dataset},
  journal   = {{IEEE} J. Sel. Top. Signal Process.},
  volume    = {13},
  number    = {4},
  pages     = {863--876},
  year      = {2019}
}
```



