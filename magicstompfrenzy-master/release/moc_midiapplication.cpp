/****************************************************************************
** Meta object code from reading C++ file 'midiapplication.h'
**
** Created by: The Qt Meta Object Compiler version 69 (Qt 6.9.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../midiapplication.h"
#include <QtCore/qmetatype.h>

#include <QtCore/qtmochelpers.h>

#include <memory>


#include <QtCore/qxptype_traits.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'midiapplication.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 69
#error "This file was generated using the moc from 6.9.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

#ifndef Q_CONSTINIT
#define Q_CONSTINIT
#endif

QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
QT_WARNING_DISABLE_GCC("-Wuseless-cast")
namespace {
struct qt_meta_tag_ZN15MidiApplicationE_t {};
} // unnamed namespace

template <> constexpr inline auto MidiApplication::qt_create_metaobjectdata<qt_meta_tag_ZN15MidiApplicationE_t>()
{
    namespace QMC = QtMocConstants;
    QtMocHelpers::StringRefStorage qt_stringData {
        "MidiApplication",
        "midiEventReceived",
        "",
        "MidiEvent*",
        "changeReadableMidiPortStatus",
        "MidiClientPortId",
        "mcpId",
        "connect",
        "changeWritebleMidiPortStatus",
        "portName",
        "sendMidiEvent",
        "ev",
        "onPortConnectionStatusChanged",
        "srcId",
        "destId",
        "isConnected",
        "onPortClientPortStatusChanged",
        "mpId",
        "isExisting",
        "isQuitting"
    };

    QtMocHelpers::UintData qt_methods {
        // Signal 'midiEventReceived'
        QtMocHelpers::SignalData<void(MidiEvent *)>(1, 2, QMC::AccessPublic, QMetaType::Void, {{
            { 0x80000000 | 3, 2 },
        }}),
        // Slot 'changeReadableMidiPortStatus'
        QtMocHelpers::SlotData<bool(MidiClientPortId, bool)>(4, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { 0x80000000 | 5, 6 }, { QMetaType::Bool, 7 },
        }}),
        // Slot 'changeWritebleMidiPortStatus'
        QtMocHelpers::SlotData<bool(MidiClientPortId, bool)>(8, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { 0x80000000 | 5, 6 }, { QMetaType::Bool, 7 },
        }}),
        // Slot 'changeReadableMidiPortStatus'
        QtMocHelpers::SlotData<bool(const QString &, bool)>(4, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 9 }, { QMetaType::Bool, 7 },
        }}),
        // Slot 'changeWritebleMidiPortStatus'
        QtMocHelpers::SlotData<bool(const QString &, bool)>(8, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 9 }, { QMetaType::Bool, 7 },
        }}),
        // Slot 'sendMidiEvent'
        QtMocHelpers::SlotData<bool(MidiEvent *)>(10, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { 0x80000000 | 3, 11 },
        }}),
        // Slot 'onPortConnectionStatusChanged'
        QtMocHelpers::SlotData<void(MidiClientPortId, MidiClientPortId, bool)>(12, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { 0x80000000 | 5, 13 }, { 0x80000000 | 5, 14 }, { QMetaType::Bool, 15 },
        }}),
        // Slot 'onPortClientPortStatusChanged'
        QtMocHelpers::SlotData<void(MidiClientPortId, bool)>(16, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { 0x80000000 | 5, 17 }, { QMetaType::Bool, 18 },
        }}),
        // Slot 'isQuitting'
        QtMocHelpers::SlotData<void()>(19, 2, QMC::AccessPrivate, QMetaType::Void),
    };
    QtMocHelpers::UintData qt_properties {
    };
    QtMocHelpers::UintData qt_enums {
    };
    return QtMocHelpers::metaObjectData<MidiApplication, qt_meta_tag_ZN15MidiApplicationE_t>(QMC::MetaObjectFlag{}, qt_stringData,
            qt_methods, qt_properties, qt_enums);
}
Q_CONSTINIT const QMetaObject MidiApplication::staticMetaObject = { {
    QMetaObject::SuperData::link<QApplication::staticMetaObject>(),
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN15MidiApplicationE_t>.stringdata,
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN15MidiApplicationE_t>.data,
    qt_static_metacall,
    nullptr,
    qt_staticMetaObjectRelocatingContent<qt_meta_tag_ZN15MidiApplicationE_t>.metaTypes,
    nullptr
} };

void MidiApplication::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    auto *_t = static_cast<MidiApplication *>(_o);
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: _t->midiEventReceived((*reinterpret_cast< std::add_pointer_t<MidiEvent*>>(_a[1]))); break;
        case 1: { bool _r = _t->changeReadableMidiPortStatus((*reinterpret_cast< std::add_pointer_t<MidiClientPortId>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<bool>>(_a[2])));
            if (_a[0]) *reinterpret_cast< bool*>(_a[0]) = std::move(_r); }  break;
        case 2: { bool _r = _t->changeWritebleMidiPortStatus((*reinterpret_cast< std::add_pointer_t<MidiClientPortId>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<bool>>(_a[2])));
            if (_a[0]) *reinterpret_cast< bool*>(_a[0]) = std::move(_r); }  break;
        case 3: { bool _r = _t->changeReadableMidiPortStatus((*reinterpret_cast< std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<bool>>(_a[2])));
            if (_a[0]) *reinterpret_cast< bool*>(_a[0]) = std::move(_r); }  break;
        case 4: { bool _r = _t->changeWritebleMidiPortStatus((*reinterpret_cast< std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<bool>>(_a[2])));
            if (_a[0]) *reinterpret_cast< bool*>(_a[0]) = std::move(_r); }  break;
        case 5: { bool _r = _t->sendMidiEvent((*reinterpret_cast< std::add_pointer_t<MidiEvent*>>(_a[1])));
            if (_a[0]) *reinterpret_cast< bool*>(_a[0]) = std::move(_r); }  break;
        case 6: _t->onPortConnectionStatusChanged((*reinterpret_cast< std::add_pointer_t<MidiClientPortId>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<MidiClientPortId>>(_a[2])),(*reinterpret_cast< std::add_pointer_t<bool>>(_a[3]))); break;
        case 7: _t->onPortClientPortStatusChanged((*reinterpret_cast< std::add_pointer_t<MidiClientPortId>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<bool>>(_a[2]))); break;
        case 8: _t->isQuitting(); break;
        default: ;
        }
    }
    if (_c == QMetaObject::IndexOfMethod) {
        if (QtMocHelpers::indexOfMethod<void (MidiApplication::*)(MidiEvent * )>(_a, &MidiApplication::midiEventReceived, 0))
            return;
    }
}

const QMetaObject *MidiApplication::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *MidiApplication::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_staticMetaObjectStaticContent<qt_meta_tag_ZN15MidiApplicationE_t>.strings))
        return static_cast<void*>(this);
    return QApplication::qt_metacast(_clname);
}

int MidiApplication::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QApplication::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 9)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 9;
    }
    if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 9)
            *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType();
        _id -= 9;
    }
    return _id;
}

// SIGNAL 0
void MidiApplication::midiEventReceived(MidiEvent * _t1)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 0, nullptr, _t1);
}
QT_WARNING_POP
