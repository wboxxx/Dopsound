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
#include "midisender.h"

#include "midievent.h"

#ifdef Q_OS_LINUX
#include <alsa/asoundlib.h>


#include <QApplication>
#include <QThread>
#include <QDebug>
#include <QDateTime>
#include <QTextStream>

#include <QCoreApplication>

void MidiSender::hexDump(const QByteArray &data, const QString &paramName, int offset, int length)
{
    if (data.isEmpty())
        return;
        
    // Get current timestamp
    QString timestamp = QDateTime::currentDateTime().toString("[yyyy-MM-dd hh:mm:ss]");
    
    // Format hex bytes with space separation
    QString hexString;
    QTextStream stream(&hexString);
    for (int i = 0; i < data.size(); ++i) {
        stream << QString("%1").arg(static_cast<unsigned char>(data[i]), 2, 16, QChar('0')).toUpper();
        if (i < data.size() - 1) {
            stream << " ";
        }
    }
    
    // Output to both console and file for debugging
    QString logMessage = timestamp + " SYSEX OUT len=" + QString::number(data.size());
    
    // Add parameter information if available
    if (!paramName.isEmpty()) {
        logMessage += " | PARAM: " + paramName;
        if (offset >= 0) {
            logMessage += " (offset=" + QString::number(offset);
            if (length > 0) {
                logMessage += ", len=" + QString::number(length);
            }
            logMessage += ")";
        }
    }
    
    logMessage += "  " + hexString + "\n";
    
    // Write to console
    QTextStream(stdout) << logMessage;
    QTextStream(stdout).flush();
    
    // Write to file
    QFile logFile("sysex_debug.log");
    if (logFile.open(QIODevice::WriteOnly | QIODevice::Append)) {
        QTextStream fileStream(&logFile);
        fileStream << logMessage;
        fileStream.flush();
        logFile.close();
    }
}

bool MidiSender::event(QEvent *e)
{

    MidiEvent *me = dynamic_cast<MidiEvent *>(e);
    if(me && me->type()==static_cast<QEvent::Type>(UserEventTypes::MidiSysEx))
    {
        snd_seq_event_t ev;
        snd_seq_ev_clear(&ev);
        snd_seq_ev_set_source(&ev, outport.portId());
        snd_seq_ev_set_subs(&ev);
        snd_seq_ev_set_direct(&ev);

        snd_seq_ev_set_variable(&ev, me->sysExData()->size(), (void * )me->sysExData()->constData() );
        ev.type=SND_SEQ_EVENT_SYSEX;

        // Log SysEx message before sending (without parameter info since it's not available here)
        hexDump(*me->sysExData());

        int ret;

        ret = snd_seq_event_output(handle, &ev);
        if(ret < 0)
        {
            qDebug() << "Error at snd_seq_event_output";
        }
        ret = snd_seq_drain_output(handle);
        if(ret < 0)
        {
            qDebug() << "Error at snd_seq_drain_output";
        }
        me->accept();
    }

    return true;
}
#endif
