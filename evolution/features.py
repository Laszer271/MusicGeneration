import numpy as np
from .utils import representations as rep
from .utils import tonality
from .utils import utils

# statistical features
def calculate_mean_pitch(gen_vec, _):
    notes = gen_vec[gen_vec >= utils.LOWEST_PITCH]
    if notes.size == 0:
        return 0.5
    mean = np.average(notes)
    return mean / utils.HIGHEST_PITCH
def calculate_pitch_deviation(gen_vec, _):
    notes = gen_vec[gen_vec >= utils.LOWEST_PITCH]
    if notes.size == 0:
        return 0
    deviation = np.std(notes)
    return deviation / utils.HIGHEST_PITCH
def calculate_off_scale_notes(gen_vec, music_key):
    off_scale_notes_no = np.count_nonzero(np.isin(gen_vec[gen_vec >= utils.LOWEST_PITCH], music_key) == False)
    notes_no = np.count_nonzero(gen_vec[gen_vec >= utils.LOWEST_PITCH])
    if notes_no == 0:
        return 0
    return off_scale_notes_no / notes_no
'''
def get_chord_pitches(gen_vec):
    return
def get_dissonances(gen_vec):
    return
'''
def calculate_minor_and_major_seconds(gen_vec, _):
    intervals = utils.get_intervals(gen_vec)
    if intervals.size == 0:
        return 0
    seconds_no = np.count_nonzero(np.isin(intervals, np.array([utils.MINOR_SECOND_INTERVAL, utils.MAJOR_SECOND_INTERVAL])))
    return seconds_no / intervals.size
def calculate_intervals_smaller_than_octave(gen_vec, _):
    intervals = utils.get_intervals(gen_vec)
    if intervals.size == 0:
        return 0
    intervals_smaller_than_octave_no = np.count_nonzero(intervals <= utils.OCTAVE_LENGTH)
    return intervals_smaller_than_octave_no / intervals.size
def calculate_mean_rhythmic_value(gen_vec, _):
    mean = np.average( np.log( np.array(rep.gen_to_midi(gen_vec)[1]) / 4 + 1 ) )
    whole_notes = np.log(5)
    return mean / whole_notes
def calculate_rhythm_deviation(gen_vec, _):
    deviation = np.std( np.log( np.array(rep.gen_to_midi(gen_vec)[1]) / 4 + 1 ) )
    whole_notes = np.log(5)
    return deviation / whole_notes
def calculate_notes_in_strong_beat(gen_vec, _):
    strong_beats = gen_vec[0::8]
    if strong_beats.size == 0:
        return 1
    notes_in_strong_beat_no = np.count_nonzero(strong_beats >= utils.LOWEST_PITCH)
    return notes_in_strong_beat_no / strong_beats.size
def calculate_rests_to_notes_ratio(gen_vec, _):
    rhythmical_no = np.count_nonzero(gen_vec >= utils.REST_VALUE)
    if rhythmical_no == 0:
        return 0
    rests_no = np.count_nonzero(gen_vec == utils.REST_VALUE)
    return rests_no / rhythmical_no

# calculation, weight, mean value, standard deviation
mean_pitch = (calculate_mean_pitch, 1, 0.564, 0.065)
pitch_deviation = (calculate_pitch_deviation, 1, 0.053, 0.013)
off_scale_notes = (calculate_off_scale_notes, 1, 0, 0.05)
minor_and_major_seconds = (calculate_minor_and_major_seconds, 1, 0.553, 0.078)
intervals_smaller_than_octave = (calculate_intervals_smaller_than_octave, 1, 1, 0.1)
mean_rhythmic_value = (calculate_mean_rhythmic_value, 1, 0.282, 0.12)
rhythm_deviation = (calculate_rhythm_deviation, 1, 0.156, 0.058)
notes_in_strong_beat = (calculate_notes_in_strong_beat, 1, 0.788, 0.218)
rests_to_notes_ratio = (calculate_rests_to_notes_ratio, 1, 0.105, 0.092)

statistical_features = np.array([mean_pitch, pitch_deviation, off_scale_notes, minor_and_major_seconds, intervals_smaller_than_octave,
                                 mean_rhythmic_value, rhythm_deviation, notes_in_strong_beat, rests_to_notes_ratio])
