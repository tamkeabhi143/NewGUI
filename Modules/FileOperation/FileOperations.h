#ifndef FILEOPERATIONS_H
#define FILEOPERATIONS_H

#include <QObject>
#include <QString>
#include <QFile>
#include <QJsonDocument>
#include <QJsonObject>

/**
 * @brief The FileOperations class handles file-related operations for the Signal Manager application
 */
class FileOperations : public QObject
{
    Q_OBJECT
    
public:
    explicit FileOperations(QObject *parent = nullptr);
    
    /**
     * @brief Load a configuration file
     * @param filePath Path to the configuration file
     * @return True if file loaded successfully, false otherwise
     */
    bool loadConfigFile(const QString &filePath);
    
    /**
     * @brief Save a configuration file
     * @param filePath Path to save the configuration file
     * @param configData Configuration data to save
     * @return True if file saved successfully, false otherwise
     */
    bool saveConfigFile(const QString &filePath, const QJsonObject &configData);
    
    /**
     * @brief Export data to Excel format
     * @param filePath Path to save the Excel file
     * @param data Data to export
     * @return True if export successful, false otherwise
     */
    bool exportToExcel(const QString &filePath, const QJsonObject &data);
    
    /**
     * @brief Import data from Excel format
     * @param filePath Path to the Excel file
     * @param data Variable to store the imported data
     * @return True if import successful, false otherwise
     */
    bool importFromExcel(const QString &filePath, QJsonObject &data);
    
private:
    QString m_lastFilePath;
    QJsonDocument m_currentDocument;
};

#endif // FILEOPERATIONS_H