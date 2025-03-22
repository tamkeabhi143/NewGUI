QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11

# Application name and version
TARGET = SignalManager
VERSION = 1.0.0

# Define application icon
win32:RC_ICONS += Cfg/Icons/app_icon.ico
macx:ICON = Cfg/Icons/app_icon.icns

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

# Include paths
INCLUDEPATH += \
    APP/include \
    Modules/FileOperation \
    Modules/MenuOperation \
    Modules/DatabaseOperation

# Source files
SOURCES += \
    APP/src/main.cpp \
    APP/src/signalmgrapp.cpp \
    Modules/FileOperation/fileoperations.cpp \
    Modules/MenuOperation/menuoperations.cpp \
    Modules/DatabaseOperation/databaseoperations.cpp

# Header files
HEADERS += \
    APP/include/signalmgrapp.h \
    Modules/FileOperation/fileoperations.h \
    Modules/MenuOperation/menuoperations.h \
    Modules/DatabaseOperation/databaseoperations.h

# UI forms
FORMS += \
    Cfg/LayoutFiles/signalmgrapp.ui

# Resource files
RESOURCES += \
    Cfg/Resources/resources.qrc

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

# Output directories
CONFIG(debug, debug|release) {
    DESTDIR = $$PWD/debug
} else {
    DESTDIR = $$PWD/Release
}

# Platform-specific build options
win32 {
    # Windows-specific configuration
    RC_FILE = Cfg/Resources/windows_resource.rc
}

unix:!macx {
    # Linux-specific configuration
    # Add any Linux-specific settings here
}

macx {
    # macOS-specific configuration
    # Add any macOS-specific settings here
}