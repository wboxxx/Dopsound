/****************************************************************************
** Meta object code from reading C++ file 'midiportmodel.h'
**
** Created by: The Qt Meta Object Compiler version 69 (Qt 6.9.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../midiportmodel.h"
#include <QtCore/qmetatype.h>

#include <QtCore/qtmochelpers.h>

#include <memory>


#include <QtCore/qxptype_traits.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'midiportmodel.h' doesn't include <QObject>."
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
struct qt_meta_tag_ZN13MidiPortModelE_t {};
} // unnamed namespace

template <> constexpr inline auto MidiPortModel::qt_create_metaobjectdata<qt_meta_tag_ZN13MidiPortModelE_t>()
{
    namespace QMC = QtMocConstants;
    QtMocHelpers::StringRefStorage qt_stringData {
        "MidiPortModel",
        "scan",
        "",
        "connectPorts",
        "MidiClientPortId",
        "src",
        "dest",
        "connected",
        "connectPortsByName",
        "srcName",
        "destId",
        "srcId",
        "destName"
    };

    QtMocHelpers::UintData qt_methods {
        // Slot 'scan'
        QtMocHelpers::SlotData<void()>(1, 2, QMC::AccessPublic, QMetaType::Void),
        // Slot 'connectPorts'
        QtMocHelpers::SlotData<bool(MidiClientPortId, MidiClientPortId, bool)>(3, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { 0x80000000 | 4, 5 }, { 0x80000000 | 4, 6 }, { QMetaType::Bool, 7 },
        }}),
        // Slot 'connectPortsByName'
        QtMocHelpers::SlotData<bool(const QString &, MidiClientPortId, bool)>(8, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 9 }, { 0x80000000 | 4, 10 }, { QMetaType::Bool, 7 },
        }}),
        // Slot 'connectPortsByName'
        QtMocHelpers::SlotData<bool(MidiClientPortId, const QString &, bool)>(8, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { 0x80000000 | 4, 11 }, { QMetaType::QString, 12 }, { QMetaType::Bool, 7 },
        }}),
    };
    QtMocHelpers::UintData qt_properties {
    };
    QtMocHelpers::UintData qt_enums {
    };
    return QtMocHelpers::metaObjectData<MidiPortModel, qt_meta_tag_ZN13MidiPortModelE_t>(QMC::MetaObjectFlag{}, qt_stringData,
            qt_methods, qt_properties, qt_enums);
}
Q_CONSTINIT const QMetaObject MidiPortModel::staticMetaObject = { {
    QMetaObject::SuperData::link<QAbstractItemModel::staticMetaObject>(),
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN13MidiPortModelE_t>.stringdata,
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN13MidiPortModelE_t>.data,
    qt_static_metacall,
    nullptr,
    qt_staticMetaObjectRelocatingContent<qt_meta_tag_ZN13MidiPortModelE_t>.metaTypes,
    nullptr
} };

void MidiPortModel::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    auto *_t = static_cast<MidiPortModel *>(_o);
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: _t->scan(); break;
        case 1: { bool _r = _t->connectPorts((*reinterpret_cast< std::add_pointer_t<MidiClientPortId>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<MidiClientPortId>>(_a[2])),(*reinterpret_cast< std::add_pointer_t<bool>>(_a[3])));
            if (_a[0]) *reinterpret_cast< bool*>(_a[0]) = std::move(_r); }  break;
        case 2: { bool _r = _t->connectPortsByName((*reinterpret_cast< std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<MidiClientPortId>>(_a[2])),(*reinterpret_cast< std::add_pointer_t<bool>>(_a[3])));
            if (_a[0]) *reinterpret_cast< bool*>(_a[0]) = std::move(_r); }  break;
        case 3: { bool _r = _t->connectPortsByName((*reinterpret_cast< std::add_pointer_t<MidiClientPortId>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<QString>>(_a[2])),(*reinterpret_cast< std::add_pointer_t<bool>>(_a[3])));
            if (_a[0]) *reinterpret_cast< bool*>(_a[0]) = std::move(_r); }  break;
        default: ;
        }
    }
}

const QMetaObject *MidiPortModel::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *MidiPortModel::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_staticMetaObjectStaticContent<qt_meta_tag_ZN13MidiPortModelE_t>.strings))
        return static_cast<void*>(this);
    return QAbstractItemModel::qt_metacast(_clname);
}

int MidiPortModel::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QAbstractItemModel::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 4)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 4;
    }
    if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 4)
            *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType();
        _id -= 4;
    }
    return _id;
}
QT_WARNING_POP
