/*
 * Copyright (C) 2019 Robert Vetter.
 * This file is part of the MagicstompFrenzy - an editor for Yamaha Magicstomp
 * effect processor
 * 
 * Original source: https://github.com/dulnikovsky/magicstompfrenzy
 * License: GPL-3.0
 * 
 * COMPLETE PARAMETER MAPPING FOR ALL EFFECTS
 * ==========================================
 */

#ifndef KNOBPARAMETERS_H
#define KNOBPARAMETERS_H

#include <QMap>
#include <QString>

// KEY: AmpMultiFlange parameters (used in our tests)
const QMap<int, QString> AmpMultiFlangeKnobParameters =
{
    {  2, QStringLiteral("Compressor Threshold") },
    {  3, QStringLiteral("Flanger Delay") },
    {  4, QStringLiteral("Delay Feedback") },
    {  5, QStringLiteral("Reverb Ini. Delay") },
    { 11, QStringLiteral("Amp Type") },
    { 19, QStringLiteral("Gain") },
    { 20, QStringLiteral("Master") },
    { 21, QStringLiteral("Bass") },
    { 22, QStringLiteral("Middle") },
    { 23, QStringLiteral("Treble") },
    { 24, QStringLiteral("Presence") },
    { 25, QStringLiteral("Volume") },
    { 26, QStringLiteral("Stereo") },
    { 27, QStringLiteral("Bass Freq") },
    { 28, QStringLiteral("Middle Freq") },
    { 29, QStringLiteral("Treble Freq") },
    { 30, QStringLiteral("Presence Freq") },
    { 32, QStringLiteral("Flanger Type") },
    { 33, QStringLiteral("Flanger Speed") },
    { 34, QStringLiteral("Flanger Depth") },
    { 35, QStringLiteral("Flanger Feedback") },
    { 36, QStringLiteral("Flanger Manual") },
    { 37, QStringLiteral("Flanger Mix") },
    { 38, QStringLiteral("Flanger Stereo") },
    { 53, QStringLiteral("Flanger Depth") },      // KEY: Used in our tests
    { 54, QStringLiteral("Flanger Feedback") },   // KEY: Used in our tests
    { 67, QStringLiteral("Delay Level") },        // KEY: Used in our tests (DLVL)
    { 71, QStringLiteral("High Pass Filter") },   // KEY: Used in our tests (DHPF)
    { 72, QStringLiteral("Low Pass Filter") },    // KEY: Used in our tests
};

// KEY: MonoDelay parameters (used in our tests)
const QMap<int, QString> MonoDelayKnobParameters =
{
    {  0, QStringLiteral("Time") },
    {  8, QStringLiteral("Feedback") },
    {  9, QStringLiteral("Level") },
    { 10, QStringLiteral("High Pass Filter") },   // KEY: Used in our tests
    { 11, QStringLiteral("Low Pass Filter") },
    { 19, QStringLiteral("Tempo") },
    { 20, QStringLiteral("Note") },
    { 21, QStringLiteral("Dotted") },
    { 22, QStringLiteral("Triplet") }
};

// Reverb parameters
const QMap<int, QString> ReverbKnobParameters =
{
    {  0, QStringLiteral("Type") },
    {  8, QStringLiteral("Decay") },
    {  9, QStringLiteral("Pre Delay") },
    { 10, QStringLiteral("High Cut") },
    { 11, QStringLiteral("Low Cut") },
    { 19, QStringLiteral("Level") },
    { 20, QStringLiteral("Mix") },
    { 21, QStringLiteral("Stereo") }
};

// Compressor parameters
const QMap<int, QString> CompressorKnobParameters =
{
    {  0, QStringLiteral("Threshold") },          // KEY: Used in our tests
    { 19, QStringLiteral("Ratio") },
    { 20, QStringLiteral("Attack") },
    { 21, QStringLiteral("Release") },
    { 22, QStringLiteral("Knee") },
    { 23, QStringLiteral("Gain") }
};

// Bass Preamp parameters
const QMap<int, QString> BassPreampKnobParameters =
{
    {  0, QStringLiteral("Type") },
    {  8, QStringLiteral("Gain") },
    {  9, QStringLiteral("Master") },
    { 10, QStringLiteral("Bass") },
    { 11, QStringLiteral("Middle") },
    { 19, QStringLiteral("Treble") },
    { 20, QStringLiteral("Presence") },
    { 21, QStringLiteral("Volume") },
    { 22, QStringLiteral("Stereo") }
};

// Acoustic Multi parameters
const QMap<int, QString> AcousticMultiKnobParameters =
{
    { 11, QStringLiteral("Type") },
    { 19, QStringLiteral("Blend") },
    { 20, QStringLiteral("Bass") },
    { 21, QStringLiteral("Middle") },
    { 22, QStringLiteral("Treble") },
    { 23, QStringLiteral("Presence") },
    { 24, QStringLiteral("Volume") },
    { 25, QStringLiteral("Stereo") },
    { 26, QStringLiteral("Bass Freq") },
    { 27, QStringLiteral("Middle Freq") },
    { 28, QStringLiteral("Treble Freq") },
    { 29, QStringLiteral("Presence Freq") },
    { 30, QStringLiteral("Limiter On/Off") },
    { 32, QStringLiteral("Chorus/Delay Type") },
    { 34, QStringLiteral("Reverb Type") },
    { 36, QStringLiteral("Limiter") },
    { 37, QStringLiteral("Speed/Time") },
    { 38, QStringLiteral("Depth/Feedback") },
    { 39, QStringLiteral("Chorus/Delay Level") },
    { 40, QStringLiteral("Reverb Level") }
};

// Distortion parameters
const QMap<int, QString> DistortionKnobParameters =
{
    {  0, QStringLiteral("EQ 1 Frequency") },
    {  1, QStringLiteral("Pre EQ Level") },
    {  8, QStringLiteral("Gain") },
    {  9, QStringLiteral("Master") },
    { 10, QStringLiteral("Tone") },
    { 11, QStringLiteral("Type") },
    { 19, QStringLiteral("EQ 1 Gain") },
    { 20, QStringLiteral("EQ 1 Q") },
    { 21, QStringLiteral("EQ 2 Frequency") },
    { 22, QStringLiteral("EQ 2 Gain") },
    { 23, QStringLiteral("EQ 2 Q") },
    { 24, QStringLiteral("EQ 3 Frequency") },
    { 25, QStringLiteral("EQ 3 Gain") },
    { 26, QStringLiteral("EQ 3 Q") },
    { 27, QStringLiteral("EQ 4 Frequency") },
    { 28, QStringLiteral("EQ 4 Gain") },
    { 29, QStringLiteral("EQ 4 Q") },
    { 32, QStringLiteral("Pre EQ 1 Frequency") },
    { 33, QStringLiteral("Pre EQ 1 Gain") },
    { 34, QStringLiteral("Pre EQ 1 Q") },
    { 35, QStringLiteral("Pre EQ 2 Frequency") },
    { 36, QStringLiteral("Pre EQ 2 Gain") },
    { 37, QStringLiteral("Pre EQ 2 Q") },
    { 38, QStringLiteral("Pre EQ 3 Frequency") },
    { 39, QStringLiteral("Pre EQ 3 Gain") },
    { 40, QStringLiteral("Pre EQ 3 Q") },
    { 42, QStringLiteral("Noise Gate Threshold") },
    { 43, QStringLiteral("Noise Gate Attack") },
    { 44, QStringLiteral("Noise Gate Hold") },
    { 45, QStringLiteral("Noise Gate Decay") }
};

// Flange parameters
const QMap<int, QString> FlangeKnobParameters =
{
    {   0, QStringLiteral("Modulation Delay") },
    {   8, QStringLiteral("Frequency") },
    {   9, QStringLiteral("Depth") },
    {  10, QStringLiteral("Feedback") },
    {  11, QStringLiteral("Wave") },
    {  19, QStringLiteral("LSH Frequency") },
    {  20, QStringLiteral("LSH Gain") },
    {  21, QStringLiteral("EQ Frequency") },
    {  22, QStringLiteral("EQ Gain") },
    {  23, QStringLiteral("EQ Q") },
    {  24, QStringLiteral("HSH Frequency") },
    {  25, QStringLiteral("HSH Gain") },
    {  29, QStringLiteral("Mix") }
};

// Phaser parameters
const QMap<int, QString> PhaserKnobParameters =
{
    {   0, QStringLiteral("Offset") },
    {   8, QStringLiteral("Frequency") },
    {   9, QStringLiteral("Depth") },
    {  10, QStringLiteral("Feedback Gain") },
    {  11, QStringLiteral("Stage") },
    {  19, QStringLiteral("Phase") },
    {  20, QStringLiteral("LSH Frequency") },
    {  21, QStringLiteral("LSH Gain") },
    {  22, QStringLiteral("HSH Frequency") },
    {  23, QStringLiteral("HSH Gain") },
    {  29, QStringLiteral("Mix") }
};

// Chorus parameters
const QMap<int, QString> ChorusKnobParameters =
{
    {   0, QStringLiteral("Modulation Delay") },
    {   8, QStringLiteral("Frequency") },
    {   9, QStringLiteral("Depth") },
    {  10, QStringLiteral("Feedback") },
    {  11, QStringLiteral("Wave") },
    {  19, QStringLiteral("LSH Frequency") },
    {  20, QStringLiteral("LSH Gain") },
    {  21, QStringLiteral("EQ Frequency") },
    {  22, QStringLiteral("EQ Gain") },
    {  23, QStringLiteral("EQ Q") },
    {  24, QStringLiteral("HSH Frequency") },
    {  25, QStringLiteral("HSH Gain") },
    {  29, QStringLiteral("Mix") }
};

// Tremolo parameters
const QMap<int, QString> TremoloKnobParameters =
{
    {   0, QStringLiteral("Rate") },
    {   8, QStringLiteral("Depth") },
    {   9, QStringLiteral("Wave") },
    {  10, QStringLiteral("Phase") },
    {  11, QStringLiteral("Offset") },
    {  19, QStringLiteral("LSH Frequency") },
    {  20, QStringLiteral("LSH Gain") },
    {  21, QStringLiteral("HSH Frequency") },
    {  22, QStringLiteral("HSH Gain") },
    {  29, QStringLiteral("Mix") }
};

// Spring Reverb parameters
const QMap<int, QString> SpringReverbKnobParameters =
{
    {  0, QStringLiteral("Reverb") }
};

// Tape Echo parameters
const QMap<int, QString> TapeEchoKnobParameters =
{
    {  0, QStringLiteral("Time") },
    { 19, QStringLiteral("Feedback") },
    { 20, QStringLiteral("Level") }
};

// Three Band Parametric EQ parameters
const QMap<int, QString> ThreeBandParametricEQKnobParameters =
{
    {  0, QStringLiteral("Level") },
    {  8, QStringLiteral("EQ 1 Frequency") },
    {  9, QStringLiteral("EQ 2 Frequency") },
    { 10, QStringLiteral("EQ 3 Frequency") },
    { 21, QStringLiteral("EQ 1 Gain") },
    { 22, QStringLiteral("EQ 2 Gain") },
    { 23, QStringLiteral("EQ 3 Gain") },
    { 27, QStringLiteral("EQ 1 Q") },
    { 28, QStringLiteral("EQ 2 Q") },
    { 29, QStringLiteral("EQ 3 Q") }
};

#endif // KNOBPARAMETERS_H


