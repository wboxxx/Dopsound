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
#ifndef MBANDDYNAWIDGET_H
#define MBANDDYNAWIDGET_H

#include "effecteditbasewidget.h"

class MBandDynaWidget: public EffectEditBaseWidget
{
    Q_OBJECT
public:
    explicit MBandDynaWidget( QWidget *parent = nullptr);

    enum ParameterOffsets
    {
        LookUp = 0x00, // 2 Bytes
        CompressorThreshold = 0x02, // 2 Bytes
        ExpanderThreshold = 0x04, // 2 Bytes
        LimiterThreshold = 0x06, // 2 Bytes

        LowGain = 0x10, // 2 Bytes
        MiddleGain = 0x12, // 2 Bytes
        HighGain = 0x14, // 2 Bytes

        Slope = 0x16,

        CompressorBypass = 0x17,
        ExpanderBypass = 0x18,
        LimiterBypass = 0x18,

        Ceiling = 0x1F,
        LMXover = 0x20,
        MHXover = 0x21,
        Presence = 0x22,

        Mix = 0x28,

        CompressorRatio = 0x29,
        CompressorAttack = 0x2A,
        CompressorRelease = 0x2B,
        CompressorKnee = 0x2C,

        ExpanderRatio = 0x34,
        ExpanderRelease = 0x36,

        LimiterAttack = 0x40,
        LimiterRelease = 0x41,
        LimiterKnee = 0x42
    };
};

#endif // MBANDDYNAWIDGET_H
