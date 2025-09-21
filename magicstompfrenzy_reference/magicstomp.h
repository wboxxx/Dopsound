/*
 * Copyright (C) 2018 Robert Vetter.
 * This file is part of the MagicstompFrenzy - an editor for Yamaha Magicstomp
 * effect processor
 * 
 * Original source: https://github.com/dulnikovsky/magicstompfrenzy
 * License: GPL-3.0
 * 
 * PATCH STRUCTURE AND EFFECT DEFINITIONS
 * =====================================
 */

#ifndef MAGICSTOMP_H
#define MAGICSTOMP_H

static const int numOfPatches = 99;
static const int PatchNameLength = 12;

// KEY: Patch structure offsets
enum MagistompPatchDesc
{
    PatchType,
    Control1 = 2,           // Physical potentiometer 1 assignment
    Control2 = 4,           // Physical potentiometer 2 assignment  
    Control3 = 6,           // Physical potentiometer 3 assignment
    PatchName = 16,
    PatchNameLast = PatchName + PatchNameLength,
    PatchCommonLength = 0x20,    // 32 bytes for common parameters
    PatchEffectLength = 0x7F,    // 127 bytes for effect parameters
    PatchTotalLength = PatchCommonLength + PatchEffectLength
};

// KEY: Effect type IDs for potentiometer assignment
enum EffectTypeId
{
    AcousticMulti = 0x00,
    EightBandParallelDelay = 0x01,
    EightBandSeriesDelay = 0x02,
    FourBand2TapModDelay = 0x03,
    TwoBand4TapModDelay = 0x04,
    EightMultiTapModDelay = 0x05,
    TwoBandLong4ShortModDelay = 0x06,
    ShortMediumLongModDelay = 0x07,
    AmpSimulator = 0x08,
    Reverb = 0x09,
    EarlyRef = 0x0A,
    GateReverb = 0x0B,
    ReverseGate = 0x0C,
    MonoDelay = 0x0D,       // KEY: Used in our tests
    StereoDelay = 0x0E,
    ModDelay = 0x0F,
    DelayLCR = 0x10,
    Echo = 0x11,
    Chorus = 0x12,
    Flange = 0x13,
    Symphonic = 0x14,
    Phaser = 0x15,
    AutoPan = 0x16,
    Tremolo = 0x17,
    HQPitch = 0x18,
    DualPitch = 0x19,
    Rotary = 0x1A,
    RingMod = 0x1B,
    ModFilter = 0x1C,
    DigitalDistortion = 0x1D,
    DynaFilter = 0x1E,
    DynaFlange = 0x1F,
    DynaPhaser = 0x20,
    ReverbChorusParallel = 0x21,
    ReverbChorusSerial = 0x22,
    ReverbFlangeParallel = 0x23,
    ReverbFlangeSerial = 0x24,
    ReverbSymphonicParallel = 0x25,
    ReverbSymphonicSerial = 0x26,
    ReverbPan = 0x27,
    DelayEarlyRefParallel = 0x28,
    DelayEarlyRefSerial = 0x29,
    DelayReverbParallel = 0x2A,
    DelayReverbSerial = 0x2B,
    DistortionDelay = 0x2C,
    MultiFilter = 0x2D,
    MBandDyna = 0x2E,
    Distortion = 0x2F,
    VintageFlange = 0x30,
    MonoVintagePhaser = 0x31,
    StereoVintagePhaser = 0x32,
    ThreeBandParametricEQ = 0x33,
    SpringReverb = 0x34,
    TapeEcho = 0x35,
    Compressor = 0x36,
    AmpMultiChorus = 0x37,
    AmpMultiFlange = 0x38,  // KEY: Used in our tests
    AmpMultiTremolo = 0x39,
    AmpMultiPhaser = 0x3A,
    AmpMultiRotary = 0x3B,
    AmpMultiPan = 0x3C,
    AmpMultiPitch = 0x3D,
    AmpMultiFilter = 0x3E,
    AmpMultiDistortion = 0x3F,
    BassPreamp = 0x40,
    BassMultiChorus = 0x41,
    BassMultiFlange = 0x42,
    BassMultiTremolo = 0x43,
    BassMultiPhaser = 0x44,
    BassMultiRotary = 0x45,
    BassMultiPan = 0x46,
    BassMultiPitch = 0x47,
    BassMultiFilter = 0x48,
    BassMultiDistortion = 0x49
};

#endif // MAGICSTOMP_H
