import pendulum
from pynwb import NWBHDF5IO
from pynwb.file import Subject
from simply_nwb import SimpleNWB
from simply_nwb.pipeline import NWBSession
from simply_nwb.pipeline.enrichments.saccades import PutativeSaccadesEnrichment
from simply_nwb.pipeline.enrichments.saccades.predict_gui import PredictedSaccadeGUIEnrichment
import random
import os

NUM_TRAINING_FILES = 5
RECORDING_FPS = 150


def find_training_putatives(foldername):
    filenames = []
    for fn in os.listdir(foldername):
        if fn.endswith(".nwb"):
            filenames.append(fn)
    
    trainings = []
    for i in range(NUM_TRAINING_FILES):
        trainings.append(os.path.join(foldername, filenames[random.randint(1, len(filenames)) - 1]))
    
    trainings = list(set(trainings))
    return trainings


def process_sess(foldername, filename):
    sess = NWBSession(os.path.join(foldername, filename))
    # Take our putative saccades and do the actual prediction for the start, end time, and time location
    print("Adding predictive data..")
    enrich = PredictedSaccadeGUIEnrichment(RECORDING_FPS, find_training_putatives(foldername), 40, {
        "x_center": "center_x", "y_center": "center_y", "likelihood": "center_likelihood"})

    sess.enrich(enrich)
    print("Saving to NWB")
    new_filename = filename[len("putative-"):]  # Remove the 'putative-' prefix from the filename to generate a new one
    new_filename = "predicted-" + new_filename
    sess.save(new_filename)  # Save as our finalized session, ready for analysis
    tw = 2


def main():
    for filename in os.listdir("putative"):
        if filename.endswith(".nwb"):
            process_sess("putative", filename)



if __name__ == "__main__":
    main()
