# Signal processing and analysis of human brain potentials (EEG) [Exercise 1]

## Overview
In this exercise we will install the mne-python toolbox, download a example dataset, make some basic visualizations and epoch, average and visualize the resulting ERPs.

What we are doing is roughly outlined in the "What is EEG" video lecture.

## Install MNE toolbox
run `pip install mne`
or if you like conda:
`conda install -c conda-forge mne`

similarly, install `pip install mne-bids`, a tool to load the EEG data easily.

Test the installation by
`import mne`

## Download data
We will be using a typical P3 oddball dataset. We expect a positive response over parietal/central electrodes (Cz/Pz) starting at 300-400ms, [something like this](https://www.neurobs.com/manager/content/docs/psychlab101_experiments/Oddball%20Task%20(Visual)/description.html).

If you want to read the details you can find it [here](https://psyarxiv.com/4azqm/). You can also investigate the `sub-030_task-P3_eeg.json` for a task description which is one of the files you will download next:

Please download the data from [](https://osf.io/9cnmx/)


Next, you need the [ccs_eeg_utils.py](ccs_eeg_utils.py) file which you can add to your python code e.g. via
```python
import sys
sys.path.insert(0,'.')
```

## Load data & plot continuous EEG
```python
# Load the data
from mne_bids import (BIDSPath,read_raw_bids)

# path where to save the datasets.
bids_root = "../local/bids"
subject_id = '030' # recommend subject 30 for now


bids_path = BIDSPath(subject=subject_id,task="P3",session="P3",
                     datatype='eeg', suffix='eeg',
                     root=bids_root)

# read the file
raw = read_raw_bids(bids_path)
# fix the annotations readin
ccs_eeg_utils.read_annotations_core(bids_path,raw)

```

**Task:** Extract a single channel and plot the whole timeseries. 

:::callout-note

You can directly interact with the `raw` object, e.g. `raw[1:10,1:5000]`, which extracts the first 10 channels and 5000 samples.

You can also use `raw.get_data()` to get the whole data as a numpy array.

:::

::: callout-tipp

For now we can use simple matplotlib to visualize the data, e.g.:
```python
from matplotlib import pyplot as plt
plt.plot(raw[10,:][0].T)
```

:::

**Question:** What is the range of the data (in sense of min-y to max-y in µ-volt)?

**Task:** Have a look at `raw.info` and note down what the sampling frequency is (how many EEG-samples per second)

## Epoching 

**Task:** We will epoch the data now. Formost we will cut the raw data to one channel using `raw.pick(["Cz"])` - note that this will permanently change the `raw` object and **removes** alle other channels from memory. If you want rather a copy you could use `raw_subselect = raw.copy().pick(["Cz"]))`.


**Task** Let's investigate the annotation markers. Have a look at raw.annotations. These values reflect the values in the bids `*_events.tsv`  file (have a look at this file via `../local/bids/sub-030/sub-030_task-P3_events.tsv`). BIDS is a new standard to share neuroimaging and other physiological data. It is not really a fileformat, but more of a folder & filename structure with some additional json files. I highly recommend to put your data into bids-format as soon as possible. It helps you stay organized and on top of things!


**Task** MNE-speciality: We have to convert annotations to events with `evts,evts_dict = mne.events_from_annotations(raw)`. Have a look at evts - it shows you the sample, the duration and event-id (with the look-up table evts_dict). In this case we only want to look at stimulus evoked responses, so we subset the event table (note: this could be done after epoching too)

```python
# get all keys which contain "stimulus"
wanted_keys = [e for e in evts_dict.keys() if "stimulus" in e]
# subset the large event-dictionairy
evts_dict_stim=dict((k, evts_dict[k]) for k in wanted_keys if k in evts_dict)
```

**Task** Epoch the data with `epochs = mne.Epochs(raw,evts,evts_dict_stim,tmin=-0.1,tmax=1)`

**Task** Now that we have the epochs we should plot them. Plot all trials 'manually', (without using mne's functionality) (`epochs.get_data()`).

::: callout-note

You should plot one line per trial.

:::

**Question** What is the scale-range of the epoched data now?

## My first ERP

**Task** But which epochs belong to targets and which to distractors? This is hidden in the event-description. Using the following lines you can find out which indices belong to which trial-types
```python
target = ["stimulus:{}{}".format(k,k) for k in [1,2,3,4,5]]
distractor = ["stimulus:{}{}".format(k,j) for k in [1,2,3,4,5] for j in [1,2,3,4,5] if k!=j]
```
Now index the epochs `evoked = epochs[index].average()` and average them. You can then plot them either via `evoked.plot()` or with `mne.viz.plot_compare_evokeds([evokedA,evokedB])`.

**Question** What is the unit/scale of the data now? Set it into context to the other two scales you reported before

