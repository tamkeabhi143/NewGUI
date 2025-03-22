#include "signalmgrapp.h"
#include "ui_signalmgrapp.h"
#include "fileoperations.h"

#include <QFile>
#include <QDir>
#include <QMessageBox>
#include <QFileDialog>
#include <QStandardPaths>
#include <QSettings>
#include <QStyleFactory>
#include <QSplitter>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QLineEdit>
#include <QComboBox>
#include <QDateTimeEdit>
#include <QPlainTextEdit>
#include <QPushButton>
#include <QTableWidget>
#include <QHeaderView>
#include <QGraphicsDropShadowEffect>
#include <QDebug>

SignalMgrApp::SignalMgrApp(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::SignalMgrApp)
    , fileOperations(new FileOperations(this))
    , currentProjectName("Untitled")
    , hasUnsavedChanges(false)
{
    ui->setupUi(this);
    
    // Set window title and attributes
    setWindowTitle("Signal Manager - " + currentProjectName);
    setMinimumSize(1000, 700);
    
    // Set up modern UI
    setupModernUI();
    
    // Connect signals and slots
    connectSignalsSlots();
    
    // Load settings
    loadSettings();
}

SignalMgrApp::~SignalMgrApp()
{
    delete ui;
}

void SignalMgrApp::setupModernUI()
{
    // Create central widget with horizontal layout
    QWidget* centralWidget = new QWidget();
    QHBoxLayout* mainLayout = new QHBoxLayout(centralWidget);
    mainLayout->setContentsMargins(0, 0, 0, 0);
    mainLayout->setSpacing(0);
    setCentralWidget(centralWidget);
    
    // Create sidebar navigation panel
    QWidget* sidebarWidget = new QWidget();
    sidebarWidget->setObjectName("sidebarWidget");
    sidebarWidget->setFixedWidth(220);
    
    QVBoxLayout* sidebarLayout = new QVBoxLayout(sidebarWidget);
    sidebarLayout->setContentsMargins(10, 20, 10, 20);
    sidebarLayout->setSpacing(5);
    
    // App title
    QLabel* titleLabel = new QLabel("Signal Manager");
    titleLabel->setStyleSheet("font-size: 22px; font-weight: bold; color: #E0E0E0; margin-bottom: 15px;");
    sidebarLayout->addWidget(titleLabel);
    
    // Navigation items
    QStringList navItems = {"Core Configuration", "Project Config", "Signal Database", "Code Generator", "Settings"};
    
    navButtons.clear();
    for (int i = 0; i < navItems.size(); i++) {
        QPushButton* navButton = new QPushButton(navItems[i]);
        navButton->setStyleSheet(
            "QPushButton {"
                "background-color: #1E2233;"
                "color: #B0B0B0;"
                "border-radius: 4px;"
                "padding: 12px 15px;"
                "text-align: left;"
                "font-size: 14px;"
                "margin: 2px 0px;"
            "}"
            "QPushButton:hover {"
                "background-color: #262D40;"
            "}"
            "QPushButton:checked {"
                "background-color: #2C3548;"
                "color: #FFFFFF;"
                "border-left: 3px solid #3498DB;"
            "}"
        );
        navButton->setCheckable(true);
        
        connect(navButton, &QPushButton::clicked, this, [this, i]() {
            onNavigationButtonClicked(i);
        });
        
        sidebarLayout->addWidget(navButton);
        navButtons.append(navButton);
    }
    
    // Set first button checked by default
    if (!navButtons.isEmpty()) {
        navButtons[0]->setChecked(true);
    }
    
    // Add spacer to push profile to bottom
    sidebarLayout->addStretch();
    
    // Add user profile section
    QHBoxLayout* profileLayout = new QHBoxLayout();
    
    QLabel* profileIcon = new QLabel();
    profileIcon->setFixedSize(32, 32);
    profileIcon->setStyleSheet("background-color: #3498DB; border-radius: 16px;");
    
    QLabel* profileName = new QLabel("User Profile");
    profileName->setStyleSheet("color: #FFFFFF; font-size: 14px;");
    
    profileLayout->addWidget(profileIcon);
    profileLayout->addWidget(profileName);
    profileLayout->addStretch();
    
    sidebarLayout->addLayout(profileLayout);
    
    // Add sidebar to main layout
    mainLayout->addWidget(sidebarWidget);
    
    // Create content stack
    contentStack = new QStackedWidget();
    contentStack->setStyleSheet("background-color: #1E2233;");
    
    // Add content pages
    setupCoreConfigPage();
    setupProjectConfigPage();
    setupSignalDatabasePage();
    setupCodeGeneratorPage();
    setupSettingsPage();
    
    // Add content stack to main layout
    mainLayout->addWidget(contentStack);
}

void SignalMgrApp::setupCoreConfigPage()
{
    QWidget* coreConfigPage = new QWidget();
    QVBoxLayout* pageLayout = new QVBoxLayout(coreConfigPage);
    pageLayout->setContentsMargins(20, 20, 20, 20);
    pageLayout->setSpacing(20);
    
    // Top bar with search and actions
    QHBoxLayout* topBarLayout = new QHBoxLayout();
    
    // Search field
    QLineEdit* searchField = new QLineEdit();
    searchField->setPlaceholderText("Search configurations...");
    searchField->setFixedHeight(36);
    
    // Action buttons
    QPushButton* newButton = new QPushButton("New");
    newButton->setIcon(QIcon(":/icons/new.png"));
    
    QPushButton* importButton = new QPushButton("Import");
    importButton->setIcon(QIcon(":/icons/import.png"));
    
    topBarLayout->addWidget(searchField);
    topBarLayout->addStretch();
    topBarLayout->addWidget(newButton);
    topBarLayout->addWidget(importButton);
    
    pageLayout->addLayout(topBarLayout);
    
    // Content layout with cards
    QHBoxLayout* cardsLayout = new QHBoxLayout();
    cardsLayout->setSpacing(20);
    
    // Core Info Card
    QFrame* coreInfoCard = createCard("SOC Core Information");
    QVBoxLayout* coreInfoLayout = new QVBoxLayout(coreInfoCard);
    
    // Add form fields
    QFormLayout* coreForm = new QFormLayout();
    coreForm->setSpacing(15);
    coreForm->setLabelAlignment(Qt::AlignLeft);
    coreForm->setFieldGrowthPolicy(QFormLayout::AllNonFixedFieldsGrow);
    
    QLineEdit* coreIdField = new QLineEdit();
    QLineEdit* versionField = new QLineEdit();
    QComboBox* configTypeCombo = new QComboBox();
    configTypeCombo->addItems({"Standard", "Extended", "Custom"});
    
    coreForm->addRow("Core ID:", coreIdField);
    coreForm->addRow("Version:", versionField);
    coreForm->addRow("Configuration Type:", configTypeCombo);
    
    coreInfoLayout->addLayout(coreForm);
    cardsLayout->addWidget(coreInfoCard);
    
    // Version Details Card
    QFrame* versionCard = createCard("Version Details");
    QVBoxLayout* versionLayout = new QVBoxLayout(versionCard);
    
    QFormLayout* versionForm = new QFormLayout();
    versionForm->setSpacing(15);
    
    QLineEdit* versionNumberField = new QLineEdit();
    QDateTimeEdit* versionDateField = new QDateTimeEdit(QDateTime::currentDateTime());
    QLineEdit* updatedByField = new QLineEdit();
    QPlainTextEdit* changeDescField = new QPlainTextEdit();
    changeDescField->setMaximumHeight(80);
    
    versionForm->addRow("Version Number:", versionNumberField);
    versionForm->addRow("Date:", versionDateField);
    versionForm->addRow("Updated By:", updatedByField);
    versionForm->addRow("Change Description:", changeDescField);
    
    versionLayout->addLayout(versionForm);
    cardsLayout->addWidget(versionCard);
    
    pageLayout->addLayout(cardsLayout, 1);
    
    // Action buttons area
    QHBoxLayout* actionLayout = new QHBoxLayout();
    actionLayout->setContentsMargins(0, 10, 0, 0);
    
    QPushButton* updateButton = new QPushButton("Update Configuration");
    updateButton->setMinimumWidth(150);
    
    QPushButton* resetButton = new QPushButton("Reset");
    resetButton->setMinimumWidth(150);
    resetButton->setProperty("class", "secondary");
    resetButton->setStyleSheet(
        "QPushButton {"
            "background-color: transparent;"
            "border: 1px solid #3498DB;"
            "color: #3498DB;"
        "}"
        "QPushButton:hover {"
            "background-color: rgba(52, 152, 219, 0.1);"
        "}"
    );
    
    actionLayout->addStretch();
    actionLayout->addWidget(updateButton);
    actionLayout->addWidget(resetButton);
    actionLayout->addStretch();
    
    pageLayout->addLayout(actionLayout);
    
    // Status table
    QFrame* statusCard = createCard("Configuration Status");
    QVBoxLayout* statusLayout = new QVBoxLayout(statusCard);
    
    QTableWidget* statusTable = new QTableWidget(4, 5);
    statusTable->setHorizontalHeaderLabels({"ID", "Name", "Status", "Last Updated", "Actions"});
    statusTable->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    statusTable->verticalHeader()->setVisible(false);
    statusTable->setSelectionBehavior(QAbstractItemView::SelectRows);
    statusTable->setEditTriggers(QAbstractItemView::NoEditTriggers);
    statusTable->setAlternatingRowColors(true);
    
    // Sample data
    QStringList ids = {"001", "002", "003", "004"};
    QStringList names = {"Core Configuration A", "Core Configuration B", "Core Configuration C", "Core Configuration D"};
    QStringList statuses = {"Active", "Inactive", "Draft", "Active"};
    QStringList dates = {"2023-10-15", "2023-09-20", "2023-10-05", "2023-10-12"};
    
    for (int row = 0; row < 4; row++) {
        // ID
        QTableWidgetItem* idItem = new QTableWidgetItem(ids[row]);
        statusTable->setItem(row, 0, idItem);
        
        // Name
        QTableWidgetItem* nameItem = new QTableWidgetItem(names[row]);
        statusTable->setItem(row, 1, nameItem);
        
        // Status
        QWidget* statusWidget = new QWidget();
        QHBoxLayout* statusLayout = new QHBoxLayout(statusWidget);
        statusLayout->setContentsMargins(5, 2, 5, 2);
        statusLayout->setAlignment(Qt::AlignCenter);
        
        QLabel* statusLabel = new QLabel(statuses[row]);
        statusLabel->setAlignment(Qt::AlignCenter);
        
        QString statusStyle;
        if (statuses[row] == "Active") {
            statusStyle = "background-color: #27AE60; color: white;";
        } else if (statuses[row] == "Inactive") {
            statusStyle = "background-color: #7F8C9A; color: white;";
        } else if (statuses[row] == "Draft") {
            statusStyle = "background-color: #E67E22; color: white;";
        }
        
        statusLabel->setStyleSheet("border-radius: 10px; padding: 3px 10px;" + statusStyle);
        statusLayout->addWidget(statusLabel);
        
        statusTable->setCellWidget(row, 2, statusWidget);
        
        // Date
        QTableWidgetItem* dateItem = new QTableWidgetItem(dates[row]);
        statusTable->setItem(row, 3, dateItem);
        
        // Actions
        QWidget* actionsWidget = new QWidget();
        QHBoxLayout* actionsLayout = new QHBoxLayout(actionsWidget);
        actionsLayout->setContentsMargins(5, 2, 5, 2);
        actionsLayout->setAlignment(Qt::AlignCenter);
        
        QPushButton* editButton = new QPushButton();
        editButton->setIcon(QIcon(":/icons/edit.png"));
        editButton->setFixedSize(24, 24);
        editButton->setIconSize(QSize(14, 14));
        editButton->setStyleSheet("background-color: #3498DB; border-radius: 12px;");
        
        QPushButton* deleteButton = new QPushButton();
        deleteButton->setIcon(QIcon(":/icons/delete.png"));
        deleteButton->setFixedSize(24, 24);
        deleteButton->setIconSize(QSize(14, 14));
        deleteButton->setStyleSheet("background-color: #E74C3C; border-radius: 12px;");
        
        actionsLayout->addWidget(editButton);
        actionsLayout->addWidget(deleteButton);
        
        statusTable->setCellWidget(row, 4, actionsWidget);
    }
    
    statusLayout->addWidget(statusTable);
    pageLayout->addWidget(statusCard, 2);
    
    // Add floating action button
    QPushButton* fabButton = new QPushButton("+");
    fabButton->setObjectName("fabButton");
    fabButton->setFixedSize(56, 56);
    fabButton->setStyleSheet(
        "QPushButton#fabButton {"
            "background-color: #3498DB;"
            "color: white;"
            "border-radius: 28px;"
            "font-size: 24px;"
            "font-weight: bold;"
        "}"
        "QPushButton#fabButton:hover {"
            "background-color: #2980B9;"
        "}"
    );
    
    // Set up drop shadow effect for FAB
    QGraphicsDropShadowEffect* shadowEffect = new QGraphicsDropShadowEffect();
    shadowEffect->setBlurRadius(15);
    shadowEffect->setColor(QColor(0, 0, 0, 80));
    shadowEffect->setOffset(0, 2);
    fabButton->setGraphicsEffect(shadowEffect);
    
    // Position FAB at bottom right of the page
    fabButton->setParent(coreConfigPage);
    fabButton->move(coreConfigPage->width() - 76, coreConfigPage->height() - 76);
    
    // Update FAB position when window is resized
    connect(this, &SignalMgrApp::resized, this, [this, coreConfigPage, fabButton]() {
        fabButton->move(coreConfigPage->width() - 76, coreConfigPage->height() - 76);
    });
    
    // Connect FAB to add entry action
    connect(fabButton, &QPushButton::clicked, this, &SignalMgrApp::on_actionAdd_Entry_triggered);
    
    contentStack->addWidget(coreConfigPage);
}

QFrame* SignalMgrApp::createCard(const QString& title)
{
    QFrame* card = new QFrame();
    card->setObjectName("card");
    card->setStyleSheet(
        "QFrame#card {"
            "background-color: #2C3548;"
            "border-radius: 8px;"
            "padding: 15px;"
        "}"
    );
    
    // Add drop shadow effect
    QGraphicsDropShadowEffect* shadowEffect = new QGraphicsDropShadowEffect();
    shadowEffect->setBlurRadius(10);
    shadowEffect->setColor(QColor(0, 0, 0, 60));
    shadowEffect->setOffset(0, 2);
    card->setGraphicsEffect(shadowEffect);
    
    // Create layout for card
    QVBoxLayout* cardLayout = new QVBoxLayout(card);
    cardLayout->setContentsMargins(15, 15, 15, 15);
    
    // Add title
    if (!title.isEmpty()) {
        QLabel* titleLabel = new QLabel(title);
        titleLabel->setStyleSheet("font-size: 16px; font-weight: bold; color: white;");
        
        QHBoxLayout* headerLayout = new QHBoxLayout();
        headerLayout->addWidget(titleLabel);
        headerLayout->addStretch();
        
        cardLayout->addLayout(headerLayout);
        
        // Add separator line
        QFrame* line = new QFrame();
        line->setFrameShape(QFrame::HLine);
        line->setFrameShadow(QFrame::Sunken);
        line->setStyleSheet("background-color: #3498DB;");
        line->setMaximumHeight(2);
        
        cardLayout->addWidget(line);
        cardLayout->addSpacing(10);
    }
    
    return card;
}

void SignalMgrApp::setupProjectConfigPage()
{
    QWidget* projectConfigPage = new QWidget();
    QVBoxLayout* layout = new QVBoxLayout(projectConfigPage);
    layout->setContentsMargins(20, 20, 20, 20);
    
    QLabel* pageLabel = new QLabel("Project Configuration");
    pageLabel->setStyleSheet("font-size: 24px; color: white;");
    layout->addWidget(pageLabel);
    
    // API Configuration Card
    QFrame* apiCard = createCard("API Configuration");
    QVBoxLayout* apiLayout = new QVBoxLayout(apiCard);
    
    // Path Configuration Card
    QFrame* pathCard = createCard("Path Configuration");
    QVBoxLayout* pathLayout = new QVBoxLayout(pathCard);
    
    // Output path
    QHBoxLayout* outputPathLayout = new QHBoxLayout();
    QLabel* outputPathLabel = new QLabel("Choose Output Directory:");
    QLineEdit* outputPathLineEdit = new QLineEdit();
    QPushButton* outputPathButton = new QPushButton("Browse...");
    
    outputPathLayout->addWidget(outputPathLabel);
    outputPathLayout->addWidget(outputPathLineEdit, 1);
    outputPathLayout->addWidget(outputPathButton);
    
    // Script path
    QHBoxLayout* scriptPathLayout = new QHBoxLayout();
    QLabel* scriptPathLabel = new QLabel("Choose Scripts Directory:");
    QLineEdit* scriptPathLineEdit = new QLineEdit();
    QPushButton* scriptPathButton = new QPushButton("Browse...");
    
    scriptPathLayout->addWidget(scriptPathLabel);
    scriptPathLayout->addWidget(scriptPathLineEdit, 1);
    scriptPathLayout->addWidget(scriptPathButton);
    
    pathLayout->addLayout(outputPathLayout);
    pathLayout->addLayout(scriptPathLayout);
    
    // Add cards to layout
    layout->addWidget(apiCard);
    layout->addWidget(pathCard);
    layout->addStretch();
    
    // Add page to stack
    contentStack->addWidget(projectConfigPage);
}

void SignalMgrApp::setupSignalDatabasePage()
{
    QWidget* signalDbPage = new QWidget();
    QVBoxLayout* layout = new QVBoxLayout(signalDbPage);
    layout->setContentsMargins(20, 20, 20, 20);
    
    // Signal Database Layout
    QHBoxLayout* signalDbLayout = new QHBoxLayout();
    
    // Signal Entry Frame
    QFrame* signalEntryFrame = createCard("Signal Names");
    signalEntryFrame->setMinimumWidth(400);
    
    // Signal Details Frame
    QFrame* signalDetailsFrame = createCard("Signal Details");
    signalDetailsFrame->setMinimumWidth(400);
    
    // Add frames to layout
    signalDbLayout->addWidget(signalEntryFrame);
    signalDbLayout->addWidget(signalDetailsFrame);
    layout->addLayout(signalDbLayout, 1);
    
    // Board selector layout
    QHBoxLayout* selectorLayout = new QHBoxLayout();
    
    QComboBox* boardListComboBox = new QComboBox();
    boardListComboBox->setMinimumWidth(200);
    boardListComboBox->addItems({"Board 1", "Board 2", "Board 3"});
    
    QComboBox* socListComboBox = new QComboBox();
    socListComboBox->setMinimumWidth(200);
    socListComboBox->addItems({"SOC 1", "SOC 2", "SOC 3"});
    
    QComboBox* buildImageComboBox = new QComboBox();
    buildImageComboBox->setMinimumWidth(200);
    buildImageComboBox->addItems({"Build Image 1", "Build Image 2", "Build Image 3"});
    
    selectorLayout->addWidget(boardListComboBox);
    selectorLayout->addStretch();
    selectorLayout->addWidget(socListComboBox);
    selectorLayout->addStretch();
    selectorLayout->addWidget(buildImageComboBox);
    
    layout->addLayout(selectorLayout);
    
    // Add page to stack
    contentStack->addWidget(signalDbPage);
}

void SignalMgrApp::setupCodeGeneratorPage()
{
    QWidget* codeGenPage = new QWidget();
    QVBoxLayout* layout = new QVBoxLayout(codeGenPage);
    layout->setContentsMargins(20, 20, 20, 20);
    
    QLabel* pageLabel = new QLabel("Code Generator");
    pageLabel->setStyleSheet("font-size: 24px; color: white;");
    layout->addWidget(pageLabel);
    
    // Code Generator options
    QFrame* generatorCard = createCard("Generator Options");
    QVBoxLayout* generatorLayout = new QVBoxLayout(generatorCard);
    
    QComboBox* generatorTypeCombo = new QComboBox();
    generatorTypeCombo->addItems({"SignalMgr", "IpcManager", "IpcOvEthMgr"});
    
    QFormLayout* generatorForm = new QFormLayout();
    generatorForm->addRow("Generator Type:", generatorTypeCombo);
    
    QLineEdit* outputPathLineEdit = new QLineEdit();
    QPushButton* browseButton = new QPushButton("Browse...");
    QHBoxLayout* pathLayout = new QHBoxLayout();
    pathLayout->addWidget(outputPathLineEdit);
    pathLayout->addWidget(browseButton);
    
    generatorForm->addRow("Output Path:", pathLayout);
    
    generatorLayout->addLayout(generatorForm);
    
    // Generate Button
    QPushButton* generateButton = new QPushButton("Generate Code");
    generateButton->setMinimumWidth(200);
    
    QHBoxLayout* buttonLayout = new QHBoxLayout();
    buttonLayout->addStretch();
    buttonLayout->addWidget(generateButton);
    buttonLayout->addStretch();
    
    // Add to main layout
    layout->addWidget(generatorCard);
    layout->addLayout(buttonLayout);
    layout->addStretch();
    
    // Add page to stack
    contentStack->addWidget(codeGenPage);
}

void SignalMgrApp::setupSettingsPage()
{
    QWidget* settingsPage = new QWidget();
    QVBoxLayout* layout = new QVBoxLayout(settingsPage);
    layout->setContentsMargins(20, 20, 20, 20);
    
    QLabel* pageLabel = new QLabel("Settings");
    pageLabel->setStyleSheet("font-size: 24px; color: white;");
    layout->addWidget(pageLabel);
    
    // Settings sections
    QFrame* appearanceCard = createCard("Appearance");
    QVBoxLayout* appearanceLayout = new QVBoxLayout(appearanceCard);
    
    QCheckBox* darkModeCheckbox = new QCheckBox("Dark Mode");
    darkModeCheckbox->setChecked(true);
    
    appearanceLayout->addWidget(darkModeCheckbox);
    
    // Default paths
    QFrame* defaultPathsCard = createCard("Default Paths");
    QVBoxLayout* pathsLayout = new QVBoxLayout(defaultPathsCard);
    
    QFormLayout* pathsForm = new QFormLayout();
    
    QLineEdit* projectPathLineEdit = new QLineEdit();
    QPushButton* projectPathButton = new QPushButton("Browse...");
    QHBoxLayout* projectPathLayout = new QHBoxLayout();
    projectPathLayout->addWidget(projectPathLineEdit);
    projectPathLayout->addWidget(projectPathButton);
    
    QLineEdit* outputPathLineEdit = new QLineEdit();
    QPushButton* outputPathButton = new QPushButton("Browse...");
    QHBoxLayout* outputPathLayout = new QHBoxLayout();
    outputPathLayout->addWidget(outputPathLineEdit);
    outputPathLayout->addWidget(outputPathButton);
    
    pathsForm->addRow("Default Project Path:", projectPathLayout);
    pathsForm->addRow("Default Output Path:", outputPathLayout);
    
    pathsLayout->addLayout(pathsForm);
    
    // Save settings button
    QPushButton* saveButton = new QPushButton("Save Settings");
    
    // Add to layout
    layout->addWidget(appearanceCard);
    layout->addWidget(defaultPathsCard);
    layout->addStretch();
    layout->addWidget(saveButton, 0, Qt::AlignCenter);
    
    // Add page to stack
    contentStack->addWidget(settingsPage);
}

void SignalMgrApp::onNavigationButtonClicked(int pageIndex)
{
    setActivePage(pageIndex);
}

void SignalMgrApp::setActivePage(int index)
{
    // Update button states
    for (int i = 0; i < navButtons.size(); i++) {
        navButtons[i]->setChecked(i == index);
    }
    
    // Switch page in stack
    contentStack->setCurrentIndex(index);
}

void SignalMgrApp::resizeEvent(QResizeEvent* event)
{
    QMainWindow::resizeEvent(event);
    emit resized();
}

void SignalMgrApp::closeEvent(QCloseEvent* event)
{
    if (maybeSave()) {
        saveSettings();
        event->accept();
    } else {
        event->ignore();
    }
}

bool SignalMgrApp::maybeSave()
{
    if (!hasUnsavedChanges) {
        return true;
    }
    
    QMessageBox::StandardButton ret = QMessageBox::warning(
        this,
        tr("Signal Manager"),
        tr("The document has been modified.\n"
           "Do you want to save your changes?"),
        QMessageBox::Save | QMessageBox::Discard | QMessageBox::Cancel
    );
    
    if (ret == QMessageBox::Save) {
        return on_actionSave_triggered(), true;
    } else if (ret == QMessageBox::Cancel) {
        return false;
    }
    
    return true;
}

void SignalMgrApp::loadSettings()
{
    QSettings settings("YourOrganization", "SignalManager");
    
    // Window geometry
    restoreGeometry(settings.value("geometry").toByteArray());
    restoreState(settings.value("windowState").toByteArray());
    
    // Recent files
    // TODO: Implement recent files list
}

void SignalMgrApp::saveSettings()
{
    QSettings settings("YourOrganization", "SignalManager");
    
    // Window geometry
    settings.setValue("geometry", saveGeometry());
    settings.setValue("windowState", saveState());
    
    // Other settings
    // TODO: Save other application settings
}

void SignalMgrApp::updateWindowTitle()
{
    QString title = "Signal Manager";
    
    if (!currentProjectName.isEmpty()) {
        title += " - " + currentProjectName;
    }
    
    if (hasUnsavedChanges) {
        title += " *";
    }
    
    setWindowTitle(title);
}

void SignalMgrApp::connectSignalsSlots()
{
    // Connect signals and slots
}

// File menu actions
void SignalMgrApp::on_actionNew_triggered()
{
    if (maybeSave()) {
        newProject();
    }
}

void SignalMgrApp::on_actionOpen_triggered()
{
    if (maybeSave()) {
        QString filePath = QFileDialog::getOpenFileName(
            this,
            tr("Open Project"),
            QStandardPaths::writableLocation(QStandardPaths::DocumentsLocation),
            tr("Signal Manager Files (*.smgr);;All Files (*)")
        );
        
        if (!filePath.isEmpty()) {
            loadProject(filePath);
        }
    }
}

void SignalMgrApp::on_actionSave_triggered()
{
    if (currentFilePath.isEmpty()) {
        on_actionSave_As_triggered();
    } else {
        saveProject(currentFilePath);
    }
}

void SignalMgrApp::on_actionSave_As_triggered()
{
    QString filePath = QFileDialog::getSaveFileName(
        this,
        tr("Save Project"),
        QStandardPaths::writableLocation(QStandardPaths::DocumentsLocation),
        tr("Signal Manager Files (*.smgr);;All Files (*)")
    );
    
    if (!filePath.isEmpty()) {
        if (!filePath.endsWith(".smgr")) {
            filePath += ".smgr";
        }
        saveProject(filePath);
    }
}

void SignalMgrApp::on_actionExport_To_Excel_triggered()
{
    QString filePath = QFileDialog::getSaveFileName(
        this,
        tr("Export to Excel"),
        QStandardPaths::writableLocation(QStandardPaths::DocumentsLocation),
        tr("Excel Files (*.xlsx);;CSV Files (*.csv);;All Files (*)")
    );
    
    if (!filePath.isEmpty()) {
        // Update data from UI before exporting
        updateDataFromUI();
        
        // Export data to Excel
        if (fileOperations->exportToExcel(filePath, projectData)) {
            QMessageBox::information(this, tr("Export Successful"), tr("Data was successfully exported to %1").arg(filePath));
        } else {
            QMessageBox::warning(this, tr("Export Failed"), tr("Failed to export data to %1").arg(filePath));
        }
    }
}

void SignalMgrApp::on_actionImport_From_Excel_triggered()
{
    QString filePath = QFileDialog::getOpenFileName(
        this,
        tr("Import from Excel"),
        QStandardPaths::writableLocation(QStandardPaths::DocumentsLocation),
        tr("Excel Files (*.xlsx);;CSV Files (*.csv);;All Files (*)")
    );
    
    if (!filePath.isEmpty()) {
        QJsonObject importedData;
        
        // Import data from Excel
        if (fileOperations->importFromExcel(filePath, importedData)) {
            // Update project data with imported data
            projectData = importedData;
            
            // Update UI with new data
            updateUIFromData();
            
            // Mark as having unsaved changes
            hasUnsavedChanges = true;
            updateWindowTitle();
            
            QMessageBox::information(this, tr("Import Successful"), tr("Data was successfully imported from %1").arg(filePath));
        } else {
            QMessageBox::warning(this, tr("Import Failed"), tr("Failed to import data from %1").arg(filePath));
        }
    }
}

void SignalMgrApp::on_actionClose_triggered()
{
    if (maybeSave()) {
        newProject();
    }
}

void SignalMgrApp::on_actionExit_triggered()
{
    close();
}

// Edit menu actions
void SignalMgrApp::on_actionAdd_Entry_triggered()
{
    // TODO: Implement add entry functionality
    QMessageBox::information(this, tr("Add Entry"), tr("Add Entry functionality to be implemented"));
}

void SignalMgrApp::on_actionDelete_Entry_triggered()
{
    // TODO: Implement delete entry functionality
    QMessageBox::information(this, tr("Delete Entry"), tr("Delete Entry functionality to be implemented"));
}

void SignalMgrApp::on_actionUpdate_Entry_triggered()
{
    // TODO: Implement update entry functionality
    QMessageBox::information(this, tr("Update Entry"), tr("Update Entry functionality to be implemented"));
}

void SignalMgrApp::newProject()
{
    // Clear current project data
    currentProjectName = "Untitled";
    currentFilePath = "";
    hasUnsavedChanges = false;
    projectData = QJsonObject();
    
    // Update UI
    updateUIFromData();
    updateWindowTitle();
}

bool SignalMgrApp::loadProject(const QString& filePath)
{
    if (fileOperations->loadConfigFile(filePath)) {
        // TODO: Parse the loaded data and update UI
        currentFilePath = filePath;
        
        // Extract filename without path and extension
        QFileInfo fileInfo(filePath);
        currentProjectName = fileInfo.baseName();
        
        hasUnsavedChanges = false;
        updateWindowTitle();
        
        QMessageBox::information(this, tr("Load Successful"), tr("Project was successfully loaded from %1").arg(filePath));
        return true;
    } else {
        QMessageBox::warning(this, tr("Load Failed"), tr("Failed to load project from %1").arg(filePath));
        return false;
    }
}

bool SignalMgrApp::saveProject(const QString& filePath)
{
    // Update data from UI before saving
    updateDataFromUI();
    
    if (fileOperations->saveConfigFile(filePath, projectData)) {
        currentFilePath = filePath;
        
        // Extract filename without path and extension
        QFileInfo fileInfo(filePath);
        currentProjectName = fileInfo.baseName();
        
        hasUnsavedChanges = false;
        updateWindowTitle();
        
        QMessageBox::information(this, tr("Save Successful"), tr("Project was successfully saved to %1").arg(filePath));
        return true;
    } else {
        QMessageBox::warning(this, tr("Save Failed"), tr("Failed to save project to %1").arg(filePath));
        return false;
    }
}

void SignalMgrApp::updateDataFromUI()
{
    // TODO: Collect data from UI and update projectData
    hasUnsavedChanges = true;
    updateWindowTitle();
}

void SignalMgrApp::updateUIFromData()
{
    // TODO: Update UI with data from projectData
}