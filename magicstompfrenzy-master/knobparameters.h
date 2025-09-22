/****************************************************************************
**
** Copyright (C) 2019 Robert Vetter.
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

#ifndef KNOBPARAMETERS_H
#define KNOBPARAMETERS_H

#include <QMap>
#include <QString>

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

const QMap<int, QString> EightBandParaDlyKnobParameters =
{
    { 0, QStringLiteral("Band 1 Delay Time") },
    { 1, QStringLiteral("Band 2 Delay Time") },
    { 2, QStringLiteral("Band 3 Delay Time") },
    { 3, QStringLiteral("Band 4 Delay Time") },
    { 4, QStringLiteral("Band 5 Delay Time") },
    { 5, QStringLiteral("Band 6 Delay Time") },
    { 6, QStringLiteral("Band 7 Delay Time") },
    { 7, QStringLiteral("Band 8 Delay Time") },
    { 8, QStringLiteral("Effect Level") },
    { 9, QStringLiteral("Direct Level") },
    { 10, QStringLiteral("Direct Pan") },
    { 11, QStringLiteral("Wave Form") },

    { 19, QStringLiteral("Band 1 Low Cut Filter") },
    { 20, QStringLiteral("Band 1 High Cut Filter") },
    { 21, QStringLiteral("Band 1 Feedback") },
    { 22, QStringLiteral("Band 1 Wave") },
    { 23, QStringLiteral("Band 1 Phase") },
    { 24, QStringLiteral("Band 1 Tap") },
    { 25, QStringLiteral("Band 1 Speed") },
    { 26, QStringLiteral("Band 1 Depth") },
    { 27, QStringLiteral("Band 1 Pan") },
    { 28, QStringLiteral("Band 1 Level") },
    { 29, QStringLiteral("Band 1 Sync") },

    { 30, QStringLiteral("Band 2 Low Cut Filter") },
    { 31, QStringLiteral("Band 2 High Cut Filter") },
    { 32, QStringLiteral("Band 2 Feedback") },
    { 33, QStringLiteral("Band 2 Wave") },
    { 34, QStringLiteral("Band 2 Phase") },
    { 35, QStringLiteral("Band 2 Tap") },
    { 36, QStringLiteral("Band 2 Speed") },
    { 37, QStringLiteral("Band 2 Depth") },
    { 38, QStringLiteral("Band 2 Pan") },
    { 39, QStringLiteral("Band 2 Level") },
    { 40, QStringLiteral("Band 2 Sync") },

    { 41, QStringLiteral("Band 3 Low Cut Filter") },
    { 42, QStringLiteral("Band 3 High Cut Filter") },
    { 43, QStringLiteral("Band 3 Feedback") },
    { 44, QStringLiteral("Band 3 Wave") },
    { 45, QStringLiteral("Band 3 Phase") },
    { 46, QStringLiteral("Band 3 Tap") },
    { 47, QStringLiteral("Band 3 Speed") },
    { 48, QStringLiteral("Band 3 Depth") },
    { 49, QStringLiteral("Band 3 Pan") },
    { 50, QStringLiteral("Band 3 Level") },
    { 51, QStringLiteral("Band 3 Sync") },

    { 52, QStringLiteral("Band 4 Low Cut Filter") },
    { 53, QStringLiteral("Band 4 High Cut Filter") },
    { 54, QStringLiteral("Band 4 Feedback") },
    { 55, QStringLiteral("Band 4 Wave") },
    { 56, QStringLiteral("Band 4 Phase") },
    { 57, QStringLiteral("Band 4 Tap") },
    { 58, QStringLiteral("Band 4 Speed") },
    { 59, QStringLiteral("Band 4 Depth") },
    { 60, QStringLiteral("Band 4 Pan") },
    { 61, QStringLiteral("Band 4 Level") },
    { 62, QStringLiteral("Band 4 Sync") },

    { 63, QStringLiteral("Band 5 Low Cut Filter") },
    { 64, QStringLiteral("Band 5 High Cut Filter") },
    { 65, QStringLiteral("Band 5 Feedback") },
    { 66, QStringLiteral("Band 5 Wave") },
    { 67, QStringLiteral("Band 5 Phase") },
    { 68, QStringLiteral("Band 5 Tap") },
    { 69, QStringLiteral("Band 5 Speed") },
    { 70, QStringLiteral("Band 5 Depth") },
    { 71, QStringLiteral("Band 5 Pan") },
    { 72, QStringLiteral("Band 5 Level") },
    { 73, QStringLiteral("Band 5 Sync") },

    { 74, QStringLiteral("Band 6 Low Cut Filter") },
    { 75, QStringLiteral("Band 6 High Cut Filter") },
    { 76, QStringLiteral("Band 6 Feedback") },
    { 77, QStringLiteral("Band 6 Wave") },
    { 78, QStringLiteral("Band 6 Phase") },
    { 79, QStringLiteral("Band 6 Tap") },
    { 80, QStringLiteral("Band 6 Speed") },
    { 81, QStringLiteral("Band 6 Depth") },
    { 82, QStringLiteral("Band 6 Pan") },
    { 83, QStringLiteral("Band 6 Level") },
    { 84, QStringLiteral("Band 6 Sync") },

    { 85, QStringLiteral("Band 7 Low Cut Filter") },
    { 86, QStringLiteral("Band 7 High Cut Filter") },
    { 87, QStringLiteral("Band 7 Feedback") },
    { 88, QStringLiteral("Band 7 Wave") },
    { 89, QStringLiteral("Band 7 Phase") },
    { 90, QStringLiteral("Band 7 Tap") },
    { 91, QStringLiteral("Band 7 Speed") },
    { 92, QStringLiteral("Band 7 Depth") },
    { 93, QStringLiteral("Band 7 Pan") },
    { 94, QStringLiteral("Band 7 Level") },
    { 95, QStringLiteral("Band 7 Sync") },

    { 96, QStringLiteral("Band 8 Low Cut Filter") },
    { 97, QStringLiteral("Band 8 High Cut Filter") },
    { 98, QStringLiteral("Band 8 Feedback") },
    { 99, QStringLiteral("Band 8 Wave") },
    {100, QStringLiteral("Band 8 Phase") },
    {101, QStringLiteral("Band 8 Tap") },
    {102, QStringLiteral("Band 8 Speed") },
    {103, QStringLiteral("Band 8 Depth") },
    {104, QStringLiteral("Band 8 Pan") },
    {105, QStringLiteral("Band 8 Level") },
    {106, QStringLiteral("Band 8 Sync") }
};

const QMap<int, QString> FourBand2TapModDlyKnobParameters =
{
    { 0, QStringLiteral("Band 1 Delay Time") },
    { 2, QStringLiteral("Band 2 Delay Time") },
    { 4, QStringLiteral("Band 3 Delay Time") },
    { 6, QStringLiteral("Band 4 Delay Time") },
    { 8, QStringLiteral("Effect Level") },
    { 9, QStringLiteral("Direct Level") },
    { 10, QStringLiteral("Direct Pan") },
    { 11, QStringLiteral("Wave Form") },

    { 19, QStringLiteral("Band 1 Tap 1 Low Cut Filter") },
    { 20, QStringLiteral("Band 1 Tap 1 High Cut Filter") },
    { 21, QStringLiteral("Band 1 Tap 1 Feedback") },
    { 22, QStringLiteral("Band 1 Tap 1 Wave") },
    { 23, QStringLiteral("Band 1 Tap 1 Phase") },
    { 24, QStringLiteral("Band 1 Tap 1 Tap") },
    { 25, QStringLiteral("Band 1 Tap 1 Speed") },
    { 26, QStringLiteral("Band 1 Tap 1 Depth") },
    { 27, QStringLiteral("Band 1 Tap 1 Pan") },
    { 28, QStringLiteral("Band 1 Tap 1 Level") },
    { 29, QStringLiteral("Band 1 Tap 1 Sync") },

    { 33, QStringLiteral("Band 1 Tap 2 Wave") },
    { 34, QStringLiteral("Band 1 Tap 2 Phase") },
    { 35, QStringLiteral("Band 1 Tap 2 Tap") },
    { 36, QStringLiteral("Band 1 Tap 2 Speed") },
    { 37, QStringLiteral("Band 1 Tap 2 Depth") },
    { 38, QStringLiteral("Band 1 Tap 2 Pan") },
    { 39, QStringLiteral("Band 1 Tap 2 Level") },
    { 40, QStringLiteral("Band 1 Tap 2 Sync") },

    { 41, QStringLiteral("Band 2 Tap 1 Low Cut Filter") },
    { 42, QStringLiteral("Band 2 Tap 1 High Cut Filter") },
    { 43, QStringLiteral("Band 2 Tap 1 Feedback") },
    { 44, QStringLiteral("Band 2 Tap 1 Wave") },
    { 45, QStringLiteral("Band 2 Tap 1 Phase") },
    { 46, QStringLiteral("Band 2 Tap 1 Tap") },
    { 47, QStringLiteral("Band 2 Tap 1 Speed") },
    { 48, QStringLiteral("Band 2 Tap 1 Depth") },
    { 49, QStringLiteral("Band 2 Tap 1 Pan") },
    { 50, QStringLiteral("Band 2 Tap 1 Level") },
    { 51, QStringLiteral("Band 2 Tap 1 Sync") },

    { 55, QStringLiteral("Band 2 Tap 2 Wave") },
    { 56, QStringLiteral("Band 2 Tap 2 Phase") },
    { 57, QStringLiteral("Band 2 Tap 2 Tap") },
    { 58, QStringLiteral("Band 2 Tap 2 Speed") },
    { 59, QStringLiteral("Band 2 Tap 2 Depth") },
    { 60, QStringLiteral("Band 2 Tap 2 Pan") },
    { 61, QStringLiteral("Band 2 Tap 2 Level") },
    { 62, QStringLiteral("Band 2 Tap 2 Sync") },

    { 63, QStringLiteral("Band 3 Tap 1 Low Cut Filter") },
    { 64, QStringLiteral("Band 3 Tap 1 High Cut Filter") },
    { 65, QStringLiteral("Band 3 Tap 1 Feedback") },
    { 66, QStringLiteral("Band 3 Tap 1 Wave") },
    { 67, QStringLiteral("Band 3 Tap 1 Phase") },
    { 68, QStringLiteral("Band 3 Tap 1 Tap") },
    { 69, QStringLiteral("Band 3 Tap 1 Speed") },
    { 70, QStringLiteral("Band 3 Tap 1 Depth") },
    { 71, QStringLiteral("Band 3 Tap 1 Pan") },
    { 72, QStringLiteral("Band 3 Tap 1 Level") },
    { 73, QStringLiteral("Band 3 Tap 1 Sync") },

    { 77, QStringLiteral("Band 3 Tap 2 Wave") },
    { 78, QStringLiteral("Band 3 Tap 2 Phase") },
    { 79, QStringLiteral("Band 3 Tap 2 Tap") },
    { 80, QStringLiteral("Band 3 Tap 2 Speed") },
    { 81, QStringLiteral("Band 3 Tap 2 Depth") },
    { 82, QStringLiteral("Band 3 Tap 2 Pan") },
    { 83, QStringLiteral("Band 3 Tap 2 Level") },
    { 84, QStringLiteral("Band 3 Tap 2 Sync") },

    { 85, QStringLiteral("Band 4 Tap 1 Low Cut Filter") },
    { 86, QStringLiteral("Band 4 Tap 1 High Cut Filter") },
    { 87, QStringLiteral("Band 4 Tap 1 Feedback") },
    { 88, QStringLiteral("Band 4 Tap 1 Wave") },
    { 89, QStringLiteral("Band 4 Tap 1 Phase") },
    { 90, QStringLiteral("Band 4 Tap 1 Tap") },
    { 91, QStringLiteral("Band 4 Tap 1 Speed") },
    { 92, QStringLiteral("Band 4 Tap 1 Depth") },
    { 93, QStringLiteral("Band 4 Tap 1 Pan") },
    { 94, QStringLiteral("Band 4 Tap 1 Level") },
    { 95, QStringLiteral("Band 4 Tap 1 Sync") },

    { 99, QStringLiteral("Band 4 Tap 2 Wave") },
    {100, QStringLiteral("Band 4 Tap 2 Phase") },
    {101, QStringLiteral("Band 4 Tap 2 Tap") },
    {102, QStringLiteral("Band 4 Tap 2 Speed") },
    {103, QStringLiteral("Band 4 Tap 2 Depth") },
    {104, QStringLiteral("Band 4 Tap 2 Pan") },
    {105, QStringLiteral("Band 4 Tap 2 Level") },
    {106, QStringLiteral("Band 4 Tap 2 Sync") }
};

const QMap<int, QString> TwoBand4TapModDlyKnobParameters =
{
    { 0, QStringLiteral("Band 1 Delay Time") },
    { 4, QStringLiteral("Band 2 Delay Time") },
    { 8, QStringLiteral("Effect Level") },
    { 9, QStringLiteral("Direct Level") },
    { 10, QStringLiteral("Direct Pan") },
    { 11, QStringLiteral("Wave Form") },

    { 19, QStringLiteral("Band 1 Tap 1 Low Cut Filter") },
    { 20, QStringLiteral("Band 1 Tap 1 High Cut Filter") },
    { 21, QStringLiteral("Band 1 Tap 1 Feedback") },
    { 22, QStringLiteral("Band 1 Tap 1 Wave") },
    { 23, QStringLiteral("Band 1 Tap 1 Phase") },
    { 24, QStringLiteral("Band 1 Tap 1 Tap") },
    { 25, QStringLiteral("Band 1 Tap 1 Speed") },
    { 26, QStringLiteral("Band 1 Tap 1 Depth") },
    { 27, QStringLiteral("Band 1 Tap 1 Pan") },
    { 28, QStringLiteral("Band 1 Tap 1 Level") },
    { 29, QStringLiteral("Band 1 Tap 1 Sync") },

    { 33, QStringLiteral("Band 1 Tap 2 Wave") },
    { 34, QStringLiteral("Band 1 Tap 2 Phase") },
    { 35, QStringLiteral("Band 1 Tap 2 Tap") },
    { 36, QStringLiteral("Band 1 Tap 2 Speed") },
    { 37, QStringLiteral("Band 1 Tap 2 Depth") },
    { 38, QStringLiteral("Band 1 Tap 2 Pan") },
    { 39, QStringLiteral("Band 1 Tap 2 Level") },
    { 40, QStringLiteral("Band 1 Tap 2 Sync") },

    { 44, QStringLiteral("Band 1 Tap 3 Wave") },
    { 45, QStringLiteral("Band 1 Tap 3 Phase") },
    { 46, QStringLiteral("Band 1 Tap 3 Tap") },
    { 47, QStringLiteral("Band 1 Tap 3 Speed") },
    { 48, QStringLiteral("Band 1 Tap 3 Depth") },
    { 49, QStringLiteral("Band 1 Tap 3 Pan") },
    { 50, QStringLiteral("Band 1 Tap 3 Level") },
    { 51, QStringLiteral("Band 1 Tap 3 Sync") },

    { 55, QStringLiteral("Band 1 Tap 4 Wave") },
    { 56, QStringLiteral("Band 1 Tap 4 Phase") },
    { 57, QStringLiteral("Band 1 Tap 4 Tap") },
    { 58, QStringLiteral("Band 1 Tap 4 Speed") },
    { 59, QStringLiteral("Band 1 Tap 4 Depth") },
    { 60, QStringLiteral("Band 1 Tap 4 Pan") },
    { 61, QStringLiteral("Band 1 Tap 4 Level") },
    { 62, QStringLiteral("Band 1 Tap 4 Sync") },

    { 63, QStringLiteral("Band 2 Tap 1 Low Cut Filter") },
    { 64, QStringLiteral("Band 2 Tap 1 High Cut Filter") },
    { 65, QStringLiteral("Band 2 Tap 1 Feedback") },
    { 66, QStringLiteral("Band 2 Tap 1 Wave") },
    { 67, QStringLiteral("Band 2 Tap 1 Phase") },
    { 68, QStringLiteral("Band 2 Tap 1 Tap") },
    { 69, QStringLiteral("Band 2 Tap 1 Speed") },
    { 70, QStringLiteral("Band 2 Tap 1 Depth") },
    { 71, QStringLiteral("Band 2 Tap 1 Pan") },
    { 72, QStringLiteral("Band 2 Tap 1 Level") },
    { 73, QStringLiteral("Band 2 Tap 1 Sync") },

    { 77, QStringLiteral("Band 2 Tap 2 Wave") },
    { 78, QStringLiteral("Band 2 Tap 2 Phase") },
    { 79, QStringLiteral("Band 2 Tap 2 Tap") },
    { 80, QStringLiteral("Band 2 Tap 2 Speed") },
    { 81, QStringLiteral("Band 2 Tap 2 Depth") },
    { 82, QStringLiteral("Band 2 Tap 2 Pan") },
    { 83, QStringLiteral("Band 2 Tap 2 Level") },
    { 84, QStringLiteral("Band 2 Tap 2 Sync") },

    { 88, QStringLiteral("Band 2 Tap 3 Wave") },
    { 89, QStringLiteral("Band 2 Tap 3 Phase") },
    { 90, QStringLiteral("Band 2 Tap 3 Tap") },
    { 91, QStringLiteral("Band 2 Tap 3 Speed") },
    { 92, QStringLiteral("Band 2 Tap 3 Depth") },
    { 93, QStringLiteral("Band 2 Tap 3 Pan") },
    { 94, QStringLiteral("Band 2 Tap 3 Level") },
    { 95, QStringLiteral("Band 2 Tap 3 Sync") },

    { 99, QStringLiteral("Band 2 Tap 4 Wave") },
    {100, QStringLiteral("Band 2 Tap 4 Phase") },
    {101, QStringLiteral("Band 2 Tap 4 Tap") },
    {102, QStringLiteral("Band 2 Tap 4 Speed") },
    {103, QStringLiteral("Band 2 Tap 4 Depth") },
    {104, QStringLiteral("Band 2 Tap 4 Pan") },
    {105, QStringLiteral("Band 2 Tap 4 Level") },
    {106, QStringLiteral("Band 2 Tap 4 Sync") }
};

const QMap<int, QString> OneBand8TapModDlyKnobParameters =
{
    { 0, QStringLiteral("Band 1 Delay Time") },
    { 8, QStringLiteral("Effect Level") },
    { 9, QStringLiteral("Direct Level") },
    { 10, QStringLiteral("Direct Pan") },
    { 11, QStringLiteral("Wave Form") },

    { 19, QStringLiteral("Tap 1 Low Cut Filter") },
    { 20, QStringLiteral("Tap 1 High Cut Filter") },
    { 21, QStringLiteral("Tap 1 Feedback") },
    { 22, QStringLiteral("Tap 1 Wave") },
    { 23, QStringLiteral("Tap 1 Phase") },
    { 24, QStringLiteral("Tap 1 Tap") },
    { 25, QStringLiteral("Tap 1 Speed") },
    { 26, QStringLiteral("Tap 1 Depth") },
    { 27, QStringLiteral("Tap 1 Pan") },
    { 28, QStringLiteral("Tap 1 Level") },
    { 29, QStringLiteral("Tap 1 Sync") },

    { 33, QStringLiteral("Tap 2 Wave") },
    { 34, QStringLiteral("Tap 2 Phase") },
    { 35, QStringLiteral("Tap 2 Tap") },
    { 36, QStringLiteral("Tap 2 Speed") },
    { 37, QStringLiteral("Tap 2 Depth") },
    { 38, QStringLiteral("Tap 2 Pan") },
    { 39, QStringLiteral("Tap 2 Level") },
    { 40, QStringLiteral("Tap 2 Sync") },

    { 44, QStringLiteral("Tap 3 Wave") },
    { 45, QStringLiteral("Tap 3 Phase") },
    { 46, QStringLiteral("Tap 3 Tap") },
    { 47, QStringLiteral("Tap 3 Speed") },
    { 48, QStringLiteral("Tap 3 Depth") },
    { 49, QStringLiteral("Tap 3 Pan") },
    { 50, QStringLiteral("Tap 3 Level") },
    { 51, QStringLiteral("Tap 3 Sync") },

    { 55, QStringLiteral("Tap 4 Wave") },
    { 56, QStringLiteral("Tap 4 Phase") },
    { 57, QStringLiteral("Tap 4 Tap") },
    { 58, QStringLiteral("Tap 4 Speed") },
    { 59, QStringLiteral("Tap 4 Depth") },
    { 60, QStringLiteral("Tap 4 Pan") },
    { 61, QStringLiteral("Tap 4 Level") },
    { 62, QStringLiteral("Tap 4 Sync") },

    { 66, QStringLiteral("Tap 5 Wave") },
    { 67, QStringLiteral("Tap 5 Phase") },
    { 68, QStringLiteral("Tap 5 Tap") },
    { 69, QStringLiteral("Tap 5 Speed") },
    { 70, QStringLiteral("Tap 5 Depth") },
    { 71, QStringLiteral("Tap 5 Pan") },
    { 72, QStringLiteral("Tap 5 Level") },
    { 73, QStringLiteral("Tap 5 Sync") },

    { 77, QStringLiteral("Tap 6 Wave") },
    { 78, QStringLiteral("Tap 6 Phase") },
    { 79, QStringLiteral("Tap 6 Tap") },
    { 80, QStringLiteral("Tap 6 Speed") },
    { 81, QStringLiteral("Tap 6 Depth") },
    { 82, QStringLiteral("Tap 6 Pan") },
    { 83, QStringLiteral("Tap 6 Level") },
    { 84, QStringLiteral("Tap 6 Sync") },

    { 88, QStringLiteral("Tap 7 Wave") },
    { 89, QStringLiteral("Tap 7 Phase") },
    { 90, QStringLiteral("Tap 7 Tap") },
    { 91, QStringLiteral("Tap 7 Speed") },
    { 92, QStringLiteral("Tap 7 Depth") },
    { 93, QStringLiteral("Tap 7 Pan") },
    { 94, QStringLiteral("Tap 7 Level") },
    { 95, QStringLiteral("Tap 7 Sync") },

    { 99, QStringLiteral("Tap 8 Wave") },
    {100, QStringLiteral("Tap 8 Phase") },
    {101, QStringLiteral("Tap 8 Tap") },
    {102, QStringLiteral("Tap 8 Speed") },
    {103, QStringLiteral("Tap 8 Depth") },
    {104, QStringLiteral("Tap 8 Pan") },
    {105, QStringLiteral("Tap 8 Level") },
    {106, QStringLiteral("Tap 8 Sync") }
};

const QMap<int, QString> TwoBandLong4ShortModDlyKnobParameters =
{
    { 0, QStringLiteral("Long Band 1 Delay Time") },
    { 2, QStringLiteral("Long Band 2 Delay Time") },
    { 4, QStringLiteral("Short Band 1 Delay Time") },
    { 5, QStringLiteral("Short Band 2 Delay Time") },
    { 6, QStringLiteral("Short Band 3 Delay Time") },
    { 7, QStringLiteral("Short Band 4 Short Delay Time") },
    { 8, QStringLiteral("Effect Level") },
    { 9, QStringLiteral("Direct Level") },
    { 10, QStringLiteral("Direct Pan") },
    { 11, QStringLiteral("Wave Form") },

    { 19, QStringLiteral("Long Band 1 Tap 1 Low Cut Filter") },
    { 20, QStringLiteral("Long Band 1 Tap 1 High Cut Filter") },
    { 21, QStringLiteral("Long Band 1 Tap 1 Feedback") },
    { 22, QStringLiteral("Long Band 1 Tap 1 Wave") },
    { 23, QStringLiteral("Long Band 1 Tap 1 Phase") },
    { 24, QStringLiteral("Long Band 1 Tap 1 Tap") },
    { 25, QStringLiteral("Long Band 1 Tap 1 Speed") },
    { 26, QStringLiteral("Long Band 1 Tap 1 Depth") },
    { 27, QStringLiteral("Long Band 1 Tap 1 Pan") },
    { 28, QStringLiteral("Long Band 1 Tap 1 Level") },
    { 29, QStringLiteral("Long Band 1 Tap 1 Sync") },

    { 33, QStringLiteral("Long Band 1 Tap 2 Wave") },
    { 34, QStringLiteral("Long Band 1 Tap 2 Phase") },
    { 35, QStringLiteral("Long Band 1 Tap 2 Tap") },
    { 36, QStringLiteral("Long Band 1 Tap 2 Speed") },
    { 37, QStringLiteral("Long Band 1 Tap 2 Depth") },
    { 38, QStringLiteral("Long Band 1 Tap 2 Pan") },
    { 39, QStringLiteral("Long Band 1 Tap 2 Level") },
    { 40, QStringLiteral("Long Band 1 Tap 2 Sync") },

    { 41, QStringLiteral("Long Band 2 Tap 1 Low Cut Filter") },
    { 42, QStringLiteral("Long Band 2 Tap 1 High Cut Filter") },
    { 43, QStringLiteral("Long Band 2 Tap 1 Feedback") },
    { 44, QStringLiteral("Long Band 2 Tap 1 Wave") },
    { 45, QStringLiteral("Long Band 2 Tap 1 Phase") },
    { 46, QStringLiteral("Long Band 2 Tap 1 Tap") },
    { 47, QStringLiteral("Long Band 2 Tap 1 Speed") },
    { 48, QStringLiteral("Long Band 2 Tap 1 Depth") },
    { 49, QStringLiteral("Long Band 2 Tap 1 Pan") },
    { 50, QStringLiteral("Long Band 2 Tap 1 Level") },
    { 51, QStringLiteral("Long Band 2 Tap 1 Sync") },

    { 55, QStringLiteral("Long Band 2 Tap 2 Wave") },
    { 56, QStringLiteral("Long Band 2 Tap 2 Phase") },
    { 57, QStringLiteral("Long Band 2 Tap 2 Tap") },
    { 58, QStringLiteral("Long Band 2 Tap 2 Speed") },
    { 59, QStringLiteral("Long Band 2 Tap 2 Depth") },
    { 60, QStringLiteral("Long Band 2 Tap 2 Pan") },
    { 61, QStringLiteral("Long Band 2 Tap 2 Level") },
    { 62, QStringLiteral("Long Band 2 Tap 2 Sync") },

    { 63, QStringLiteral("Short Band 1 Low Cut Filter") },
    { 64, QStringLiteral("Short Band 1 High Cut Filter") },
    { 65, QStringLiteral("Short Band 1 Feedback") },
    { 66, QStringLiteral("Short Band 1 Wave") },
    { 67, QStringLiteral("Short Band 1 Phase") },
    { 68, QStringLiteral("Short Band 1 Tap") },
    { 69, QStringLiteral("Short Band 1 Speed") },
    { 70, QStringLiteral("Short Band 1 Depth") },
    { 71, QStringLiteral("Short Band 1 Pan") },
    { 72, QStringLiteral("Short Band 1 Level") },
    { 73, QStringLiteral("Short Band 1 Sync") },

    { 74, QStringLiteral("Short Band 2 Low Cut Filter") },
    { 75, QStringLiteral("Short Band 2 High Cut Filter") },
    { 76, QStringLiteral("Short Band 2 Feedback") },
    { 77, QStringLiteral("Short Band 2 Wave") },
    { 78, QStringLiteral("Short Band 2 Phase") },
    { 79, QStringLiteral("Short Band 2 Tap") },
    { 80, QStringLiteral("Short Band 2 Speed") },
    { 81, QStringLiteral("Short Band 2 Depth") },
    { 82, QStringLiteral("Short Band 2 Pan") },
    { 83, QStringLiteral("Short Band 2 Level") },
    { 84, QStringLiteral("Short Band 2 Sync") },

    { 85, QStringLiteral("Short Band 3 Low Cut Filter") },
    { 86, QStringLiteral("Short Band 3 High Cut Filter") },
    { 87, QStringLiteral("Short Band 3 Feedback") },
    { 88, QStringLiteral("Short Band 3 Wave") },
    { 89, QStringLiteral("Short Band 3 Phase") },
    { 90, QStringLiteral("Short Band 3 Tap") },
    { 91, QStringLiteral("Short Band 3 Speed") },
    { 92, QStringLiteral("Short Band 3 Depth") },
    { 93, QStringLiteral("Short Band 3 Pan") },
    { 94, QStringLiteral("Short Band 3 Level") },
    { 95, QStringLiteral("Short Band 3 Sync") },

    { 96, QStringLiteral("Short Band 4 Low Cut Filter") },
    { 97, QStringLiteral("Short Band 4 High Cut Filter") },
    { 98, QStringLiteral("Short Band 4 Feedback") },
    { 99, QStringLiteral("Short Band 4 Wave") },
    {100, QStringLiteral("Short Band 4 Phase") },
    {101, QStringLiteral("Short Band 4 Tap") },
    {102, QStringLiteral("Short Band 4 Speed") },
    {103, QStringLiteral("Short Band 4 Depth") },
    {104, QStringLiteral("Short Band 4 Pan") },
    {105, QStringLiteral("Short Band 4 Level") },
    {106, QStringLiteral("Short Band 4 Sync") }
};

const QMap<int, QString> ShortMediumLongModDlyKnobParameters =
{
    { 0, QStringLiteral("Short Band Delay Time") },
    { 1, QStringLiteral("Medium Band Delay Time") },
    { 4, QStringLiteral("Long Band Delay Time") },
    { 8, QStringLiteral("Effect Level") },
    { 9, QStringLiteral("Direct Level") },
    { 10, QStringLiteral("Direct Pan") },
    { 11, QStringLiteral("Wave Form") },

    { 19, QStringLiteral("Short Band Low Cut Filter") },
    { 20, QStringLiteral("Short Band High Cut Filter") },
    { 21, QStringLiteral("Short Band Feedback") },
    { 22, QStringLiteral("Short Band Wave") },
    { 23, QStringLiteral("Short Band Phase") },
    { 24, QStringLiteral("Short Band Tap") },
    { 25, QStringLiteral("Short Band Speed") },
    { 26, QStringLiteral("Short Band Depth") },
    { 27, QStringLiteral("Short Band Pan") },
    { 28, QStringLiteral("Short Band Level") },
    { 29, QStringLiteral("Short Band Sync") },

    { 30, QStringLiteral("Medium Band Low Cut Filter") },
    { 31, QStringLiteral("Medium Band High Cut Filter") },
    { 32, QStringLiteral("Medium Band Feedback") },
    { 33, QStringLiteral("Medium Band Tap 1 Wave") },
    { 34, QStringLiteral("Medium Band Tap 1 Phase") },
    { 35, QStringLiteral("Medium Band Tap 1 Tap") },
    { 36, QStringLiteral("Medium Band Tap 1 Speed") },
    { 37, QStringLiteral("Medium Band Tap 1 Depth") },
    { 38, QStringLiteral("Medium Band Tap 1 Pan") },
    { 39, QStringLiteral("Medium Band Tap 1 Level") },
    { 40, QStringLiteral("Medium Band Tap 1 Sync") },

    { 44, QStringLiteral("Medium Band Tap 2 Wave") },
    { 45, QStringLiteral("Medium Band Tap 2 Phase") },
    { 46, QStringLiteral("Medium Band Tap 2 Tap") },
    { 47, QStringLiteral("Medium Band Tap 2 Speed") },
    { 48, QStringLiteral("Medium Band Tap 2 Depth") },
    { 49, QStringLiteral("Medium Band Tap 2 Pan") },
    { 50, QStringLiteral("Medium Band Tap 2 Level") },
    { 51, QStringLiteral("Medium Band Tap 2 Sync") },

    { 55, QStringLiteral("Medium Band Tap 3 Wave") },
    { 56, QStringLiteral("Medium Band Tap 3 Phase") },
    { 57, QStringLiteral("Medium Band Tap 3 Tap") },
    { 58, QStringLiteral("Medium Band Tap 3 Speed") },
    { 59, QStringLiteral("Medium Band Tap 3 Depth") },
    { 60, QStringLiteral("Medium Band Tap 3 Pan") },
    { 61, QStringLiteral("Medium Band Tap 3 Level") },
    { 62, QStringLiteral("Medium Band Tap 3 Sync") },

    { 63, QStringLiteral("Long Band Low Cut Filter") },
    { 64, QStringLiteral("Long Band High Cut Filter") },
    { 65, QStringLiteral("Long Band Feedback") },
    { 66, QStringLiteral("Long Band Tap 1 Wave") },
    { 67, QStringLiteral("Long Band Tap 1 Phase") },
    { 68, QStringLiteral("Long Band Tap 1 Tap") },
    { 69, QStringLiteral("Long Band Tap 1 Speed") },
    { 70, QStringLiteral("Long Band Tap 1 Depth") },
    { 71, QStringLiteral("Long Band Tap 1 Pan") },
    { 72, QStringLiteral("Long Band Tap 1 Level") },
    { 73, QStringLiteral("Long Band Tap 1 Sync") },

    { 77, QStringLiteral("Long Band Tap 2 Wave") },
    { 78, QStringLiteral("Long Band Tap 2 Phase") },
    { 79, QStringLiteral("Long Band Tap 2 Tap") },
    { 80, QStringLiteral("Long Band Tap 2 Speed") },
    { 81, QStringLiteral("Long Band Tap 2 Depth") },
    { 82, QStringLiteral("Long Band Tap 2 Pan") },
    { 83, QStringLiteral("Long Band Tap 2 Level") },
    { 84, QStringLiteral("Long Band Tap 2 Sync") },

    { 88, QStringLiteral("Long Band Tap 3 Wave") },
    { 89, QStringLiteral("Long Band Tap 3 Phase") },
    { 90, QStringLiteral("Long Band Tap 3Tap") },
    { 91, QStringLiteral("Long Band Tap 3 Speed") },
    { 92, QStringLiteral("Long Band Tap 3 Depth") },
    { 93, QStringLiteral("Long Band Tap 3 Pan") },
    { 94, QStringLiteral("Long Band Tap 3 Level") },
    { 95, QStringLiteral("Long Band Tap 3 Sync") },

    { 99, QStringLiteral("Long Band Tap 4 Wave") },
    {100, QStringLiteral("Long Band Tap 4 Phase") },
    {101, QStringLiteral("Long Band Tap 4 Tap") },
    {102, QStringLiteral("Long Band Tap 4 Speed") },
    {103, QStringLiteral("Long Band Tap 4 Depth") },
    {104, QStringLiteral("Long Band Tap 4 Pan") },
    {105, QStringLiteral("Long Band Tap 4 Level") },
    {106, QStringLiteral("Long Band Tap 4 Sync") }
};

const QMap<int, QString> AmpSimulatorKnobParameters =
{
    { 11, QStringLiteral("Amp Type") },
    { 12, QStringLiteral("Speaker Simulator") },
    { 19, QStringLiteral("Gain") },
    { 20, QStringLiteral("Master") },
    { 23, QStringLiteral("Tone") },
    { 25, QStringLiteral("Treble") },
    { 26, QStringLiteral("High Middle") },
    { 27, QStringLiteral("Low Middle") },
    { 28, QStringLiteral("Bass") },
    { 29, QStringLiteral("Presence") },
    { 31, QStringLiteral("Noise Gate Threshold") },
    { 32, QStringLiteral("Noise Gate Attack") },
    { 33, QStringLiteral("Noise Gate Hold") },
    { 34, QStringLiteral("Noise Gate Decay") }
};

const QMap<int, QString> AmpMultiChorusKnobParameters =
{
    {  2, QStringLiteral("Compressor Threshold") },
    {  3, QStringLiteral("Chorus Delay") },
    {  4, QStringLiteral("Delay Feedback") },
    {  5, QStringLiteral("Reverb Ini. Delay") },
    { 11, QStringLiteral("Amp Type") },
    { 12, QStringLiteral("Speaker Simulator") },
    { 14, QStringLiteral("Chorus Wave") },
    { 19, QStringLiteral("Gain") },
    { 20, QStringLiteral("Master") },
    { 23, QStringLiteral("Tone") },
    { 25, QStringLiteral("Treble") },
    { 26, QStringLiteral("High Middle") },
    { 27, QStringLiteral("Low Middle") },
    { 28, QStringLiteral("Bass") },
    { 29, QStringLiteral("Presence") },
    { 31, QStringLiteral("Noise Gate Threshold") },
    { 32, QStringLiteral("Noise Gate Attack") },
    { 33, QStringLiteral("Noise Gate Hold") },
    { 34, QStringLiteral("Noise Gate Decay") },
    { 41, QStringLiteral("Compressor Ratio") },
    { 42, QStringLiteral("Compressor Attack") },
    { 43, QStringLiteral("Compressor Release") },
    { 44, QStringLiteral("Compressor Knee") },
    { 45, QStringLiteral("Compressor Gain") },
    { 52, QStringLiteral("Chorus Speed") },
    { 53, QStringLiteral("Chorus Depth") },
    { 54, QStringLiteral("Chorus Level") },
    { 63, QStringLiteral("Delay Tap Left") },
    { 64, QStringLiteral("Delay Tap Right") },
    { 65, QStringLiteral("Delay Feedback Gain") },
    { 66, QStringLiteral("Delay High") },
    { 67, QStringLiteral("Delay Level") },
    { 71, QStringLiteral("High Pass Filter") },
    { 72, QStringLiteral("Low Pass Filter") },
    { 74, QStringLiteral("Reverb Time") },
    { 75, QStringLiteral("Reverb High") },
    { 76, QStringLiteral("Reverb Diffusion") },
    { 77, QStringLiteral("Reverb Density") },
    { 78, QStringLiteral("Reverb Level") },
};

const QMap<int, QString> AmpMultiFlangeKnobParameters =
{
    {  2, QStringLiteral("Compressor Threshold") },
    {  3, QStringLiteral("Flanger Delay") },
    {  4, QStringLiteral("Delay Feedback") },
    {  5, QStringLiteral("Reverb Ini. Delay") },
    { 11, QStringLiteral("Amp Type") },
    { 12, QStringLiteral("Speaker Simulator") },
    { 14, QStringLiteral("Flanger Wave") },
    { 19, QStringLiteral("Gain") },
    { 20, QStringLiteral("Master") },
    { 23, QStringLiteral("Tone") },
    { 25, QStringLiteral("Treble") },
    { 26, QStringLiteral("High Middle") },
    { 27, QStringLiteral("Low Middle") },
    { 28, QStringLiteral("Bass") },
    { 29, QStringLiteral("Presence") },
    { 31, QStringLiteral("Noise Gate Threshold") },
    { 32, QStringLiteral("Noise Gate Attack") },
    { 33, QStringLiteral("Noise Gate Hold") },
    { 34, QStringLiteral("Noise Gate Decay") },
    { 41, QStringLiteral("Compressor Ratio") },
    { 42, QStringLiteral("Compressor Attack") },
    { 43, QStringLiteral("Compressor Release") },
    { 44, QStringLiteral("Compressor Knee") },
    { 45, QStringLiteral("Compressor Gain") },
    { 52, QStringLiteral("Flanger Speed") },
    { 53, QStringLiteral("Flanger Depth") },
    { 54, QStringLiteral("Flanger Feedback") },
    { 55, QStringLiteral("Flanger Level") },
    { 63, QStringLiteral("Delay Tap Left") },
    { 64, QStringLiteral("Delay Tap Right") },
    { 65, QStringLiteral("Delay Feedback Gain") },
    { 66, QStringLiteral("Delay High") },
    { 67, QStringLiteral("Delay Level") },
    { 71, QStringLiteral("High Pass Filter") },
    { 72, QStringLiteral("Low Pass Filter") },
    { 74, QStringLiteral("Reverb Time") },
    { 75, QStringLiteral("Reverb High") },
    { 76, QStringLiteral("Reverb Diffusion") },
    { 77, QStringLiteral("Reverb Density") },
    { 78, QStringLiteral("Reverb Level") },
};

const QMap<int, QString> AmpMultiTremoloKnobParameters =
{
    {  2, QStringLiteral("Compressor Threshold") },
    {  4, QStringLiteral("Delay Feedback") },
    {  5, QStringLiteral("Reverb Ini. Delay") },
    { 11, QStringLiteral("Amp Type") },
    { 12, QStringLiteral("Speaker Simulator") },
    { 14, QStringLiteral("Tremolo Wave") },
    { 19, QStringLiteral("Gain") },
    { 20, QStringLiteral("Master") },
    { 23, QStringLiteral("Tone") },
    { 25, QStringLiteral("Treble") },
    { 26, QStringLiteral("High Middle") },
    { 27, QStringLiteral("Low Middle") },
    { 28, QStringLiteral("Bass") },
    { 29, QStringLiteral("Presence") },
    { 31, QStringLiteral("Noise Gate Threshold") },
    { 32, QStringLiteral("Noise Gate Attack") },
    { 33, QStringLiteral("Noise Gate Hold") },
    { 34, QStringLiteral("Noise Gate Decay") },
    { 41, QStringLiteral("Compressor Ratio") },
    { 42, QStringLiteral("Compressor Attack") },
    { 43, QStringLiteral("Compressor Release") },
    { 44, QStringLiteral("Compressor Knee") },
    { 45, QStringLiteral("Compressor Gain") },
    { 52, QStringLiteral("Tremolo Speed") },
    { 53, QStringLiteral("Tremolo Depth") },
    { 63, QStringLiteral("Delay Tap Left") },
    { 64, QStringLiteral("Delay Tap Right") },
    { 65, QStringLiteral("Delay Feedback Gain") },
    { 66, QStringLiteral("Delay High") },
    { 67, QStringLiteral("Delay Level") },
    { 71, QStringLiteral("High Pass Filter") },
    { 72, QStringLiteral("Low Pass Filter") },
    { 74, QStringLiteral("Reverb Time") },
    { 75, QStringLiteral("Reverb High") },
    { 76, QStringLiteral("Reverb Diffusion") },
    { 77, QStringLiteral("Reverb Density") },
    { 78, QStringLiteral("Reverb Level") },
};

const QMap<int, QString> AmpMultiPhaserKnobParameters =
{
    {  2, QStringLiteral("Compressor Threshold") },
    {  4, QStringLiteral("Delay Feedback") },
    {  5, QStringLiteral("Reverb Ini. Delay") },
    { 11, QStringLiteral("Amp Type") },
    { 12, QStringLiteral("Speaker Simulator") },
    { 14, QStringLiteral("Tremolo Wave") },
    { 19, QStringLiteral("Gain") },
    { 20, QStringLiteral("Master") },
    { 23, QStringLiteral("Tone") },
    { 25, QStringLiteral("Treble") },
    { 26, QStringLiteral("High Middle") },
    { 27, QStringLiteral("Low Middle") },
    { 28, QStringLiteral("Bass") },
    { 29, QStringLiteral("Presence") },
    { 31, QStringLiteral("Noise Gate Threshold") },
    { 32, QStringLiteral("Noise Gate Attack") },
    { 33, QStringLiteral("Noise Gate Hold") },
    { 34, QStringLiteral("Noise Gate Decay") },
    { 41, QStringLiteral("Compressor Ratio") },
    { 42, QStringLiteral("Compressor Attack") },
    { 43, QStringLiteral("Compressor Release") },
    { 44, QStringLiteral("Compressor Knee") },
    { 45, QStringLiteral("Compressor Gain") },
    { 52, QStringLiteral("Phaser Speed") },
    { 53, QStringLiteral("Phaser Depth") },
    { 54, QStringLiteral("Phaser Feedback") },
    { 55, QStringLiteral("Phaser Level") },
    { 63, QStringLiteral("Delay Tap Left") },
    { 64, QStringLiteral("Delay Tap Right") },
    { 65, QStringLiteral("Delay Feedback Gain") },
    { 66, QStringLiteral("Delay High") },
    { 67, QStringLiteral("Delay Level") },
    { 71, QStringLiteral("High Pass Filter") },
    { 72, QStringLiteral("Low Pass Filter") },
    { 74, QStringLiteral("Reverb Time") },
    { 75, QStringLiteral("Reverb High") },
    { 76, QStringLiteral("Reverb Diffusion") },
    { 77, QStringLiteral("Reverb Density") },
    { 78, QStringLiteral("Reverb Level") },
};

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

const QMap<int, QString> DistortionMultiChorusKnobParameters =
{
    {  0, QStringLiteral("EQ 1 Frequency") },
    {  1, QStringLiteral("Pre EQ Level") },
    {  2, QStringLiteral("Compressor Threshold") },
    {  3, QStringLiteral("Chorus Delay") },
    {  4, QStringLiteral("Delay Feedback") },
    {  5, QStringLiteral("Reverb Ini. Delay") },
    {  8, QStringLiteral("Gain") },
    {  9, QStringLiteral("Master") },
    { 10, QStringLiteral("Tone") },
    { 11, QStringLiteral("Type") },
    { 14, QStringLiteral("Chorus Wave") },
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
    { 41, QStringLiteral("Compressor Ratio") },
    { 42, QStringLiteral("Compressor Attack") },
    { 43, QStringLiteral("Compressor Release") },
    { 44, QStringLiteral("Compressor Knee") },
    { 45, QStringLiteral("Compressor Gain") },
    { 48, QStringLiteral("Noise Gate Threshold") },
    { 49, QStringLiteral("Noise Gate Attack") },
    { 50, QStringLiteral("Noise Gate Hold") },
    { 51, QStringLiteral("Noise Gate Decay") },
    { 52, QStringLiteral("Chorus Speed") },
    { 53, QStringLiteral("Chorus Depth") },
    { 54, QStringLiteral("Chorus Level") },
    { 63, QStringLiteral("Delay Tap Left") },
    { 64, QStringLiteral("Delay Tap Right") },
    { 65, QStringLiteral("Delay Feedback Gain") },
    { 66, QStringLiteral("Delay High") },
    { 67, QStringLiteral("Delay Level") },
    { 71, QStringLiteral("High Pass Filter") },
    { 72, QStringLiteral("Low Pass Filter") },
    { 74, QStringLiteral("Reverb Time") },
    { 75, QStringLiteral("Reverb High") },
    { 76, QStringLiteral("Reverb Diffusion") },
    { 77, QStringLiteral("Reverb Density") },
    { 78, QStringLiteral("Reverb Level") }
};

const QMap<int, QString> DistortionMultiFlangeKnobParameters =
{
    {  0, QStringLiteral("EQ 1 Frequency") },
    {  1, QStringLiteral("Pre EQ Level") },
    {  2, QStringLiteral("Compressor Threshold") },
    {  3, QStringLiteral("Flanger Delay") },
    {  4, QStringLiteral("Delay Feedback") },
    {  5, QStringLiteral("Reverb Ini. Delay") },
    {  8, QStringLiteral("Gain") },
    {  9, QStringLiteral("Master") },
    { 10, QStringLiteral("Tone") },
    { 11, QStringLiteral("Type") },
    { 14, QStringLiteral("Flanger Wave") },
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
    { 41, QStringLiteral("Compressor Ratio") },
    { 42, QStringLiteral("Compressor Attack") },
    { 43, QStringLiteral("Compressor Release") },
    { 44, QStringLiteral("Compressor Knee") },
    { 45, QStringLiteral("Compressor Gain") },
    { 48, QStringLiteral("Noise Gate Threshold") },
    { 49, QStringLiteral("Noise Gate Attack") },
    { 50, QStringLiteral("Noise Gate Hold") },
    { 51, QStringLiteral("Noise Gate Decay") },
    { 52, QStringLiteral("Flanger Speed") },
    { 53, QStringLiteral("Flanger Depth") },
    { 54, QStringLiteral("Flanger Feedback") },
    { 55, QStringLiteral("Flanger Level") },
    { 63, QStringLiteral("Delay Tap Left") },
    { 64, QStringLiteral("Delay Tap Right") },
    { 65, QStringLiteral("Delay Feedback Gain") },
    { 66, QStringLiteral("Delay High") },
    { 67, QStringLiteral("Delay Level") },
    { 71, QStringLiteral("High Pass Filter") },
    { 72, QStringLiteral("Low Pass Filter") },
    { 74, QStringLiteral("Reverb Time") },
    { 75, QStringLiteral("Reverb High") },
    { 76, QStringLiteral("Reverb Diffusion") },
    { 77, QStringLiteral("Reverb Density") },
    { 78, QStringLiteral("Reverb Level") }
};

const QMap<int, QString> DistortionMultiTremoloKnobParameters =
{
    {  0, QStringLiteral("EQ 1 Frequency") },
    {  1, QStringLiteral("Pre EQ Level") },
    {  2, QStringLiteral("Compressor Threshold") },
    {  4, QStringLiteral("Delay Feedback") },
    {  5, QStringLiteral("Reverb Ini. Delay") },
    {  8, QStringLiteral("Gain") },
    {  9, QStringLiteral("Master") },
    { 10, QStringLiteral("Tone") },
    { 11, QStringLiteral("Type") },
    { 14, QStringLiteral("Tremolo Wave") },
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
    { 41, QStringLiteral("Compressor Ratio") },
    { 42, QStringLiteral("Compressor Attack") },
    { 43, QStringLiteral("Compressor Release") },
    { 44, QStringLiteral("Compressor Knee") },
    { 45, QStringLiteral("Compressor Gain") },
    { 48, QStringLiteral("Noise Gate Threshold") },
    { 49, QStringLiteral("Noise Gate Attack") },
    { 50, QStringLiteral("Noise Gate Hold") },
    { 51, QStringLiteral("Noise Gate Decay") },
    { 52, QStringLiteral("Tremolo Speed") },
    { 53, QStringLiteral("Tremolo Depth") },
    { 63, QStringLiteral("Delay Tap Left") },
    { 64, QStringLiteral("Delay Tap Right") },
    { 65, QStringLiteral("Delay Feedback Gain") },
    { 66, QStringLiteral("Delay High") },
    { 67, QStringLiteral("Delay Level") },
    { 71, QStringLiteral("High Pass Filter") },
    { 72, QStringLiteral("Low Pass Filter") },
    { 74, QStringLiteral("Reverb Time") },
    { 75, QStringLiteral("Reverb High") },
    { 76, QStringLiteral("Reverb Diffusion") },
    { 77, QStringLiteral("Reverb Density") },
    { 78, QStringLiteral("Reverb Level") }
};

const QMap<int, QString> DistortionMultiPhaseKnobParameters =
{
    {  0, QStringLiteral("EQ 1 Frequency") },
    {  1, QStringLiteral("Pre EQ Level") },
    {  2, QStringLiteral("Compressor Threshold") },
    {  4, QStringLiteral("Delay Feedback") },
    {  5, QStringLiteral("Reverb Ini. Delay") },
    {  8, QStringLiteral("Gain") },
    {  9, QStringLiteral("Master") },
    { 10, QStringLiteral("Tone") },
    { 11, QStringLiteral("Type") },
    { 14, QStringLiteral("Phaser Wave") },
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
    { 41, QStringLiteral("Compressor Ratio") },
    { 42, QStringLiteral("Compressor Attack") },
    { 43, QStringLiteral("Compressor Release") },
    { 44, QStringLiteral("Compressor Knee") },
    { 45, QStringLiteral("Compressor Gain") },
    { 48, QStringLiteral("Noise Gate Threshold") },
    { 49, QStringLiteral("Noise Gate Attack") },
    { 50, QStringLiteral("Noise Gate Hold") },
    { 51, QStringLiteral("Noise Gate Decay") },
    { 52, QStringLiteral("Phaser Speed") },
    { 53, QStringLiteral("Phaser Depth") },
    { 54, QStringLiteral("Phaser Feedback") },
    { 55, QStringLiteral("Phaser Level") },
    { 63, QStringLiteral("Delay Tap Left") },
    { 64, QStringLiteral("Delay Tap Right") },
    { 65, QStringLiteral("Delay Feedback Gain") },
    { 66, QStringLiteral("Delay High") },
    { 67, QStringLiteral("Delay Level") },
    { 71, QStringLiteral("High Pass Filter") },
    { 72, QStringLiteral("Low Pass Filter") },
    { 74, QStringLiteral("Reverb Time") },
    { 75, QStringLiteral("Reverb High") },
    { 76, QStringLiteral("Reverb Diffusion") },
    { 77, QStringLiteral("Reverb Density") },
    { 78, QStringLiteral("Reverb Level") }
};

const QMap<int, QString> ReverbKnobParameters =
{
    {  0, QStringLiteral("High Ratio") },
    {  8, QStringLiteral("Init Delay") },
    {  9, QStringLiteral("ER/Rev Delay") },
    { 10, QStringLiteral("Reverb Time") },
    { 11, QStringLiteral("Reverb Type") },
    { 19, QStringLiteral("Low Ratio") },
    { 20, QStringLiteral("Diffusion") },
    { 21, QStringLiteral("Density") },
    { 22, QStringLiteral("ER/Rev Balance") },
    { 23, QStringLiteral("High Pass Filter") },
    { 24, QStringLiteral("Low Pass Filter") },
    { 25, QStringLiteral("Gate Level") },
    { 26, QStringLiteral("Gate Attack") },
    { 27, QStringLiteral("Gate Hold") },
    { 28, QStringLiteral("Gate Decay") },
    { 29, QStringLiteral("Mix") },
};

const QMap<int, QString> EarlyRefKnobParameters =
{
    {   8, QStringLiteral("Init Delay") },
    {   9, QStringLiteral("Feedback Gain") },
    {  10, QStringLiteral("Room Size") },
    {  11, QStringLiteral("Type") },
    {  20, QStringLiteral("Liveness") },
    {  21, QStringLiteral("Diffusion") },
    {  22, QStringLiteral("Density") },
    {  23, QStringLiteral("ER Number") },
    {  26, QStringLiteral("High Ratio") },
    {  27, QStringLiteral("High Pass Filter") },
    {  28, QStringLiteral("Low Pass Filter") },
    {  29, QStringLiteral("Mix") }
};

const QMap<int, QString> MonoDelayKnobParameters =
{
    {   8, QStringLiteral("Time") },
    {   9, QStringLiteral("Feedback Gain") },
    {  20, QStringLiteral("High Ratio") },
    {  21, QStringLiteral("High Pass Filter") },
    {  22, QStringLiteral("Low Pass Filter") },
    {  29, QStringLiteral("Mix") }
};

const QMap<int, QString> StereoDelayKnobParameters =
{
    {   0, QStringLiteral("Feedback Gain Right") },
    {   8, QStringLiteral("Time Left") },
    {   9, QStringLiteral("Time Right") },
    {  10, QStringLiteral("Feedback Gain Left") },
    {  19, QStringLiteral("High Ratio") },
    {  20, QStringLiteral("High Pass Filter") },
    {  21, QStringLiteral("Low Pass Filter") },
    {  29, QStringLiteral("Mix") }
};

const QMap<int, QString> ModulationDelayKnobParameters =
{
    {   8, QStringLiteral("Time") },
    {   9, QStringLiteral("Feedback Gain") },
    {  10, QStringLiteral("Frequency") },
    {  11, QStringLiteral("Wave") },
    {  20, QStringLiteral("High Pass Filter") },
    {  21, QStringLiteral("Low Pass Filter") },
    {  22, QStringLiteral("High Ratio") },
    {  23, QStringLiteral("Depth") },
    {  29, QStringLiteral("Mix") }
};

const QMap<int, QString> DelayLCRKnobParameters =
{
    {   0, QStringLiteral("Delay Feedback") },
    {   8, QStringLiteral("Time Left") },
    {   9, QStringLiteral("Time Center") },
    {  10, QStringLiteral("Time Right") },
    {  19, QStringLiteral("Level Left") },
    {  20, QStringLiteral("Level Center") },
    {  21, QStringLiteral("Level Right") },
    {  22, QStringLiteral("Feedback Gain") },
    {  23, QStringLiteral("High Ratio") },
    {  24, QStringLiteral("High Pass Filter") },
    {  25, QStringLiteral("Low Pass Filter") },
    {  29, QStringLiteral("Mix") }
};

const QMap<int, QString> EchoKnobParameters =
{
    {   0, QStringLiteral("Feedback Delay Right") },
    {   8, QStringLiteral("Delay Left") },
    {   9, QStringLiteral("Delay Right") },
    {  10, QStringLiteral("Feedback Delay Left") },
    {  19, QStringLiteral("Feedback Gain Left") },
    {  20, QStringLiteral("Feedback Gain Right") },
    {  21, QStringLiteral("L->R Feedback Gain") },
    {  22, QStringLiteral("R->L Feedback Gain") },
    {  23, QStringLiteral("High Ratio") },
    {  24, QStringLiteral("High Pass Filter") },
    {  25, QStringLiteral("Low Pass Filter") },
    {  29, QStringLiteral("Mix") }
};

const QMap<int, QString> ChorusKnobParameters =
{
    {   0, QStringLiteral("Modulation Delay") },
    {   8, QStringLiteral("Frequency") },
    {   9, QStringLiteral("AM Depth") },
    {  10, QStringLiteral("PM Depth") },
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

const QMap<int, QString> SymphonicKnobParameters =
{
    {   8, QStringLiteral("Frequency") },
    {   9, QStringLiteral("Depth") },
    {  10, QStringLiteral("Modulation Delay") },
    {  11, QStringLiteral("Wave") },
    {  19, QStringLiteral("LSH Frequency") },
    {  20, QStringLiteral("LSH Gain") },
    {  21, QStringLiteral("EQ Frequency") },
    {  22, QStringLiteral("EQ Gain") },
    {  23, QStringLiteral("EQ Q") },
    {  25, QStringLiteral("HSH Frequency") },
    {  26, QStringLiteral("HSH Gain") },
    {  29, QStringLiteral("Mix") }
};

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

const QMap<int, QString> AutoPanKnobParameters =
{
    {   0, QStringLiteral("Frequency") },
    {  11, QStringLiteral("Wave") },
    {  19, QStringLiteral("Depth") },
    {  20, QStringLiteral("Direction") },
    {  21, QStringLiteral("LSH Frequency") },
    {  22, QStringLiteral("LSH Gain") },
    {  24, QStringLiteral("EQ Frequency") },
    {  25, QStringLiteral("EQ Gain") },
    {  26, QStringLiteral("EQ Q") },
    {  27, QStringLiteral("HSH Frequency") },
    {  28, QStringLiteral("HSH Gain") }
};

const QMap<int, QString> TremoloKnobParameters =
{
    {   0, QStringLiteral("Frequency") },
    {  11, QStringLiteral("Wave") },
    {  19, QStringLiteral("Depth") },
    {  20, QStringLiteral("LSH Frequency") },
    {  21, QStringLiteral("LSH Gain") },
    {  24, QStringLiteral("EQ Frequency") },
    {  25, QStringLiteral("EQ Gain") },
    {  26, QStringLiteral("EQ Q") },
    {  27, QStringLiteral("HSH Frequency") },
    {  28, QStringLiteral("HSH Gain") }
};

const QMap<int, QString> HQPitchKnobParameters =
{
    {   8, QStringLiteral("Delay") },
    {   9, QStringLiteral("Feedback Gain") },
    {  11, QStringLiteral("Mode") },
    {  19, QStringLiteral("Pitch") },
    {  20, QStringLiteral("Fine") },
    {  29, QStringLiteral("Mix") }
};

const QMap<int, QString> DualPitchKnobParameters =
{
    {   0, QStringLiteral("2 Feedback Gain") },
    {   8, QStringLiteral("1 Delay") },
    {   9, QStringLiteral("1 Feedback Gain") },
    {  10, QStringLiteral("2 Delay") },
    {  11, QStringLiteral("Mode") },
    {  19, QStringLiteral("1 Pitch") },
    {  20, QStringLiteral("1 Fine") },
    {  21, QStringLiteral("1 Level") },
    {  22, QStringLiteral("1 Pan") },
    {  23, QStringLiteral("2 Pitch") },
    {  24, QStringLiteral("2 Fine") },
    {  25, QStringLiteral("2 Level") },
    {  26, QStringLiteral("2 Pan") },
    {  29, QStringLiteral("Mix") }
};

const QMap<int, QString> RingModKnobParameters =
{
    {   8, QStringLiteral("OSC Freq") },
    {   9, QStringLiteral("FM Freq") },
    {  11, QStringLiteral("Source") },
    {  22, QStringLiteral("FM Depth") },
    {  29, QStringLiteral("Mix") }
};

const QMap<int, QString> ModFilterKnobParameters =
{
    {   0, QStringLiteral("Frequency") },
    {  11, QStringLiteral("Type") },
    {  19, QStringLiteral("Depth") },
    {  20, QStringLiteral("Phase") },
    {  21, QStringLiteral("Offset") },
    {  22, QStringLiteral("Resonance") },
    {  23, QStringLiteral("Level") },
    {  29, QStringLiteral("Mix") }
};

const QMap<int, QString> DigitalDistortionKnobParameters =
{
    {  11, QStringLiteral("Type") },
    {  19, QStringLiteral("Drive") },
    {  20, QStringLiteral("Master") },
    {  21, QStringLiteral("Tone") },
    {  22, QStringLiteral("Noise Gate") }
};

const QMap<int, QString> DynaFilterKnobParameters =
{
    {  10, QStringLiteral("Decay") },
    {  11, QStringLiteral("Type") },
    {  19, QStringLiteral("Direction") },
    {  20, QStringLiteral("Sensivity") },
    {  21, QStringLiteral("Offset") },
    {  22, QStringLiteral("Resonance") },
    {  23, QStringLiteral("Level") },
    {  29, QStringLiteral("Mix") }
};

const QMap<int, QString> DynaFlangeKnobParameters =
{
    {   0, QStringLiteral("Feedback Gain") },
    {  10, QStringLiteral("Decay") },
    {  11, QStringLiteral("Type") },
    {  19, QStringLiteral("Direction") },
    {  20, QStringLiteral("Sensivity") },
    {  21, QStringLiteral("Offset") },
    {  22, QStringLiteral("LSH Frequency") },
    {  23, QStringLiteral("LSH Gain") },
    {  24, QStringLiteral("EQ Frequency") },
    {  25, QStringLiteral("EQ Gain") },
    {  26, QStringLiteral("EQ Q") },
    {  27, QStringLiteral("HSH Frequency") },
    {  28, QStringLiteral("HSH Gain") },
    {  29, QStringLiteral("Mix") }
};

const QMap<int, QString> DynaPhaserKnobParameters =
{
    {   0, QStringLiteral("Feedback Gain") },
    {  10, QStringLiteral("Decay") },
    {  19, QStringLiteral("Direction") },
    {  20, QStringLiteral("Sensivity") },
    {  21, QStringLiteral("Offset") },
    {  22, QStringLiteral("Stage") },
    {  24, QStringLiteral("LSH Frequency") },
    {  25, QStringLiteral("LSH Gain") },
    {  26, QStringLiteral("HSH Frequency") },
    {  27, QStringLiteral("HSH Gain") },
    {  29, QStringLiteral("Mix") }
};

const QMap<int, QString> ReverbChorusKnobParameters =
{
    {   8, QStringLiteral("Init Delay") },
    {   9, QStringLiteral("Chorus Frequency") },
    {  10, QStringLiteral("Modulation Delay") },
    {  11, QStringLiteral("Wave") },
    {  19, QStringLiteral("Reverb Time") },
    {  20, QStringLiteral("High Ratio") },
    {  21, QStringLiteral("Diffusion") },
    {  22, QStringLiteral("Density") },
    {  23, QStringLiteral("High Pass Filter") },
    {  25, QStringLiteral("Low Pass Filter") },
    {  26, QStringLiteral("Balance") },
    {  27, QStringLiteral("AM Depth") },
    {  28, QStringLiteral("PM Depth") },
    {  29, QStringLiteral("Mix") }
};

const QMap<int, QString> ReverbFlangeKnobParameters =
{
    {   0, QStringLiteral("Feedback Gain") },
    {   8, QStringLiteral("Init Delay") },
    {   9, QStringLiteral("Flanger Frequency") },
    {  10, QStringLiteral("Modulation Delay") },
    {  11, QStringLiteral("Wave") },
    {  19, QStringLiteral("Reverb Time") },
    {  20, QStringLiteral("High Ratio") },
    {  21, QStringLiteral("Diffusion") },
    {  22, QStringLiteral("Density") },
    {  23, QStringLiteral("High Pass Filter") },
    {  25, QStringLiteral("Low Pass Filter") },
    {  26, QStringLiteral("Balance") },
    {  27, QStringLiteral("Depth") },
    {  29, QStringLiteral("Mix") }
};

const QMap<int, QString> ReverbSymphonicKnobParameters =
{
    {   8, QStringLiteral("Init Delay") },
    {   9, QStringLiteral("Symphonic Frequency") },
    {  10, QStringLiteral("Modulation Delay") },
    {  11, QStringLiteral("Wave") },
    {  19, QStringLiteral("Reverb Time") },
    {  20, QStringLiteral("High Ratio") },
    {  21, QStringLiteral("Diffusion") },
    {  22, QStringLiteral("Density") },
    {  23, QStringLiteral("High Pass Filter") },
    {  25, QStringLiteral("Low Pass Filter") },
    {  26, QStringLiteral("Balance") },
    {  27, QStringLiteral("Depth") },
    {  29, QStringLiteral("Mix") }
};

const QMap<int, QString> ReverbPanKnobParameters =
{
    {   8, QStringLiteral("Init Delay") },
    {   9, QStringLiteral("Pan Frequency") },
    {  11, QStringLiteral("Wave") },
    {  19, QStringLiteral("Reverb Time") },
    {  20, QStringLiteral("High Ratio") },
    {  21, QStringLiteral("Diffusion") },
    {  22, QStringLiteral("Density") },
    {  23, QStringLiteral("High Pass Filter") },
    {  25, QStringLiteral("Low Pass Filter") },
    {  26, QStringLiteral("Balance") },
    {  27, QStringLiteral("Depth") },
    {  28, QStringLiteral("Direction") },
    {  29, QStringLiteral("Mix") }
};

const QMap<int, QString> DelayEarlyRefKnobParameters =
{
    {   0, QStringLiteral("Feedback Gain") },
    {   1, QStringLiteral("Init Delay") },
    {   8, QStringLiteral("Delay Time Left") },
    {   9, QStringLiteral("Delay Time Right") },
    {  10, QStringLiteral("Delay Feedback") },
    {  12, QStringLiteral("Type") },
    {  19, QStringLiteral("High Ratio") },
    {  20, QStringLiteral("High Pass Filter") },
    {  21, QStringLiteral("Low Pass Filter") },
    {  22, QStringLiteral("Balance") },
    {  29, QStringLiteral("Mix") },
    {  30, QStringLiteral("Size") },
    {  31, QStringLiteral("Liveness") },
    {  32, QStringLiteral("Diffusion") },
    {  33, QStringLiteral("Density") },
    {  34, QStringLiteral("ER Number") }
};

const QMap<int, QString> DelayReverbKnobParameters =
{
    {   0, QStringLiteral("Feedback Gain") },
    {   1, QStringLiteral("Init Delay") },
    {   8, QStringLiteral("Delay Time Left") },
    {   9, QStringLiteral("Delay Time Right") },
    {  10, QStringLiteral("Delay Feedback") },
    {  19, QStringLiteral("Delay High Ratio") },
    {  20, QStringLiteral("High Pass Filter") },
    {  21, QStringLiteral("Low Pass Filter") },
    {  22, QStringLiteral("Balance") },
    {  29, QStringLiteral("Mix") },
    {  30, QStringLiteral("Reverb Time") },
    {  31, QStringLiteral("Reverb High Ratio") },
    {  32, QStringLiteral("Diffusion") },
    {  33, QStringLiteral("Density") }
};

const QMap<int, QString> DistortionDelayKnobParameters =
{
    {   8, QStringLiteral("Delay Time") },
    {   9, QStringLiteral("Feedback Gain") },
    {  10, QStringLiteral("Frequency") },
    {  11, QStringLiteral("Type") },
    {  19, QStringLiteral("Drive") },
    {  20, QStringLiteral("Master") },
    {  21, QStringLiteral("Tone") },
    {  22, QStringLiteral("Noise Gate") },
    {  25, QStringLiteral("High Ratio") },
    {  26, QStringLiteral("Depth") },
    {  27, QStringLiteral("Balance") }
};

const QMap<int, QString> MultiFilterKnobParameters =
{
    {   11, QStringLiteral("Filter 1 Type") },
    {   12, QStringLiteral("Filter 2 Type") },
    {   13, QStringLiteral("Filter 3 Type") },
    {   19, QStringLiteral("Filter 1 Frequency") },
    {   20, QStringLiteral("Filter 1 Level") },
    {   21, QStringLiteral("Filter 1 Resonance") },
    {   29, QStringLiteral("Mix") },
    {   30, QStringLiteral("Filter 2 Frequency") },
    {   31, QStringLiteral("Filter 2 Level") },
    {   32, QStringLiteral("Filter 2 Resonance") },
    {   41, QStringLiteral("Filter 3 Frequency") },
    {   42, QStringLiteral("Filter 3 Level") },
    {   43, QStringLiteral("Filter 3 Resonance") }
};

const QMap<int, QString> MBandDynaKnobParameters =
{
    {    0, QStringLiteral("Lookup") },
    {    1, QStringLiteral("Compressor Threshold") },
    {    2, QStringLiteral("Expander Threshold") },
    {    3, QStringLiteral("Limiter Threshold") },
    {    8, QStringLiteral("Low Gain") },
    {    9, QStringLiteral("Middle Gain") },
    {   10, QStringLiteral("High Gain") },
    {   11, QStringLiteral("Slope") },
    {   12, QStringLiteral("Compressor Bypass") },
    {   13, QStringLiteral("Expander Bypass") },
    {   14, QStringLiteral("Limiter Bypass") },
    {   20, QStringLiteral("Ceiling") },
    {   21, QStringLiteral("L-M Xover") },
    {   22, QStringLiteral("M-H Xover") },
    {   23, QStringLiteral("Presence") },
    {   30, QStringLiteral("Compressor Ratio") },
    {   31, QStringLiteral("Compressor Attack") },
    {   32, QStringLiteral("Compressor Release") },
    {   33, QStringLiteral("Compressor Knee") },
    {   41, QStringLiteral("Expander Ratio") },
    {   43, QStringLiteral("Expander Release") },
    {   53, QStringLiteral("Limiter Attack") },
    {   54, QStringLiteral("Limiter Release") },
    {   55, QStringLiteral("Limiter Knee") }
};

const QMap<int, QString> VintageFlangeKnobParameters =
{
    {    0, QStringLiteral("Speed") },
    {   11, QStringLiteral("Type") },
    {   19, QStringLiteral("Depth") },
    {   20, QStringLiteral("Manual") },
    {   21, QStringLiteral("Feedback") },
    {   22, QStringLiteral("Spread") },
    {   23, QStringLiteral("Mix") }
};

const QMap<int, QString> MonoVintagePhaserKnobParameters =
{
    {    0, QStringLiteral("Mode") },
    {   11, QStringLiteral("Stage") },
    {   19, QStringLiteral("Speed") },
    {   20, QStringLiteral("Depth") },
    {   21, QStringLiteral("Manual") },
    {   22, QStringLiteral("Feedback") },
    {   23, QStringLiteral("Color") }
};

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

const QMap<int, QString> SpringReverbKnobParameters =
{
    {  0, QStringLiteral("Reverb") }
};

const QMap<int, QString> TapeEchoKnobParameters =
{
    {  0, QStringLiteral("Time") },
    { 19, QStringLiteral("Feedback") },
    { 20, QStringLiteral("Level") }
};

const QMap<int, QString> CompressorKnobParameters =
{
    {  0, QStringLiteral("Threshold") },
    { 19, QStringLiteral("Ratio") },
    { 20, QStringLiteral("Attack") },
    { 21, QStringLiteral("Release") },
    { 22, QStringLiteral("Knee") },
    { 23, QStringLiteral("Gain") }
};

const QMap<int, QString> BassPreampKnobParameters =
{
    { 1, QStringLiteral("Parametric EQ Freq") },
    { 8, QStringLiteral("Gain") },
    { 9, QStringLiteral("Master") },
    { 11, QStringLiteral("Type") },
    { 19, QStringLiteral("Bass") },
    { 20, QStringLiteral("Low Middle") },
    { 21, QStringLiteral("Middle") },
    { 22, QStringLiteral("High Middle") },
    { 23, QStringLiteral("Treble") },
    { 25, QStringLiteral("Bass Freq") },
    { 26, QStringLiteral("Low Mid Freq") },
    { 27, QStringLiteral("Mid Freq") },
    { 28, QStringLiteral("High Mid Freq") },
    { 29, QStringLiteral("Treble Freq") },
    { 30, QStringLiteral("Parametric EQ Freq") },
    { 31, QStringLiteral("Parametric EQ Gain") },
    { 32, QStringLiteral("Gate") },
    { 33, QStringLiteral("Speaker Simulator") },
    { 34, QStringLiteral("Limiter") },
    { 35, QStringLiteral("Compressor Ratio") },
    { 36, QStringLiteral("Compressor Threshold") },
    { 37, QStringLiteral("Compressor Attack") },
    { 38, QStringLiteral("Compressor Release") },
    { 39, QStringLiteral("Compressor Gain") },
    { 40, QStringLiteral("Compressor Knee") }
};


#endif // KNOBPARAMETES_H
