# -*- coding: utf-8 -*-
"""
Created on Sep 19 14:50:03 2019
@author: Gabriel Michau

A Python function to read .tps files
"""
import numpy as np
import re

def readTPS(fileID):

    s = fileID.read()
    fileID.close()

    # Read settings
    ################
    # 1 - Voltage range (per channel)
    channelVRange = [m.start()+8 for m in re.finditer(b'BNDS', s)] #=>
    channelVRange = [np.frombuffer(s[i:i+16], "float64").tolist() for i in channelVRange]

    # 2 - Sampling Frequency (per channel)
    samplingFreq = [m.start()+8 for m in re.finditer(b'SAFR', s)]
    samplingFreq = [np.frombuffer(s[i:i+8], "float64")[0] for i in samplingFreq]
    if len(set(samplingFreq)) > 1:
        raise ValueError('Channels frequencies not consistent ({})'.format(' - '.join([str(i) for i in samplingFreq])))
    else:
        samplingFreq = int(samplingFreq[0])

    # 3 - Number of samples per channel
    channelLength = [m.start()+8 for m in re.finditer(b'DASI', s)]
    channelLength = [np.frombuffer(s[i:i+8], "int64")[0] for i in channelLength]
    if len(set(channelLength)) > 1:
        raise ValueError('Channel lengths not consistent')
    else:
        channelLength = int(channelLength[0])

    # Other keys to explore (can be commented)
    #################################################################
    # Channel ID
    channelID = [m.start()+8 for m in re.finditer(b'NUM ', s)]
    channelID = [np.frombuffer(s[i:i+4], "int32") for i in channelID]

    # Channel number
    channelNumber = [m.start()+8 for m in re.finditer(b'OUT#', s)]
    channelNumber = [np.frombuffer(s[i:i+4], "int32") for i in channelNumber]

    # Resolution (bits) per channel
    reso = [m.start()+8 for m in re.finditer(b'RESO', s)]
    reso = [np.frombuffer(s[i:i+4], "int32") for i in reso]


    # Other keys whose encoding / meaning is not clear
    # #######################################################
    fmt = [m.start()+8 for m in re.finditer(b'FMT ', s)]
    fmt = [np.frombuffer(s[i:i+4], "int32") for i in fmt]
    fmt = [np.frombuffer(s[i:i+4], "float32") for i in fmt]

    # PRSA
    prsa = [m.start()+8 for m in re.finditer(b'PRSA', s)]
    prsa = [np.frombuffer(s[i:i+8], "int64") for i in prsa]

    # DOMN
    domn = [m.start()+8 for m in re.finditer(b'DOMN', s)]
    domn = [np.frombuffer(s[i:i+4], "int32") for i in domn]
    domn = [np.frombuffer(s[i:i+4], "float32") for i in domn]

    # clid
    clid = [m.start()+8 for m in re.finditer(b'CLID', s)]
    clid = [np.frombuffer(s[i:i+8], "int64") for i in clid]

    keys = [\
    'RIFF',
    'INSTSVER',
    'LVER',
    'LTPC',
    'NUM ',
    'NAME',
    'NMSH',
    'CLID',
    'OCNT',
    'TIME',
    'FVER',
    'DVER',
    'DVID',
    'SACU',
    'SANE',
    'RIFF',
    'NAME',
    'CLID',
    'NUM ',
    'OUT#',
    'BNDS',
    'DATY',
    'DOMN',
    'DASI',
    'PRSA',
    'SAFR',
    'RESO',
    'FMT ',
    'DATA',
    'COLR']
    
	# Read Data
    ##########################
    channelStart = [m.start()+8 for m in re.finditer(b'DATA', s)]

    data = np.empty((channelLength,channelStart.__len__()),dtype=np.float32)
    for channel in range(channelStart.__len__()):
        data[:,channel] = np.frombuffer(s[channelStart[channel]:channelStart[channel]+4*channelLength], "float32")

    return data,samplingFreq,channelVRange[:channelStart.__len__()]