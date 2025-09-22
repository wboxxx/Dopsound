/****************************************************************************
**
** Copyright (C) 2018 Robert Vetter.
**
** This file is part of the MagicstompFrenzy - an editor for Yamaha Magicstomp
** effect processor
**
** THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF
** ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY
** IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR
** PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.
**
** GNU General Public License Usage
** This file may be used under the terms of the GNU
** General Public License version 2.0 or (at your option) the GNU General
** Public license version 3 or any later version . The licenses are
** as published by the Free Software Foundation and appearing in the file LICENSE
** included in the packaging of this file. Please review the following
** information to ensure the GNU General Public License requirements will
** be met: https://www.gnu.org/licenses/gpl-2.0.html and
** https://www.gnu.org/licenses/gpl-3.0.html.
**/
#ifndef MAGICSTOMPTEXT_H
#define MAGICSTOMPTEXT_H

#include <QStringList>

const QStringList EffectTypeNameList =
{
    QStringLiteral("Acoustic Multi"),
    QStringLiteral("8 Band Parallel Delay"),
    QStringLiteral("8 Band Series Delay"),
    QStringLiteral("4 Band 2 Tap Mod. Delay"),
    QStringLiteral("2 Band 4 Tap Mod. Delay"),
    QStringLiteral("8 Multi Tap Mod. Delay"),
    QStringLiteral("2 Band Long + 4 Short Mod. Delay"),
    QStringLiteral("Short + Medium + Long Mod. Delay"),

    QStringLiteral("Amp Simulator"),
    QStringLiteral("Reverb"),
    QStringLiteral("Early Reflections"),
    QStringLiteral("Gate Reverb"),
    QStringLiteral("Reverse Gate"),
    QStringLiteral("Mono Delay"),
    QStringLiteral("Stereo Delay"),
    QStringLiteral("Mod. Delay"),

    QStringLiteral("Delay LCR"),
    QStringLiteral("Echo"),
    QStringLiteral("Chorus"),
    QStringLiteral("Flange"),
    QStringLiteral("Symphonic"),
    QStringLiteral("Phaser"),
    QStringLiteral("AutoPan"),
    QStringLiteral("Tremolo"),

    QStringLiteral("HQ Pitch"),
    QStringLiteral("Dual Pitch"),
    QStringLiteral("Rotary"),
    QStringLiteral("Ring Mod."),
    QStringLiteral("Mod. Filter"),
    QStringLiteral("Digital Distortion"),
    QStringLiteral("Dynamic Filter"),
    QStringLiteral("Dynamic Flange"),

    QStringLiteral("Dynamic Phaser"),
    QStringLiteral("Reverb + Chorus"),
    QStringLiteral("Reverb -> Chorus"),
    QStringLiteral("Reverb + Flange"),
    QStringLiteral("Reverb -> Flange"),
    QStringLiteral("Reverb + Symphonic"),
    QStringLiteral("Reverb -> Symphonic"),
    QStringLiteral("Reverb -> Pan"),

    QStringLiteral("Delay + Early Ref."),
    QStringLiteral("Delay -> Early Ref."),
    QStringLiteral("Delay + Reverb"),
    QStringLiteral("Delay -> Reverb"),
    QStringLiteral("Distortion -> Delay"),
    QStringLiteral("Multi Filter"),
    QStringLiteral("M. Band Dynamic Processor"),
    QStringLiteral("Distortion"),

    QStringLiteral("Vintage Flange"),
    QStringLiteral("Mono Vintage Phaser"),
    QStringLiteral("Stereo Vintage Phaser"),
    QStringLiteral("3 Band Parametric EQ"),
    QStringLiteral("Spring Reverb"),
    QStringLiteral("Tape Echo"),
    QStringLiteral("Compressor"),

    QStringLiteral("Amp Multi (Chorus)"),
    QStringLiteral("Amp Multi (Flange)"),
    QStringLiteral("Amp Multi (Tremolo)"),
    QStringLiteral("Amp Multi (Phaser)"),
    QStringLiteral("Distortion Multi (Chorus)"),
    QStringLiteral("Distortion Multi (Flange)"),
    QStringLiteral("Distortion Multi (Tremolo)"),
    QStringLiteral("Distortion Multi (Phaser)"),

    QStringLiteral("Bass Preamp")
};

const QStringList GuitarAmpTypeNameList =
{
    QStringLiteral("Heavy 1"),
    QStringLiteral("Heavy 2"),
    QStringLiteral("Lead 1"),
    QStringLiteral("Lead 2"),
    QStringLiteral("Drive 1"),
    QStringLiteral("Drive 2"),
    QStringLiteral("Crunch 1"),
    QStringLiteral("Crunch 2"),
    QStringLiteral("Clean 1"),
    QStringLiteral("Clean 2"),
    QStringLiteral("Solid")
};

const QStringList GuitarCabTypeNameList =
{
    QStringLiteral("Off"),
    QStringLiteral("American 4x12"),
    QStringLiteral("British 4x12"),
    QStringLiteral("Modern 4x12"),
    QStringLiteral("YAMAHA 4x12"),
    QStringLiteral("Hybrid 4x12"),
    QStringLiteral("American 2x12"),
    QStringLiteral("British 2x12"),
    QStringLiteral("Modern 2x12"),
    QStringLiteral("YAMAHA 2x12"),
    QStringLiteral("Hybrid 2x12"),
    QStringLiteral("American 1x12"),
    QStringLiteral("Modern 1x12"),
    QStringLiteral("YAMAHA 1x12"),
    QStringLiteral("Hybrid 1x12"),
    QStringLiteral("4x10"),
    QStringLiteral("2x10")
};

const QStringList BassPreampTypeNameList =
{
    QStringLiteral("Flat"),
    QStringLiteral("Tube"),
    QStringLiteral("Solid"),
    QStringLiteral("R&B"),
    QStringLiteral("Vintage"),
    QStringLiteral("Modern"),
    QStringLiteral("Classic"),
    QStringLiteral("Heavy"),
    QStringLiteral("Drive"),
    QStringLiteral("Dist"),
    QStringLiteral("Fuzz")
};

const QStringList BassPreampSpeakerSimNameList =
{
    QStringLiteral("Off"),
    QStringLiteral("R On"),
    QStringLiteral("LR On")
};

const QStringList OffOnStringList =
{
    QStringLiteral("Off"),
    QStringLiteral("On")
};

const QStringList MicTypeNameList =
{
    QStringLiteral("Condenser 1"),
    QStringLiteral("Condenser 2"),
    QStringLiteral("Dynamic 1"),
    QStringLiteral("Dynamic 2"),
    QStringLiteral("Tube 1"),
    QStringLiteral("Tube 2"),
    QStringLiteral("Nylon String 1"),
    QStringLiteral("Nylon String 2")
};

const QStringList AcousticReverbTypeNameList =
{
    QStringLiteral("Off"),
    QStringLiteral("Hall"),
    QStringLiteral("Room"),
    QStringLiteral("Plate")
};

const QStringList AcousticChorusDelayTypeNameList =
{
    QStringLiteral("Off"),
    QStringLiteral("Chorus"),
    QStringLiteral("Delay")
};

const QStringList DistortionTypeNameList =
{
    QStringLiteral("Lead 1"),
    QStringLiteral("Lead 2"),
    QStringLiteral("Drive 1"),
    QStringLiteral("Drive 2"),
    QStringLiteral("Crunch 1"),
    QStringLiteral("Crunch 2"),
    QStringLiteral("Fuzz 1"),
    QStringLiteral("Fuzz 2"),
    QStringLiteral("Distortion 1"),
    QStringLiteral("Distortion 2"),
    QStringLiteral("Overdrive 1"),
    QStringLiteral("Overdrive 2"),
    QStringLiteral("Tube"),
    QStringLiteral("Solidstate"),
    QStringLiteral("Bypass"),
};

const QStringList ReverbTypeNameList =
{
    QStringLiteral("Hall"),
    QStringLiteral("Room"),
    QStringLiteral("Stage"),
    QStringLiteral("Plate")
};

const QStringList GateReverbTypeNameList =
{
    QStringLiteral("Type-A"),
    QStringLiteral("Type-B")
};

const QStringList EarlyRefTypeNameList =
{
    QStringLiteral("Small Hall"),
    QStringLiteral("Large Hall"),
    QStringLiteral("Random"),
    QStringLiteral("Reverse"),
    QStringLiteral("Plate"),
    QStringLiteral("Spring")
};

#endif
