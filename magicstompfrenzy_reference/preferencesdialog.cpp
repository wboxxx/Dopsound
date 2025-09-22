/*
 * Copyright (C) 2018 Robert Vetter.
 * This file is part of the MagicstompFrenzy - an editor for Yamaha Magicstomp
 * effect processor
 * 
 * Original source: https://github.com/dulnikovsky/magicstompfrenzy
 * License: GPL-3.0
 * 
 * MIDI CONFIGURATION AND CHANNEL SETTINGS
 * =======================================
 */

// KEY: MIDI Channel configuration with OMNI default
QSpinBox *channelSpinBox = new QSpinBox();
channelSpinBox->setMinimum(0);
channelSpinBox->setMaximum(16);
channelSpinBox->setSpecialValueText(QStringLiteral("OMNI"));
settings.beginGroup(QStringLiteral("MidiControls"));
// KEY: Default MIDI channel is 0 (OMNI)
channelSpinBox->setValue(settings.value(QStringLiteral("MIDIChannel"), 0).toInt());
settings.endGroup();
connect( channelSpinBox, SIGNAL(valueChanged(int)), this, SIGNAL(midiChannelChanged(int)));
connect
    channelSpinBox, qOverload<int>(&QSpinBox::valueChanged),
    [=]( int val) {
        QSettings settings;
        settings.beginGroup(QStringLiteral("MidiControls"));
        settings.setValue(QStringLiteral("MIDIChannel"), val);
        settings.endGroup();
    }
);

// MIDI Port selection for input and output
void PreferencesDialog::midiInselectionChanged(const QItemSelection &selected, const QItemSelection &deselected)
{
    QModelIndexList indexList = selected.indexes();
    for( int i=0; i<indexList.size(); i++)
    {
        emit midiInPortStatusChanged( qvariant_cast<MidiClientPortId>( indexList.at(i).data(MidiPortModel::ClientPortIdRole)), true);
    }

    indexList = deselected.indexes();
    for( int i=0; i<indexList.size(); i++)
    {
        emit midiInPortStatusChanged( qvariant_cast<MidiClientPortId>( indexList.at(i).data(MidiPortModel::ClientPortIdRole)), false);
    }
}

void PreferencesDialog::midiOutselectionChanged(const QItemSelection &selected, const QItemSelection &deselected)
{
    QModelIndexList indexList = selected.indexes();
    for( int i=0; i<indexList.size(); i++)
    {
        emit midiOutPortStatusChanged( qvariant_cast<MidiClientPortId>( indexList.at(i).data(MidiPortModel::ClientPortIdRole)), true);
    }

    indexList = deselected.indexes();
    for( int i=0; i<indexList.size(); i++)
    {
        emit midiOutPortStatusChanged( qvariant_cast<MidiClientPortId>( indexList.at(i).data(MidiPortModel::ClientPortIdRole)), false);
    }
}

// Control Change parameter mapping
QSpinBox *PreferencesDialog::createParaCCSpinBox(const QString &name)
{
    QSpinBox *spinbox= new QSpinBox();
    spinbox->setMaximum(127);
    spinbox->setObjectName( name);

    QMap<QString, int>::iterator iter = paraToCCMap.find(name);
    if(iter != paraToCCMap.end())
    {
        spinbox->setValue( iter.value() & 0x7F);
    }
    connect(spinbox, SIGNAL(valueChanged(int)), this, SLOT(paraCCSpinBoxValueChanged(int)));
    return spinbox;
}

// Restore MIDI connections at startup
QCheckBox *restoreConnectionsCheckBox = new QCheckBox(tr("Reconnect at startup"));
QSettings settings;
restoreConnectionsCheckBox->setChecked(settings.value(QStringLiteral("RestoreMidiConnectionsAtStartUp"), true).toBool());
connect(
    restoreConnectionsCheckBox, &QCheckBox::toggled,
    [=]( bool checked) {
        QSettings settings;
        settings.setValue(QStringLiteral("RestoreMidiConnectionsAtStartUp"), checked);
    }
);


