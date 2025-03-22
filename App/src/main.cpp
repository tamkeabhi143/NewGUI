#include "signalmgrapp.h"

#include <QApplication>
#include <QFile>
#include <QDir>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    
    // Set application information
    app.setApplicationName("Signal Manager");
    app.setApplicationVersion("1.0.0");
    app.setOrganizationName("Your Organization");
    app.setOrganizationDomain("yourorganization.com");
    
    // Apply dark theme stylesheet
    QFile styleFile(":/styles/dark_theme.qss");
    if (styleFile.exists() && styleFile.open(QFile::ReadOnly | QFile::Text)) {
        QString style = QLatin1String(styleFile.readAll());
        app.setStyleSheet(style);
        styleFile.close();
    } else {
        qWarning() << "Could not open stylesheet file.";
    }
    
    // Create and show the main window
    SignalMgrApp mainWindow;
    mainWindow.show();
    
    return app.exec();
}