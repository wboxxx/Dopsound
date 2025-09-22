/****************************************************************************
** Meta object code from reading C++ file 'reverbtimespinbox.h'
**
** Created by: The Qt Meta Object Compiler version 69 (Qt 6.9.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../effecteditwidgets/reverbtimespinbox.h"
#include <QtCore/qmetatype.h>

#include <QtCore/qtmochelpers.h>

#include <memory>


#include <QtCore/qxptype_traits.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'reverbtimespinbox.h' doesn't include <QObject>."
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
struct qt_meta_tag_ZN17ReverbTimeSpinBoxE_t {};
} // unnamed namespace

template <> constexpr inline auto ReverbTimeSpinBox::qt_create_metaobjectdata<qt_meta_tag_ZN17ReverbTimeSpinBoxE_t>()
{
    namespace QMC = QtMocConstants;
    QtMocHelpers::StringRefStorage qt_stringData {
        "ReverbTimeSpinBox",
        "rawValueChanged",
        "",
        "rawValue"
    };

    QtMocHelpers::UintData qt_methods {
        // Signal 'rawValueChanged'
        QtMocHelpers::SignalData<void(int)>(1, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::Int, 2 },
        }}),
    };
    QtMocHelpers::UintData qt_properties {
        // property 'rawValue'
        QtMocHelpers::PropertyData<int>(3, QMetaType::Int, QMC::DefaultPropertyFlags | QMC::Writable | QMC::StdCppSet | QMC::User, 0),
    };
    QtMocHelpers::UintData qt_enums {
    };
    return QtMocHelpers::metaObjectData<ReverbTimeSpinBox, qt_meta_tag_ZN17ReverbTimeSpinBoxE_t>(QMC::MetaObjectFlag{}, qt_stringData,
            qt_methods, qt_properties, qt_enums);
}
Q_CONSTINIT const QMetaObject ReverbTimeSpinBox::staticMetaObject = { {
    QMetaObject::SuperData::link<QAbstractSpinBox::staticMetaObject>(),
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN17ReverbTimeSpinBoxE_t>.stringdata,
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN17ReverbTimeSpinBoxE_t>.data,
    qt_static_metacall,
    nullptr,
    qt_staticMetaObjectRelocatingContent<qt_meta_tag_ZN17ReverbTimeSpinBoxE_t>.metaTypes,
    nullptr
} };

void ReverbTimeSpinBox::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    auto *_t = static_cast<ReverbTimeSpinBox *>(_o);
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: _t->rawValueChanged((*reinterpret_cast< std::add_pointer_t<int>>(_a[1]))); break;
        default: ;
        }
    }
    if (_c == QMetaObject::IndexOfMethod) {
        if (QtMocHelpers::indexOfMethod<void (ReverbTimeSpinBox::*)(int )>(_a, &ReverbTimeSpinBox::rawValueChanged, 0))
            return;
    }
    if (_c == QMetaObject::ReadProperty) {
        void *_v = _a[0];
        switch (_id) {
        case 0: *reinterpret_cast<int*>(_v) = _t->RawValue(); break;
        default: break;
        }
    }
    if (_c == QMetaObject::WriteProperty) {
        void *_v = _a[0];
        switch (_id) {
        case 0: _t->setRawValue(*reinterpret_cast<int*>(_v)); break;
        default: break;
        }
    }
}

const QMetaObject *ReverbTimeSpinBox::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *ReverbTimeSpinBox::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_staticMetaObjectStaticContent<qt_meta_tag_ZN17ReverbTimeSpinBoxE_t>.strings))
        return static_cast<void*>(this);
    return QAbstractSpinBox::qt_metacast(_clname);
}

int ReverbTimeSpinBox::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QAbstractSpinBox::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 1)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 1;
    }
    if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 1)
            *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType();
        _id -= 1;
    }
    if (_c == QMetaObject::ReadProperty || _c == QMetaObject::WriteProperty
            || _c == QMetaObject::ResetProperty || _c == QMetaObject::BindableProperty
            || _c == QMetaObject::RegisterPropertyMetaType) {
        qt_static_metacall(this, _c, _id, _a);
        _id -= 1;
    }
    return _id;
}

// SIGNAL 0
void ReverbTimeSpinBox::rawValueChanged(int _t1)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 0, nullptr, _t1);
}
QT_WARNING_POP
