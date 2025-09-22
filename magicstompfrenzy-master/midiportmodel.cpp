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
#include "midiportmodel.h"
#ifdef Q_OS_LINUX
#include <alsa/asoundlib.h>
#endif
#ifdef Q_OS_MACOS
#include <AudioToolbox/AudioToolbox.h>
#endif
#ifdef Q_OS_WIN
#include <windows.h>
#include <mmsystem.h>
#include "inmidiheaderusedevent.h"
extern void CALLBACK MidiInProc(HMIDIIN hMidiIn, UINT wMsg, DWORD_PTR dwInstance, DWORD_PTR dwParam1, DWORD_PTR dwParam2);
#endif

QVariant MidiPortModel::data(const QModelIndex &index, int role) const
{
    if(role == Qt::DisplayRole)
    {
        return portList.at(index.row()).second;
    }
    else if(role == ClientPortIdRole)
    {
        QVariant valVariant;
        valVariant.setValue( portList.at(index.row()).first);
        return valVariant;
    }
    else if( role == isConnectedRole)
    {
        return connectionsCont.contains(portList.at(index.row()).first);
    }
    return QVariant();
}

int MidiPortModel::rowCount(const QModelIndex &parent) const
{
    Q_UNUSED(parent);
    return portList.size();
}

void MidiPortModel::scan()
{
    beginResetModel();
    portList.clear();
#ifdef Q_OS_LINUX
    snd_seq_client_info_t *cinfo;
    snd_seq_port_info_t *pinfo;
    int count;

    snd_seq_client_info_alloca(&cinfo);
    snd_seq_port_info_alloca(&pinfo);
    snd_seq_client_info_set_client(cinfo, -1);
    while (snd_seq_query_next_client(handle, cinfo) >= 0)
    {
        int clientId = snd_seq_client_info_get_client( cinfo);
        qDebug("Client  %3d '%-16s'", clientId, snd_seq_client_info_get_name( cinfo));
        if( (clientId == SND_SEQ_CLIENT_SYSTEM) || (clientId == snd_seq_client_id(handle)))
            continue;
        /* reset query info */
        snd_seq_port_info_set_client(pinfo, clientId);
        snd_seq_port_info_set_port(pinfo, -1);
        count = 0;
        while (snd_seq_query_next_port(handle, pinfo) >= 0)
        {
            unsigned int cap = snd_seq_port_info_get_capability(pinfo);
            if( ((cap & (SND_SEQ_PORT_CAP_READ|SND_SEQ_PORT_CAP_SUBS_READ)) && direction==ReadablePorts) ||
                    ((cap & (SND_SEQ_PORT_CAP_WRITE|SND_SEQ_PORT_CAP_SUBS_WRITE)) && direction==WritablePorts) )
            {
                MidiClientPortId mcpId( clientId, snd_seq_port_info_get_port(pinfo));
                portList.append(QPair<MidiClientPortId, QString>( mcpId, snd_seq_port_info_get_name(pinfo)));
            }
            count++;
        }
    }
#endif
#ifdef Q_OS_MAC
    if( direction == ReadablePorts)
    {
        unsigned long sourceCount = MIDIGetNumberOfSources();
        qDebug("%ld sources\n", sourceCount);

        for (unsigned int i = 0; i < sourceCount; ++i)
        {
            char charArr[256] = {0x00};
            MIDIEndpointRef src = MIDIGetSource(i);
            CFStringRef modelName = nullptr;
            MIDIObjectGetStringProperty(src, kMIDIPropertyModel, &modelName);
            if(modelName != nullptr)
                CFStringGetCString(modelName, charArr, sizeof (charArr), 0);

            QString fullName(charArr);

            CFStringRef name = nullptr;
            MIDIObjectGetStringProperty(src, kMIDIPropertyName, &name);
            if(name != nullptr)
                CFStringGetCString(name, charArr, sizeof (charArr), 0);

            fullName.append(" " + QString(charArr));

            portList.append(QPair<MidiClientPortId, QString>( src, fullName));
            qDebug(" source %d: %s %d\n", i, fullName.toLocal8Bit().constData(), src);
        }
    }
    else
    {
        unsigned long destCount = MIDIGetNumberOfDestinations();
        qDebug("%ld destinations\n", destCount);
        for (unsigned int i = 0; i < destCount; ++i)
        {
            char charArr[256] = {0x00};
            MIDIEndpointRef dest = MIDIGetDestination(i);
            CFStringRef modelName = nullptr;
            MIDIObjectGetStringProperty(dest, kMIDIPropertyModel, &modelName);

            if(modelName != nullptr)
                CFStringGetCString(modelName, charArr, sizeof (charArr), 0);

            QString fullName(charArr);

            CFStringRef name = nullptr;
            MIDIObjectGetStringProperty(dest, kMIDIPropertyName, &name);
            if(name != nullptr)
                CFStringGetCString(name, charArr, sizeof (charArr), 0);

            fullName.append(" " + QString(charArr));

            portList.append(QPair<MidiClientPortId, QString>( dest, fullName));
            qDebug(" destination %d: %s %d\n", i, fullName.toLocal8Bit().constData(), dest);
        }
    }
#endif
#ifdef Q_OS_WIN
    unsigned int numdevs;
    if( direction == ReadablePorts)
    {
        numdevs = midiInGetNumDevs();
        for( unsigned int i = 0; i<numdevs; i++)
        {
            MIDIINCAPS caps;
            midiInGetDevCaps(i, &caps, sizeof (caps));
            portList.append(QPair<MidiClientPortId, QString>( i, QString::fromWCharArray(caps.szPname)));

        }
    }
    else
    {
        numdevs = midiOutGetNumDevs();
        for( unsigned int i = 0; i<numdevs; i++)
        {
            MIDIOUTCAPS caps;
            midiOutGetDevCaps(i, &caps, sizeof (caps));
            portList.append(QPair<MidiClientPortId, QString>( i, QString::fromWCharArray(caps.szPname)));
        }
    }
#endif
    endResetModel();
}

bool MidiPortModel::connectPorts(MidiClientPortId srcId, MidiClientPortId destId, bool connected)
{
#ifdef Q_OS_LINUX
    snd_seq_addr_t sender, dest;
    snd_seq_port_subscribe_t* subs;
    snd_seq_port_subscribe_alloca(&subs);

    sender.client = static_cast<unsigned char>(srcId.clientId());
    sender.port = static_cast<unsigned char>(srcId.portId());
    dest.client = static_cast<unsigned char>(destId.clientId());
    dest.port = static_cast<unsigned char>(destId.portId());

    snd_seq_port_subscribe_set_sender(subs, &sender);
    snd_seq_port_subscribe_set_dest(subs, &dest);
#endif
#ifdef Q_OS_WIN
    MMRESULT retval;
#endif

    if(connected)
    {
        if(direction == ReadablePorts)
        {
            if(connectionsCont.contains(srcId))
                return true;
#ifdef Q_OS_WIN
            HMIDIIN hmidiin;
            retval = midiInOpen(&hmidiin, srcId, (DWORD_PTR)(void *)MidiInProc, (DWORD_PTR)(void *)this, CALLBACK_FUNCTION);
            if (retval == MMSYSERR_NOERROR)
            {
                for( int i = 0; i< inBufferCount; i++)
                {
                    LPMIDIHDR hdr = (LPMIDIHDR) malloc(sizeof(MIDIHDR));
                    hdr->dwBufferLength = inBufferSize;
                    hdr->lpData = (LPSTR) malloc(inBufferSize);
                    hdr->dwFlags = 0;
                    midiInPrepareHeader(hmidiin, hdr, sizeof(MIDIHDR));
                    midiInAddBuffer(hmidiin, hdr, sizeof(MIDIHDR));
                    inHeaderMap.insert(hmidiin, hdr);
                }
                midiInStart(hmidiin);
                connectionsCont.insert(srcId, hmidiin);
            }
#else
            connectionsCont.insert(srcId);
#endif
            emitPortChanged(srcId);
        }
        else
        {
            if(connectionsCont.contains(destId))
                return true;
#ifdef Q_OS_WIN
            HMIDIOUT hmidiout;
            retval = midiOutOpen(&hmidiout, destId, 0, 0, CALLBACK_NULL);
            if (retval == MMSYSERR_NOERROR)
            {
                connectionsCont.insert(destId, hmidiout);
            }
#else
           connectionsCont.insert(destId);
#endif
           emitPortChanged(destId);
        }
#ifdef Q_OS_LINUX
        return(snd_seq_subscribe_port(handle, subs) == 0);
#endif
#ifdef Q_OS_MACOS
        //return( MIDIPortConnectSource(destId, srcId, nullptr) == kAudioServicesNoError);
        MIDIPortConnectSource(destId, srcId, nullptr);
        return true;
#endif
    }
    else
    {
        if(direction == ReadablePorts)
        {
            if(! connectionsCont.contains(srcId))
                return true;
#ifdef Q_OS_WIN
            HMIDIIN hmidiin = (HMIDIIN)connectionsCont.value(srcId);
            midiInStop(hmidiin);
            midiInReset(hmidiin);
            QList<LPMIDIHDR> midiheaderList = inHeaderMap.values(hmidiin);
            for (int i = 0; i < midiheaderList.size(); ++i)
            {
                free(midiheaderList[i]->lpData);
                inHeaderMap.remove(hmidiin, midiheaderList[i]);
                free(midiheaderList[i]);
            }
            retval = midiInClose(hmidiin);
#endif
            connectionsCont.remove(srcId);
            emitPortChanged(srcId);
        }
        else
        {
            if(! connectionsCont.contains(destId))
                return true;
#ifdef Q_OS_WIN
            retval = midiOutClose((HMIDIOUT)connectionsCont.value(destId));
#endif
            connectionsCont.remove(destId);
            emitPortChanged(destId);
        }
#ifdef Q_OS_LINUX
        return(snd_seq_unsubscribe_port(handle, subs)==0);
#endif
#ifdef Q_OS_MACOS
        return(MIDIPortDisconnectSource( srcId, destId) == kAudioServicesNoError);
#endif
    }
#ifdef Q_OS_WIN
    return retval == MMSYSERR_NOERROR;
#endif
}

bool MidiPortModel::connectPortsByName(const QString &srcName, MidiClientPortId destId, bool connected)
{
    for(int i=0; i<portList.size(); i++)
    {
        if(portList.at(i).second == srcName)
            return connectPorts(portList.at(i).first, destId, connected);
    }
    return false;
}

bool MidiPortModel::connectPortsByName(MidiClientPortId srcId, const QString &destName, bool connected)
{
    for(int i=0; i<portList.size(); i++)
    {
        if(portList.at(i).second == destName)
            return connectPorts(srcId, portList.at(i).first, connected);
    }
    return false;
}

void MidiPortModel::emitPortChanged(MidiClientPortId id)
{
    int row;
    for(row=0; row<portList.size(); row++)
    {
        if( portList.at(row).first == id)
            break;
    }
    if(row < portList.size())
    {
        emit dataChanged( index(row,0), index(row,0));
    }
}

#ifdef Q_OS_WIN
bool MidiPortModel::event(QEvent *e)
{
    InMidiHeaderUsedEvent *me = dynamic_cast<InMidiHeaderUsedEvent *>(e);
    if(me)
    {
        QMultiMap<void *, LPMIDIHDR>::const_iterator iter = inHeaderMap.find( me->Handle(), me->midiHeader());
        Q_ASSERT( iter != inHeaderMap.constEnd());
        midiInAddBuffer((HMIDIIN)iter.key(), iter.value(), sizeof(MIDIHDR));
        me->accept();
        return true;
    }
    return MidiPortModel::event(e);
}
#endif

QStringList MidiPortModel::currentConnectionsNameList() const
{
    QStringList strList;
    for(int i=0; i<portList.size(); i++)
    {
        if( connectionsCont.contains(portList.at(i).first))
            strList.append( portList.at(i).second);
    }
    return strList;
}

QModelIndex MidiPortModel::index(int row, int column, const QModelIndex &parent) const
{
    Q_UNUSED(parent)
    return createIndex( row, column);
}

QModelIndex MidiPortModel::parent(const QModelIndex &child) const
{
    Q_UNUSED(child)
    return QModelIndex();
}
