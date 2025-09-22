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
#include "patchcommoneditorwidget.h"
#include "arraydataeditwidget.h"

#include "magicstomp.h"
#include "magicstomptext.h"

#include "knobparametermodel.h"
#include "knobparameters.h"

#include <QLineEdit>
#include <QLabel>
#include <QGridLayout>
#include <QSpinBox>
#include <QComboBox>

PatchCommonEditorWidget::PatchCommonEditorWidget(QWidget *parent)
 : QGroupBox( parent), knobparametermodel(nullptr)
{
    setTitle(tr("Patch Common Parameters"));

    QGridLayout *mainLayout = new QGridLayout();

    mainLayout->addWidget(new QLabel(tr("Type:")), 0, 0);
    QComboBox *typeComboBox = new QComboBox();
    typeComboBox->addItems( EffectTypeNameList);
    typeComboBox->setCurrentIndex(-1);
    typeComboBox->setProperty( ArrayDataEditWidget::valuePropertyName, QStringLiteral("currentIndex"));
    typeComboBox->setProperty( ArrayDataEditWidget::dataOffsetProperty, PatchType);
    typeComboBox->setProperty( ArrayDataEditWidget::dataLenghtProperty, 2);
    mainLayout->addWidget(typeComboBox, 1, 0);

    //connect(typeComboBox, SIGNAL(onPatchTypeChanged(int)), this, SLOT(typeComboChanged(int)));

    mainLayout->addWidget(new QLabel(tr("Name:")), 0, 1);
    QLineEdit *nameLineEdit = new QLineEdit();
    //nameLineEdit->setValidator(new QRegExpValidator( QRegExp("[a-z-A-Z_]+"), this ));
    nameLineEdit->setMaxLength(PatchNameLength);
    nameLineEdit->setProperty( ArrayDataEditWidget::dataOffsetProperty, PatchName);
    nameLineEdit->setProperty( ArrayDataEditWidget::dataLenghtProperty, PatchNameLength);
    mainLayout->addWidget(nameLineEdit, 1, 1);

    mainLayout->addWidget(new QLabel(tr("Knob 1")), 0, 2);
    knob1ComboBox = new QComboBox();
    knob1ComboBox->setProperty( ArrayDataEditWidget::valuePropertyName, QStringLiteral("currentIndex"));
    knob1ComboBox->setProperty( ArrayDataEditWidget::dataOffsetProperty, Control1);
    knob1ComboBox->setProperty( ArrayDataEditWidget::dataLenghtProperty, 2);
    mainLayout->addWidget(knob1ComboBox, 1, 2);
    mainLayout->setColumnStretch( 2, 2);

    mainLayout->addWidget(new QLabel(tr("Knob 2")), 0, 3);
    knob2ComboBox = new QComboBox();
    knob2ComboBox->setProperty( ArrayDataEditWidget::dataOffsetProperty, Control2);
    knob2ComboBox->setProperty( ArrayDataEditWidget::valuePropertyName, QStringLiteral("currentIndex"));
    knob2ComboBox->setProperty( ArrayDataEditWidget::dataLenghtProperty, 2);
    mainLayout->addWidget(knob2ComboBox, 1, 3);
    mainLayout->setColumnStretch( 3, 2);

    mainLayout->addWidget(new QLabel(tr("Knob 3")), 0, 4);
    knob3ComboBox = new QComboBox();
    knob3ComboBox->setProperty( ArrayDataEditWidget::dataOffsetProperty, Control3);
    knob3ComboBox->setProperty( ArrayDataEditWidget::valuePropertyName, QStringLiteral("currentIndex"));
    knob3ComboBox->setProperty( ArrayDataEditWidget::dataLenghtProperty, 2);
    mainLayout->addWidget(knob3ComboBox, 1, 4);
    mainLayout->setColumnStretch( 4, 2);

    setLayout( mainLayout);
}

void PatchCommonEditorWidget::onPatchTypeChanged(int type)
{
    qDebug("Patch Type Changed");

    knob1ComboBox->blockSignals(true);
    knob2ComboBox->blockSignals(true);
    knob3ComboBox->blockSignals(true);

    knob1ComboBox->clear();
    knob2ComboBox->clear();
    knob3ComboBox->clear();

    if( knobparametermodel )
        knobparametermodel->deleteLater();

    knobparametermodel = nullptr;

    switch (type) {
    case AcousticMulti:
        knobparametermodel = new KnobParameterModel( AcousticMultiKnobParameters, 41, this);
        break;
    case BassPreamp:
        knobparametermodel = new KnobParameterModel( BassPreampKnobParameters, 41, this);
        break;
    case EightBandParallelDelay:
    case EightBandSeriesDelay:
        knobparametermodel = new KnobParameterModel( EightBandParaDlyKnobParameters, 107, this);
        break;
    case FourBand2TapModDelay:
        knobparametermodel = new KnobParameterModel( FourBand2TapModDlyKnobParameters, 107, this);
        break;
    case TwoBand4TapModDelay:
        knobparametermodel = new KnobParameterModel( TwoBand4TapModDlyKnobParameters, 107, this);
        break;
    case EightMultiTapModDelay:
        knobparametermodel = new KnobParameterModel( OneBand8TapModDlyKnobParameters, 107, this);
        break;
    case TwoBandLong4ShortModDelay:
        knobparametermodel = new KnobParameterModel( TwoBandLong4ShortModDlyKnobParameters, 107, this);
        break;
    case ShortMediumLongModDelay:
        knobparametermodel = new KnobParameterModel( ShortMediumLongModDlyKnobParameters, 107, this);
        break;
    case AmpSimulator:
        knobparametermodel = new KnobParameterModel( AmpSimulatorKnobParameters, 35, this);
        break;
    case AmpMultiChorus:
        knobparametermodel = new KnobParameterModel( AmpMultiChorusKnobParameters, 79, this);
        break;
    case AmpMultiFlange:
        knobparametermodel = new KnobParameterModel( AmpMultiFlangeKnobParameters, 79, this);
        break;
    case AmpMultiTremolo:
        knobparametermodel = new KnobParameterModel( AmpMultiTremoloKnobParameters, 79, this);
        break;
    case AmpMultiPhaser:
        knobparametermodel = new KnobParameterModel( AmpMultiPhaserKnobParameters, 79, this);
        break;
    case Distortion:
        knobparametermodel = new KnobParameterModel( DistortionKnobParameters, 46, this);
        break;
    case DistorionMultiChorus:
        knobparametermodel = new KnobParameterModel( DistortionMultiChorusKnobParameters, 79, this);
        break;
    case DistorionMultiFlange:
        knobparametermodel = new KnobParameterModel( DistortionMultiFlangeKnobParameters, 79, this);
        break;
    case DistorionMultiTremolo:
        knobparametermodel = new KnobParameterModel( DistortionMultiTremoloKnobParameters, 79, this);
        break;
    case DistorionMultiPhaser:
        knobparametermodel = new KnobParameterModel( DistortionMultiPhaseKnobParameters, 79, this);
        break;
    case Reverb:
        knobparametermodel = new KnobParameterModel( ReverbKnobParameters, 30, this);
        break;
    case EarlyRef:
    case GateReverb:
    case ReverseGate:
        knobparametermodel = new KnobParameterModel( EarlyRefKnobParameters, 30, this);
        break;
    case MonoDelay:
        knobparametermodel = new KnobParameterModel( MonoDelayKnobParameters, 30, this);
        break;
    case StereoDelay:
        knobparametermodel = new KnobParameterModel( StereoDelayKnobParameters, 30, this);
        break;
    case ModDelay:
        knobparametermodel = new KnobParameterModel( ModulationDelayKnobParameters, 30, this);
        break;
    case DelayLCR:
        knobparametermodel = new KnobParameterModel( DelayLCRKnobParameters, 30, this);
        break;
    case Echo:
        knobparametermodel = new KnobParameterModel( EchoKnobParameters, 30, this);
        break;
    case Chorus:
        knobparametermodel = new KnobParameterModel( ChorusKnobParameters, 30, this);
        break;
    case Flange:
        knobparametermodel = new KnobParameterModel( FlangeKnobParameters, 30, this);
        break;
    case Symphonic:
        knobparametermodel = new KnobParameterModel( SymphonicKnobParameters, 30, this);
        break;
    case Phaser:
        knobparametermodel = new KnobParameterModel( PhaserKnobParameters, 30, this);
        break;
    case AutoPan:
        knobparametermodel = new KnobParameterModel( AutoPanKnobParameters, 30, this);
        break;
    case Tremolo:
        knobparametermodel = new KnobParameterModel( TremoloKnobParameters, 30, this);
        break;
    case HQPitch:
        knobparametermodel = new KnobParameterModel( HQPitchKnobParameters, 30, this);
        break;
    case DualPitch:
        knobparametermodel = new KnobParameterModel( DualPitchKnobParameters, 30, this);
        break;
    case RingMod:
        knobparametermodel = new KnobParameterModel( RingModKnobParameters, 30, this);
        break;
    case ModFilter:
        knobparametermodel = new KnobParameterModel( ModFilterKnobParameters, 30, this);
        break;
    case DigitalDistortion:
        knobparametermodel = new KnobParameterModel( DigitalDistortionKnobParameters, 30, this);
        break;
    case DynaFilter:
        knobparametermodel = new KnobParameterModel( DynaFilterKnobParameters, 30, this);
        break;
    case DynaFlange:
        knobparametermodel = new KnobParameterModel( DynaFlangeKnobParameters, 30, this);
        break;
    case DynaPhaser:
        knobparametermodel = new KnobParameterModel( DynaPhaserKnobParameters, 30, this);
        break;
    case ReverbChorusParallel:
    case ReverbChorusSerial:
        knobparametermodel = new KnobParameterModel( ReverbChorusKnobParameters, 30, this);
        break;
    case ReverbFlangeSerial:
    case ReverbFlangeParallel:
        knobparametermodel = new KnobParameterModel( ReverbFlangeKnobParameters, 30, this);
        break;
    case ReverbSymphonicSerial:
    case ReverbSymphonicParallel:
        knobparametermodel = new KnobParameterModel( ReverbSymphonicKnobParameters, 30, this);
        break;
    case ReverbPan:
        knobparametermodel = new KnobParameterModel( ReverbPanKnobParameters, 30, this);
        break;
    case DelayEarlyRefSerial:
    case DelayEarlyRefParallel:
        knobparametermodel = new KnobParameterModel( DelayEarlyRefKnobParameters, 35, this);
        break;
    case DelayReverbSerial:
    case DelayReverbParallel:
        knobparametermodel = new KnobParameterModel( DelayReverbKnobParameters, 35, this);
        break;
    case DistortionDelay:
        knobparametermodel = new KnobParameterModel( DistortionDelayKnobParameters, 28, this);
        break;
    case MultiFilter:
        knobparametermodel = new KnobParameterModel( MultiFilterKnobParameters, 44, this);
        break;
    case MBandDyna:
        knobparametermodel = new KnobParameterModel( MBandDynaKnobParameters, 56, this);
        break;
    case VintageFlange:
        knobparametermodel = new KnobParameterModel( VintageFlangeKnobParameters, 24, this);
        break;
    case MonoVintagePhaser:
    case StereoVintagePhaser:
        knobparametermodel = new KnobParameterModel( MonoVintagePhaserKnobParameters, 24, this);
        break;
    case ThreeBandParametricEQ:
        knobparametermodel = new KnobParameterModel( ThreeBandParametricEQKnobParameters, 30, this);
        break;
    case SpringReverb:
        knobparametermodel = new KnobParameterModel( SpringReverbKnobParameters, 2, this);
        break;
    case TapeEcho:
        knobparametermodel = new KnobParameterModel( TapeEchoKnobParameters, 21, this);
        break;
    case Compressor:
        knobparametermodel = new KnobParameterModel( CompressorKnobParameters, 28, this);
        break;
    default:
        break;
    }

    if( knobparametermodel )
    {
        knob1ComboBox->setModel( knobparametermodel );
        knob2ComboBox->setModel( knobparametermodel );
        knob3ComboBox->setModel( knobparametermodel );
    }

    knob1ComboBox->blockSignals(false);
    knob2ComboBox->blockSignals(false);
    knob3ComboBox->blockSignals(false);
}
