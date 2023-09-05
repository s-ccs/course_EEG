from matplotlib import pyplot as plt

import os.path as op

import mne
from mne.datasets import eegbci
from mne.datasets import fetch_fsaverage

# Download fsaverage files
fs_dir = fetch_fsaverage(verbose=True)
subjects_dir = op.dirname(fs_dir)

# The files live in:
subject = 'fsaverage'
trans = 'fsaverage'  # MNE has a built-in fsaverage transformation
src = op.join(fs_dir, 'bem', 'fsaverage-ico-5-src.fif')
bem = op.join(fs_dir, 'bem', 'fsaverage-5120-5120-5120-bem-sol.fif')

from mne.datasets.limo import load_data
epochs = load_data(subject=3,path='../local/limo') #
epochs.set_eeg_reference(projection=True)  # needed for inverse modeling





# Check that the locations of EEG electrodes is correct with respect to MRI

mne.viz.set_3d_backend("pyvista")

p = mne.viz.plot_alignment(
    epochs.info, src=src, eeg=['original', 'projected'], trans="fsaverage", # try trans=None for fun
    show_axes=True, mri_fiducials=True, dig='fiducials')

p