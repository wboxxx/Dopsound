/*
 * Copyright (C) 2018 Robert Vetter.
 * This file is part of the MagicstompFrenzy - an editor for Yamaha Magicstomp
 * effect processor
 * 
 * Original source: https://github.com/dulnikovsky/magicstompfrenzy
 * License: GPL-3.0
 * 
 * KEY EXCERPTS FOR REAL-TIME PARAMETER CONTROL
 * ============================================
 */

// SysEx Headers for Magicstomp
static const int sysExBulkHeaderLength = 8;
static const unsigned char sysExBulkHeader[sysExBulkHeaderLength] = { 0xF0, 0x43, 0x7D, 0x30, 0x55, 0x42, 0x39, 0x39 };
static const unsigned char dumpRequestHeader[] = { 0xF0, 0x43, 0x7D, 0x50, 0x55, 0x42, 0x30, 0x01 };

static const int parameterSendHeaderLength = 6;
static const unsigned char sysExParameterSendHeader[parameterSendHeaderLength] = { 0xF0, 0x43, 0x7D, 0x40, 0x55, 0x42 };

// KEY FUNCTION: Real-time parameter modification
void MainWindow::parameterChanged(int offset, int length, QWidget *paramEditWidget)
{
    qDebug("parameterChanged(offset=%d,len=%d)", offset, length);

    ArrayDataEditWidget *editWidget = static_cast<ArrayDataEditWidget *>( static_cast<QSplitter *>(centralWidget())->widget(1));
    if(editWidget == nullptr)
        return;

    if( offset == PatchName) // Name needs to be sent as single chars
    {
        length = 1;
        patchListModelList[currentPatchEdited.first]->patchUpdated(currentPatchEdited.second);
        QByteArray &dataArrRef = newPatchDataList[currentPatchEdited.first][currentPatchEdited.second];
        patchNameLabel->setText( QString::number( currentPatchEdited.second +1).rightJustified(2, '0') + " " + dataArrRef.mid(PatchName, PatchNameLength));
    }

    MidiEvent *midiev = new MidiEvent(static_cast<QEvent::Type>(UserEventTypes::MidiSysEx));
    QByteArray *reqArr = midiev->sysExData();
    
    // Add SysEx header
    reqArr->append(QByteArray::fromRawData(reinterpret_cast<const char*>(&sysExParameterSendHeader[0]), parameterSendHeaderLength));
    reqArr->append(0x20);
    
    // Determine section (common or effect)
    if(offset < PatchCommonLength)
    {
        reqArr->append(static_cast<char>(0x00));
        reqArr->append(static_cast<char>(offset));
    }
    else
    {
        reqArr->append(0x01);
        reqArr->append(static_cast<char>(offset - PatchCommonLength));
    }
    
    // Add parameter data
    for(int i= 0; i< length; i++)
    {
        reqArr->append( *(editWidget->DataArray()->constData()+offset+i));
    }
    
    // Add SysEx end
    reqArr->append(static_cast<char>(0xF7));

    // Check for multiple events for same parameter in the midi out queue.
    // This can happen during fast changing a parameter by Control Change messages
    QQueue<MidiEvent *>::iterator it = midiOutQueue.begin();
    while (it != midiOutQueue.end())
    {
        QByteArray *sysexData = (*it)->sysExData();
        if( sysexData->startsWith(reqArr->left(parameterSendHeaderLength +3)))
        {
            MidiEvent *eventToRemove = *it;
            it = midiOutQueue.erase( it);
            delete eventToRemove;
            qDebug ("Removed item");
        }
        else
        {
            it++;
        }
    }

#if QT_VERSION >= 0x050900
    qDebug() << reqArr->toHex(',');
#endif
    midiOutQueue.enqueue( midiev);
    if(! midiOutTimer->isActive())
    {
        midiOutTimer->setInterval(10);
        midiOutTimer->start();
    }

    if( offset == PatchName) // Name needs to be sent as single chars
    {
        for(int i= PatchName + 1; i < PatchNameLast; i++)
        {
            parameterChanged( i, 1, paramEditWidget);
        }
    }

    if( (! paramEditWidget->hasFocus()) && (! tmpArray.isEmpty()))
    {
        newPatchDataList[currentPatchEdited.first][currentPatchEdited.second].replace(offset, length, tmpArray);
        tmpArray.clear();
    }

    QMap<int, widgetWithVal>::const_iterator iter = ccToWidgetMap.constBegin();
    while (iter != ccToWidgetMap.constEnd())
    {
        if( paramEditWidget->hasFocus() && iter.value().dspinBox == paramEditWidget)
        {
            buildCCToWidgetMap();
            break;
        }
        iter++;
    }
}

// KEY FUNCTION: Checksum calculation
char MainWindow::calcChecksum(const char *data, int dataLength)
{
    char checkSum = 0;
    for (int i = 0; i < dataLength; ++i)
    {
        checkSum += *data++;
    }
    return ((-checkSum) & 0x7f);
}

// SysEx message validation with checksum
void MainWindow::midiEvent(MidiEvent *ev)
{
    if( ev->type() == static_cast<QEvent::Type>(UserEventTypes::MidiSysEx))
    {
        const QByteArray *inData = ev->sysExData();
        if( inData->size() < 13)
            return;

        if( inData->left(sysExBulkHeaderLength) != QByteArray(reinterpret_cast<const char*>(&sysExBulkHeader[0]),sysExBulkHeaderLength) )
            return;

        ev->accept();

        if( static_cast<unsigned char>(inData->at( inData->length()-1)) != 0xF7)
            return;

        char checkSum = calcChecksum(inData->constData()+sysExBulkHeaderLength, inData->length()-sysExBulkHeaderLength-2);
        if( checkSum != inData->at( inData->length()-1-1))
        {
            qDebug("Checksum Error!");
            return;
        }

        if(! isInTransmissionState && !isInImportState) // incoming unexpected data
        {
            qDebug("Incoming unexpected data!");
            return;
        }

        // Process incoming SysEx data...
    }
}


