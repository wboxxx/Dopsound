/****************************************************************************
** Meta object code from reading C++ file 'mainwindow.h'
**
** Created by: The Qt Meta Object Compiler version 69 (Qt 6.9.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../mainwindow.h"
#include <QtCore/qmetatype.h>

#include <QtCore/qtmochelpers.h>

#include <memory>


#include <QtCore/qxptype_traits.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'mainwindow.h' doesn't include <QObject>."
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
struct qt_meta_tag_ZN10MainWindowE_t {};
} // unnamed namespace

template <> constexpr inline auto MainWindow::qt_create_metaobjectdata<qt_meta_tag_ZN10MainWindowE_t>()
{
    namespace QMC = QtMocConstants;
    QtMocHelpers::StringRefStorage qt_stringData {
        "MainWindow",
        "midiEvent",
        "",
        "MidiEvent*",
        "event",
        "importSMF",
        "fileName",
        "PatchListType",
        "type",
        "importUB99",
        "hideEditor",
        "restoreSettings",
        "requestAll",
        "sendAll",
        "startMidiOutTimer",
        "requestPatch",
        "patchIndex",
        "sendPatch",
        "sendToTmpArea",
        "parameterToBeChanged",
        "offset",
        "length",
        "QWidget*",
        "editWidget",
        "parameterChanged",
        "timeout",
        "midiOutTimeOut",
        "cancelTransmission",
        "patchListDoubleClicked",
        "QModelIndex",
        "idx",
        "patchListSelectionChanged",
        "putGuiToTransmissionState",
        "isTransmitting",
        "sending",
        "swapButtonPressed",
        "copyButtonPressed",
        "undoRedoButtonPressed",
        "showPreferences",
        "saveSettings",
        "setMIDIChannel",
        "val",
        "onImport",
        "onExport",
        "onPatchTypeEditorChanged",
        "typeId",
        "onParamToCCChaged",
        "name",
        "newVal",
        "oldVal"
    };

    QtMocHelpers::UintData qt_methods {
        // Slot 'midiEvent'
        QtMocHelpers::SlotData<void(MidiEvent *)>(1, 2, QMC::AccessPublic, QMetaType::Void, {{
            { 0x80000000 | 3, 4 },
        }}),
        // Slot 'importSMF'
        QtMocHelpers::SlotData<bool(const QString &, enum PatchListType)>(5, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 6 }, { 0x80000000 | 7, 8 },
        }}),
        // Slot 'importUB99'
        QtMocHelpers::SlotData<bool(const QString &, enum PatchListType)>(9, 2, QMC::AccessPublic, QMetaType::Bool, {{
            { QMetaType::QString, 6 }, { 0x80000000 | 7, 8 },
        }}),
        // Slot 'hideEditor'
        QtMocHelpers::SlotData<void()>(10, 2, QMC::AccessPublic, QMetaType::Void),
        // Slot 'restoreSettings'
        QtMocHelpers::SlotData<void()>(11, 2, QMC::AccessPublic, QMetaType::Void),
        // Slot 'requestAll'
        QtMocHelpers::SlotData<void()>(12, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'sendAll'
        QtMocHelpers::SlotData<void(bool)>(13, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Bool, 14 },
        }}),
        // Slot 'sendAll'
        QtMocHelpers::SlotData<void()>(13, 2, QMC::AccessPrivate | QMC::MethodCloned, QMetaType::Void),
        // Slot 'requestPatch'
        QtMocHelpers::SlotData<void(int)>(15, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Int, 16 },
        }}),
        // Slot 'sendPatch'
        QtMocHelpers::SlotData<void(int, bool, enum PatchListType, bool)>(17, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Int, 16 }, { QMetaType::Bool, 18 }, { 0x80000000 | 7, 8 }, { QMetaType::Bool, 14 },
        }}),
        // Slot 'sendPatch'
        QtMocHelpers::SlotData<void(int, bool, enum PatchListType)>(17, 2, QMC::AccessPrivate | QMC::MethodCloned, QMetaType::Void, {{
            { QMetaType::Int, 16 }, { QMetaType::Bool, 18 }, { 0x80000000 | 7, 8 },
        }}),
        // Slot 'sendPatch'
        QtMocHelpers::SlotData<void(int, bool)>(17, 2, QMC::AccessPrivate | QMC::MethodCloned, QMetaType::Void, {{
            { QMetaType::Int, 16 }, { QMetaType::Bool, 18 },
        }}),
        // Slot 'sendPatch'
        QtMocHelpers::SlotData<void(int)>(17, 2, QMC::AccessPrivate | QMC::MethodCloned, QMetaType::Void, {{
            { QMetaType::Int, 16 },
        }}),
        // Slot 'parameterToBeChanged'
        QtMocHelpers::SlotData<void(int, int, QWidget *)>(19, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Int, 20 }, { QMetaType::Int, 21 }, { 0x80000000 | 22, 23 },
        }}),
        // Slot 'parameterChanged'
        QtMocHelpers::SlotData<void(int, int, QWidget *)>(24, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Int, 20 }, { QMetaType::Int, 21 }, { 0x80000000 | 22, 23 },
        }}),
        // Slot 'timeout'
        QtMocHelpers::SlotData<void()>(25, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'midiOutTimeOut'
        QtMocHelpers::SlotData<void()>(26, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'cancelTransmission'
        QtMocHelpers::SlotData<void()>(27, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'patchListDoubleClicked'
        QtMocHelpers::SlotData<void(const QModelIndex &)>(28, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { 0x80000000 | 29, 30 },
        }}),
        // Slot 'patchListSelectionChanged'
        QtMocHelpers::SlotData<void()>(31, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'putGuiToTransmissionState'
        QtMocHelpers::SlotData<void(bool, bool)>(32, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Bool, 33 }, { QMetaType::Bool, 34 },
        }}),
        // Slot 'swapButtonPressed'
        QtMocHelpers::SlotData<void()>(35, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'copyButtonPressed'
        QtMocHelpers::SlotData<void()>(36, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'undoRedoButtonPressed'
        QtMocHelpers::SlotData<void()>(37, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'showPreferences'
        QtMocHelpers::SlotData<void()>(38, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'saveSettings'
        QtMocHelpers::SlotData<void()>(39, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'setMIDIChannel'
        QtMocHelpers::SlotData<void(int)>(40, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Int, 41 },
        }}),
        // Slot 'onImport'
        QtMocHelpers::SlotData<void()>(42, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'onExport'
        QtMocHelpers::SlotData<void()>(43, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'onPatchTypeEditorChanged'
        QtMocHelpers::SlotData<void(int)>(44, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Int, 45 },
        }}),
        // Slot 'onParamToCCChaged'
        QtMocHelpers::SlotData<void(const QString &, int, int)>(46, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::QString, 47 }, { QMetaType::Int, 48 }, { QMetaType::Int, 49 },
        }}),
    };
    QtMocHelpers::UintData qt_properties {
    };
    QtMocHelpers::UintData qt_enums {
    };
    return QtMocHelpers::metaObjectData<MainWindow, qt_meta_tag_ZN10MainWindowE_t>(QMC::MetaObjectFlag{}, qt_stringData,
            qt_methods, qt_properties, qt_enums);
}
Q_CONSTINIT const QMetaObject MainWindow::staticMetaObject = { {
    QMetaObject::SuperData::link<QMainWindow::staticMetaObject>(),
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN10MainWindowE_t>.stringdata,
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN10MainWindowE_t>.data,
    qt_static_metacall,
    nullptr,
    qt_staticMetaObjectRelocatingContent<qt_meta_tag_ZN10MainWindowE_t>.metaTypes,
    nullptr
} };

void MainWindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    auto *_t = static_cast<MainWindow *>(_o);
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: _t->midiEvent((*reinterpret_cast< std::add_pointer_t<MidiEvent*>>(_a[1]))); break;
        case 1: { bool _r = _t->importSMF((*reinterpret_cast< std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<enum PatchListType>>(_a[2])));
            if (_a[0]) *reinterpret_cast< bool*>(_a[0]) = std::move(_r); }  break;
        case 2: { bool _r = _t->importUB99((*reinterpret_cast< std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<enum PatchListType>>(_a[2])));
            if (_a[0]) *reinterpret_cast< bool*>(_a[0]) = std::move(_r); }  break;
        case 3: _t->hideEditor(); break;
        case 4: _t->restoreSettings(); break;
        case 5: _t->requestAll(); break;
        case 6: _t->sendAll((*reinterpret_cast< std::add_pointer_t<bool>>(_a[1]))); break;
        case 7: _t->sendAll(); break;
        case 8: _t->requestPatch((*reinterpret_cast< std::add_pointer_t<int>>(_a[1]))); break;
        case 9: _t->sendPatch((*reinterpret_cast< std::add_pointer_t<int>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<bool>>(_a[2])),(*reinterpret_cast< std::add_pointer_t<enum PatchListType>>(_a[3])),(*reinterpret_cast< std::add_pointer_t<bool>>(_a[4]))); break;
        case 10: _t->sendPatch((*reinterpret_cast< std::add_pointer_t<int>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<bool>>(_a[2])),(*reinterpret_cast< std::add_pointer_t<enum PatchListType>>(_a[3]))); break;
        case 11: _t->sendPatch((*reinterpret_cast< std::add_pointer_t<int>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<bool>>(_a[2]))); break;
        case 12: _t->sendPatch((*reinterpret_cast< std::add_pointer_t<int>>(_a[1]))); break;
        case 13: _t->parameterToBeChanged((*reinterpret_cast< std::add_pointer_t<int>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<int>>(_a[2])),(*reinterpret_cast< std::add_pointer_t<QWidget*>>(_a[3]))); break;
        case 14: _t->parameterChanged((*reinterpret_cast< std::add_pointer_t<int>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<int>>(_a[2])),(*reinterpret_cast< std::add_pointer_t<QWidget*>>(_a[3]))); break;
        case 15: _t->timeout(); break;
        case 16: _t->midiOutTimeOut(); break;
        case 17: _t->cancelTransmission(); break;
        case 18: _t->patchListDoubleClicked((*reinterpret_cast< std::add_pointer_t<QModelIndex>>(_a[1]))); break;
        case 19: _t->patchListSelectionChanged(); break;
        case 20: _t->putGuiToTransmissionState((*reinterpret_cast< std::add_pointer_t<bool>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<bool>>(_a[2]))); break;
        case 21: _t->swapButtonPressed(); break;
        case 22: _t->copyButtonPressed(); break;
        case 23: _t->undoRedoButtonPressed(); break;
        case 24: _t->showPreferences(); break;
        case 25: _t->saveSettings(); break;
        case 26: _t->setMIDIChannel((*reinterpret_cast< std::add_pointer_t<int>>(_a[1]))); break;
        case 27: _t->onImport(); break;
        case 28: _t->onExport(); break;
        case 29: _t->onPatchTypeEditorChanged((*reinterpret_cast< std::add_pointer_t<int>>(_a[1]))); break;
        case 30: _t->onParamToCCChaged((*reinterpret_cast< std::add_pointer_t<QString>>(_a[1])),(*reinterpret_cast< std::add_pointer_t<int>>(_a[2])),(*reinterpret_cast< std::add_pointer_t<int>>(_a[3]))); break;
        default: ;
        }
    }
    if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        switch (_id) {
        default: *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType(); break;
        case 13:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType(); break;
            case 2:
                *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType::fromType< QWidget* >(); break;
            }
            break;
        case 14:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType(); break;
            case 2:
                *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType::fromType< QWidget* >(); break;
            }
            break;
        }
    }
}

const QMetaObject *MainWindow::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *MainWindow::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_staticMetaObjectStaticContent<qt_meta_tag_ZN10MainWindowE_t>.strings))
        return static_cast<void*>(this);
    return QMainWindow::qt_metacast(_clname);
}

int MainWindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QMainWindow::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 31)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 31;
    }
    if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 31)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 31;
    }
    return _id;
}
QT_WARNING_POP
