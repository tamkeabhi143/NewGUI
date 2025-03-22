#ifndef SIGNALMGRAPP_H
#define SIGNALMGRAPP_H

#include <QMainWindow>
#include <QPushButton>
#include <QStackedWidget>
#include <QFrame>
#include <QResizeEvent>
#include <QList>
#include <QJsonObject>

// Forward declarations
class FileOperations;

namespace Ui {
class SignalMgrApp;
}

class SignalMgrApp : public QMainWindow
{
    Q_OBJECT

public:
    explicit SignalMgrApp(QWidget *parent = nullptr);
    ~SignalMgrApp();

signals:
    void resized();

protected:
    void resizeEvent(QResizeEvent* event) override;
    void closeEvent(QCloseEvent* event) override;

private slots:
    // File menu actions
    void on_actionNew_triggered();
    void on_actionOpen_triggered();
    void on_actionSave_triggered();
    void on_actionSave_As_triggered();
    void on_actionExport_To_Excel_triggered();
    void on_actionImport_From_Excel_triggered();
    void on_actionClose_triggered();
    void on_actionExit_triggered();
    
    // Edit menu actions
    void on_actionAdd_Entry_triggered();
    void on_actionDelete_Entry_triggered();
    void on_actionUpdate_Entry_triggered();
    
    // Navigation slots
    void onNavigationButtonClicked(int pageIndex);
    
    // UI update slots
    void updateWindowTitle();

private:
    Ui::SignalMgrApp *ui;
    
    QList<QPushButton*> navButtons;
    QStackedWidget* contentStack;
    
    FileOperations* fileOperations;
    
    QString currentProjectName;
    QString currentFilePath;
    bool hasUnsavedChanges;
    QJsonObject projectData;
    
    // Setup methods
    void setupModernUI();
    void connectSignalsSlots();
    
    // Page setup methods
    void setupCoreConfigPage();
    void setupProjectConfigPage();
    void setupSignalDatabasePage();
    void setupCodeGeneratorPage();
    void setupSettingsPage();
    
    // Helper methods
    QFrame* createCard(const QString& title);
    void setActivePage(int index);
    bool maybeSave();
    void loadSettings();
    void saveSettings();
    
    // Data management
    void newProject();
    bool loadProject(const QString& filePath);
    bool saveProject(const QString& filePath);
    void updateDataFromUI();
    void updateUIFromData();
};

#endif // SIGNALMGRAPP_H