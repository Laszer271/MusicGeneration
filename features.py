import numpy as np
import representations as rep
import tonality
import utils

# rule-based features
def mean_pitch(gen_vec):
    mean = np.average(gen_vec[gen_vec >= utils.LOWEST_PITCH])
    return mean / utils.HIGHEST_PITCH
def pitch_deviation(gen_vec):
    deviation = np.std(gen_vec[gen_vec >= utils.LOWEST_PITCH])
    return deviation / utils.HIGHEST_PITCH
def off_scale_notes(gen_vec, music_key):
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
def minor_and_major_seconds(gen_vec):
    intervals = utils.get_intervals(gen_vec)
    if intervals.size == 0:
        return 0
    seconds_no = np.count_nonzero(np.isin(intervals, np.array([utils.MINOR_SECOND_INTERVAL, utils.MAJOR_SECOND_INTERVAL])))
    return seconds_no / np.count_nonzero(intervals)
def intervals_larger_than_octave(gen_vec):
    intervals = utils.get_intervals(gen_vec)
    if intervals.size == 0:
        return 0
    intervals_larger_than_octave_no = np.count_nonzero(intervals > utils.OCTAVE_LENGTH)
    return intervals_larger_than_octave_no / np.count_nonzero(intervals)
def get_mean_rhythmic_value(gen_vec):
    #TODO
    return np.average(rep.gen_to_midi(gen_vec)[1])
def get_rhythm_deviation(gen_vec):
    #TODO
    return np.std(rep.gen_to_midi(gen_vec)[1])
def notes_in_strong_beat(gen_vec):
    strong_beats = gen_vec[0::8]
    if strong_beats.size == 0:
        return 1
    notes_in_strong_beat_no = np.count_nonzero(strong_beats >= utils.LOWEST_PITCH)
    return notes_in_strong_beat_no / strong_beats.size
def rests_to_notes_ratio(gen_vec):
    rhythmical_no = np.count_nonzero(gen_vec >= utils.REST_VALUE)
    if rhythmical_no == 0:
        return 0
    rests_no = np.count_nonzero(gen_vec == utils.REST_VALUE)
    return rests_no / rhythmical_no
