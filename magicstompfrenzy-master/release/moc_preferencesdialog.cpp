/****************************************************************************
** Meta object code from reading C++ file 'preferencesdialog.h'
**
** Created by: The Qt Meta Object Compiler version 69 (Qt 6.9.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../preferencesdialog.h"
#include <QtCore/qmetatype.h>
#include <QtCore/QList>

#include <QtCore/qtmochelpers.h>

#include <memory>


#include <QtCore/qxptype_traits.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'preferencesdialog.h' doesn't include <QObject>."
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
struct qt_meta_tag_ZN17PreferencesDialogE_t {};
} // unnamed namespace

template <> constexpr inline auto PreferencesDialog::qt_create_metaobjectdata<qt_meta_tag_ZN17PreferencesDialogE_t>()
{
    namespace QMC = QtMocConstants;
    QtMocHelpers::StringRefStorage qt_stringData {
        "PreferencesDialog",
        "midiInPortStatusChanged",
        "",
        "MidiClientPortId",
        "portId",
        "isSelected",
        "midiOutPortStatusChanged",
        "midiChannelChanged",
        "channel",
        "paramToCCChanged",
        "name",
        "newCCNUmber",
        "oldCCNumber",
        "midiInselectionChanged",
        "QItemSelection",
        "selected",
        "deselected",
        "midiOutselectionChanged",
        "portsInModelDataChanged",
        "QModelIndex",
        "topLeft",
        "bottomRight",
        "QList<int>",
        "roles",
        "portsOutModelDataChanged",
        "paraCCSpinBoxValueChanged",
        "val",
        "paraCCModeComboBoxValueChanged",
        "paraCCInitModeComboBoxValueChanged"
    };

    QtMocHelpers::UintData qt_methods {
        // Signal 'midiInPortStatusChanged'
        QtMocHelpers::SignalData<void(MidiClientPortId, bool)>(1, 2, QMC::AccessPublic, QMetaType::Void, {{
            { 0x80000000 | 3, 4 }, { QMetaType::Bool, 5 },
        }}),
        // Signal 'midiOutPortStatusChanged'
        QtMocHelpers::SignalData<void(MidiClientPortId, bool)>(6, 2, QMC::AccessPublic, QMetaType::Void, {{
            { 0x80000000 | 3, 4 }, { QMetaType::Bool, 5 },
        }}),
        // Signal 'midiChannelChanged'
        QtMocHelpers::SignalData<void(int)>(7, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::Int, 8 },
        }}),
        // Signal 'paramToCCChanged'
        QtMocHelpers::SignalData<void(const QString &, int, int)>(9, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 10 }, { QMetaType::Int, 11 }, { QMetaType::Int, 12 },
        }}),
        // Slot 'midiInselectionChanged'
        QtMocHelpers::SlotData<void(const QItemSelection &, const QItemSelection &)>(13, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { 0x80000000 | 14, 15 }, { 0x80000000 | 14, 16 },
        }}),
        // Slot 'midiOutselectionChanged'
        QtMocHelpers::SlotData<void(const QItemSelection &, const QItemSelection &)>(17, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { 0x80000000 | 14, 15 }, { 0x80000000 | 14, 16 },
        }}),
        // Slot 'portsInModelDataChanged'
        QtMocHelpers::SlotData<void(const QModelIndex &, const QModelIndex &, const QVector<int> &)>(18, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { 0x80000000 | 19, 20 }, { 0x80000000 | 19, 21 }, { 0x80000000 | 22, 23 },
        }}),
        // Slot 'portsInModelDataChanged'
        QtMocHelpers::SlotData<void(const QModelIndex &, const QModelIndex &)>(18, 2, QMC::AccessPrivate | QMC::MethodCloned, QMetaType::Void, {{
            { 0x80000000 | 19, 20 }, { 0x80000000 | 19, 21 },
        }}),
        // Slot 'portsOutModelDataChanged'
        QtMocHelpers::SlotData<void(const QModelIndex &, const QModelIndex &, const QVector<int> &)>(24, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { 0x80000000 | 19, 20 }, { 0x80000000 | 19, 21 }, { 0x80000000 | 22, 23 },
        }}),
        // Slot 'portsOutModelDataChanged'
        QtMocHelpers::SlotData<void(const QModelIndex &, const QModelIndex &)>(24, 2, QMC::AccessPrivate | QMC::MethodCloned, QMetaType::Void, {{
            { 0x80000000 | 19, 20 }, { 0x80000000 | 19, 21 },
        }}),
        // Slot 'paraCCSpinBoxValueChanged'
        QtMocHelpers::SlotData<void(int)>(25, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Int, 26 },
        }}),
        // Slot 'paraCCModeComboBoxValueChanged'
        QtMocHelpers::SlotData<void(int)>(27, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Int, 26 },
        }}),
        // Slot 'paraCCInitModeComboBoxValueChanged'
        QtMocHelpers::SlotData<void(int)>(28, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Int, 26 },
        }}),
    };
    QtMocHelpers::UintData qt_properties {
    };
    QtMocHelpers::UintData qt_enums {
    };
    return QtMocHelpers::metaObjectData<PreferencesDialog, qt_meta_tag_ZN17PreferencesDialogE_t>(QMC::MetaObjectFlag{}, qt_stringData,
            qt_methods, qt_properties, qt_enums);
}
Q_CONSTINIT const QMetaObject PreferencesDialog::staticMetaObject = { {
    QMetaObject::SuperData::link<QDialog::staticMetaObject>(),
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN17PreferencesDialogE_t>.stringdata,
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN17PreferencesDialogE_t>.data,
    qt_static_metacall,
    nullptr,
    qt_staticMetaObjectRelocatingContent<qt_meta_tag_ZN17PreferencesDialogE_t>.metaTypes,
    nullptr
} };

void PreferencesDialog::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    auto *_t = static_cast<PreferencesDialog *>(_o);
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: _t->midiInPortStatusChanged((*reinterpret_cast< std::add_pointer_t<MidiClientPortId>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<bool>>(_a[2]))); break;
        case 1: _t->midiOutPortStatusChanged((*reinterpret_cast< std::add_pointer_t<MidiClientPortId>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<bool>>(_a[2]))); break;
        case 2: _t->midiChannelChanged((*reinterpret_cast< std::add_pointer_t<int>>(_a[1]))); break;
        case 3: _t->paramToCCChanged((*reinterpret_cast< std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<int>>(_a[2])),(*reinterpret_cast< std::add_pointer_t<int>>(_a[3]))); break;
        case 4: _t->midiInselectionChanged((*reinterpret_cast< std::add_pointer_t<QItemSelection>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<QItemSelection>>(_a[2]))); break;
        case 5: _t->midiOutselectionChanged((*reinterpret_cast< std::add_pointer_t<QItemSelection>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<QItemSelection>>(_a[2]))); break;
        case 6: _t->portsInModelDataChanged((*reinterpret_cast< std::add_pointer_t<QModelIndex>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<QModelIndex>>(_a[2])),(*reinterpret_cast< std::add_pointer_t<QList<int>>>(_a[3]))); break;
        case 7: _t->portsInModelDataChanged((*reinterpret_cast< std::add_pointer_t<QModelIndex>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<QModelIndex>>(_a[2]))); break;
        case 8: _t->portsOutModelDataChanged((*reinterpret_cast< std::add_pointer_t<QModelIndex>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<QModelIndex>>(_a[2])),(*reinterpret_cast< std::add_pointer_t<QList<int>>>(_a[3]))); break;
        case 9: _t->portsOutModelDataChanged((*reinterpret_cast< std::add_pointer_t<QModelIndex>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<QModelIndex>>(_a[2]))); break;
        case 10: _t->paraCCSpinBoxValueChanged((*reinterpret_cast< std::add_pointer_t<int>>(_a[1]))); break;
        case 11: _t->paraCCModeComboBoxValueChanged((*reinterpret_cast< std::add_pointer_t<int>>(_a[1]))); break;
        case 12: _t->paraCCInitModeComboBoxValueChanged((*reinterpret_cast< std::add_pointer_t<int>>(_a[1]))); break;
        default: ;
        }
    }
    if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        switch (_id) {
        default: *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType(); break;
        case 6:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType(); break;
            case 2:
                *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType::fromType< QList<int> >(); break;
            }
            break;
        case 8:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType(); break;
            case 2:
                *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType::fromType< QList<int> >(); break;
            }
            break;
        }
    }
    if (_c == QMetaObject::IndexOfMethod) {
        if (QtMocHelpers::indexOfMethod<void (PreferencesDialog::*)(MidiClientPortId , bool )>(_a, &PreferencesDialog::midiInPortStatusChanged, 0))
            return;
        if (QtMocHelpers::indexOfMethod<void (PreferencesDialog::*)(MidiClientPortId , bool )>(_a, &PreferencesDialog::midiOutPortStatusChanged, 1))
            return;
        if (QtMocHelpers::indexOfMethod<void (PreferencesDialog::*)(int )>(_a, &PreferencesDialog::midiChannelChanged, 2))
            return;
        if (QtMocHelpers::indexOfMethod<void (PreferencesDialog::*)(const QString & , int , int )>(_a, &PreferencesDialog::paramToCCChanged, 3))
            return;
    }
}

const QMetaObject *PreferencesDialog::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *PreferencesDialog::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_staticMetaObjectStaticContent<qt_meta_tag_ZN17PreferencesDialogE_t>.strings))
        return static_cast<void*>(this);
    return QDialog::qt_metacast(_clname);
}

int PreferencesDialog::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QDialog::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 13)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 13;
    }
    if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 13)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 13;
    }
    return _id;
}

// SIGNAL 0
void PreferencesDialog::midiInPortStatusChanged(MidiClientPortId _t1, bool _t2)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 0, nullptr, _t1, _t2);
}

// SIGNAL 1
void PreferencesDialog::midiOutPortStatusChanged(MidiClientPortId _t1, bool _t2)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 1, nullptr, _t1, _t2);
}

// SIGNAL 2
void PreferencesDialog::midiChannelChanged(int _t1)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 2, nullptr, _t1);
}

// SIGNAL 3
void PreferencesDialog::paramToCCChanged(const QString & _t1, int _t2, int _t3)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 3, nullptr, _t1, _t2, _t3);
}
QT_WARNING_POP
