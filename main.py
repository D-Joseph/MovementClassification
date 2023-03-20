import numpy as np
import pandas as pd
import h5py as h5
import 

with h5.File('./hdf5_data.h5', 'w') as hdf:
    char = hdf.create_group('/Char')
    char.create_dataset('walkingHand', data=pd.read_csv('CharWalkingHand.csv'), compression='gzip', compression_opts=7)
    char.create_dataset('walkingPant', data=pd.read_csv('CharWalkingFrontPocket.csv'), compression='gzip', compression_opts=7)
    char.create_dataset('walkingJacket', data=pd.read_csv('CharWalkingJacketPocket.csv'), compression='gzip', compression_opts=7)
    char.create_dataset('jumpingPant', data=pd.read_csv('CharJumpingFrontPocket.csv'), compression='gzip', compression_opts=7)
    char.create_dataset('jumpingHand', data=pd.read_csv('CharJumpingHand.csv'), compression='gzip', compression_opts=7)

    nile = hdf.create_group('/Nile')
    nile.create_dataset('walkingHand', data=pd.read_csv('handWalkingNile.csv'), compression='gzip', compression_opts=7)
    nile.create_dataset('walkingPant', data=pd.read_csv('pantWalkingNile.csv'), compression='gzip', compression_opts=7)
    nile.create_dataset('walkingJacket', data=pd.read_csv('CoatWalkingNile.csv'), compression='gzip', compression_opts=7)
    nile.create_dataset('jumpingPant', data=pd.read_csv('CharJumpingFrontPocket.csv'), compression='gzip', compression_opts=7)
    nile.create_dataset('jumpingHand', data=pd.read_csv('CharJumpingHand.csv'), compression='gzip', compression_opts=7)
    nile.create_dataset('jumpingJacket', data=pd.read_csv('CoatJumpingNile.csv'), compression='gzip', compression_opts=7)

    dan = hdf.create_group('/Dan')
    dan.create_dataset('walkingHand', data=pd.read_csv('DanielWalkingHand.csv'), compression='gzip', compression_opts=7)
    dan.create_dataset('walkingPant', data=pd.read_csv('DanielWalkingPant.csv'), compression='gzip', compression_opts=7)
    dan.create_dataset('walkingJacket', data=pd.read_csv('DanielWalkingJacket.csv'), compression='gzip', compression_opts=7)
    dan.create_dataset('jumpingPant', data=pd.read_csv('DanielJumpingPant.csv'), compression='gzip', compression_opts=7)
    dan.create_dataset('jumpingHand', data=pd.read_csv('DanielJumpingHand.csv'), compression='gzip', compression_opts=7)


    test = hdf.create_group('/Dataset/test')

    train = hdf.create_group('/Dataset/train')
