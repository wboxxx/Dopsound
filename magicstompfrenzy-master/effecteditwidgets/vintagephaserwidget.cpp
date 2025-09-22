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
#include "vintagephaserwidget.h"
#include <QGridLayout>
#include <QDoubleSpinBox>
#include <QLabel>
#include <QSpinBox>
#include <QComboBox>
#include <QGroupBox>

VintagePhaserWidget::VintagePhaserWidget(bool isMono, QWidget *parent) :
    EffectEditBaseWidget(parent)
{
    QSpinBox *spinBox;
    QDoubleSpinBox *dspinBox;
    QGridLayout *mainlyt = new QGridLayout();

    mainlyt->addWidget(new QLabel(tr("Stage")), 0, 0);
    QComboBox *waveComboBox = new QComboBox();
    waveComboBox->addItem(QStringLiteral("4"));
    waveComboBox->addItem(QStringLiteral("6"));
    waveComboBox->addItem(QStringLiteral("8"));
    waveComboBox->addItem(QStringLiteral("10"));
    if(isMono)
    {
        waveComboBox->addItem(QStringLiteral("12"));
        waveComboBox->addItem(QStringLiteral("16"));
    }
    waveComboBox->setCurrentIndex(-1);
    waveComboBox->setProperty( ArrayDataEditWidget::valuePropertyName, QStringLiteral("currentIndex"));
    waveComboBox->setProperty( ArrayDataEditWidget::dataOffsetProperty, Stage);
    waveComboBox->setProperty( ArrayDataEditWidget::dataLenghtProperty, 1);
    mainlyt->addWidget( waveComboBox, 1, 0);

    mainlyt->addWidget(new QLabel(tr("Mode")), 0, 1);
    spinBox = new QSpinBox();
    spinBox->setMinimum(1);
    spinBox->setMaximum(2);
    spinBox->setProperty( ArrayDataEditWidget::dataOffsetProperty, Mode);
    spinBox->setProperty( ArrayDataEditWidget::dataLenghtProperty, 2);
    spinBox->setProperty( ArrayDataEditWidget::convertMethodProperty, QStringLiteral("scaleAndAdd(1, 1)"));
    mainlyt->addWidget(spinBox, 1, 1);

    mainlyt->addWidget(new QLabel(tr("Speed")), 0, 2);
    dspinBox = createStandard10DblSpinBox(Speed);
    mainlyt->addWidget(dspinBox, 1, 2);

    mainlyt->addWidget(new QLabel(tr("Depth")), 0, 3);
    dspinBox = createStandard10DblSpinBox(Depth);
    mainlyt->addWidget(dspinBox, 1, 3);

    mainlyt->addWidget(new QLabel(tr("Manual")), 2, 0);
    dspinBox = createStandard10DblSpinBox(Manual);
    mainlyt->addWidget(dspinBox, 3, 0);

    mainlyt->addWidget(new QLabel(tr("Feedback")), 2, 1);
    dspinBox = createStandard10DblSpinBox(Feedback);
    mainlyt->addWidget(dspinBox, 3, 1);

    mainlyt->addWidget(new QLabel(tr("Color")), 2, 2);
    dspinBox = createStandard10DblSpinBox(Color);
    mainlyt->addWidget(dspinBox, 3, 2);

    if(! isMono)
    {
        mainlyt->addWidget(new QLabel(tr("Spread")), 2, 3);
        dspinBox = createStandard10DblSpinBox(Spread);
        mainlyt->addWidget(dspinBox, 3, 3);
    }

    mainlyt->setColumnStretch(4,2);
    mainlyt->setRowStretch(4,2);

    setLayout(mainlyt);
}
