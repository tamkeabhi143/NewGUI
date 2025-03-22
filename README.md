# Signal Manager

A modern PyQt5-based application for managing signal data and configurations with a sleek dark-themed UI.

## Features

- Clean, modern dark UI with card-based layout
- Signal database management
- Core configuration capabilities
- Code generation for various protocols
- Import/export functionality for Excel
- Cross-platform support (Windows and Linux)

## Project Structure

```
Signal-Manager/
├── Cfg/                   # Configuration files
│   ├── Icons/             # Application icons
│   ├── LayoutFiles/       # UI layout files (.ui)
│   └── Resources/         # Resource files (QSS, etc.)
├── Modules/               # Modular components
│   ├── FileOperation/     # File handling operations
│   ├── MenuOperation/     # Menu functionality
│   └── DatabaseOperation/ # Database operations
├── BuildScripts/          # Build automation
│   ├── Windows/           # Windows build scripts
│   └── Linux/             # Linux build scripts
├── TestConfiguration/     # Test input files
├── Release/               # Output binaries
│   ├── Windows/           # Windows release files
│   └── Linux/             # Linux release files
└── APP/                   # Main application code
```

## Requirements

- Python 3.6 or higher
- PyQt5
- Other dependencies are listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/Signal-Manager.git
   cd Signal-Manager
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

From the main project directory, run:

```
python APP/main.py
```

## Building Standalone Executables

### Windows

1. Navigate to the BuildScripts/Windows directory:
   ```
   cd BuildScripts/Windows
   ```

2. Run the build script:
   ```
   build_windows.bat
   ```

3. Find the executable in the Release/Windows directory

### Linux

1. Make the build script executable:
   ```
   chmod +x BuildScripts/Linux/build_linux.sh
   ```

2. Run the build script:
   ```
   ./BuildScripts/Linux/build_linux.sh
   ```

3. Find the executable in the Release/Linux directory, and run using the provided launcher script.

## Development

### Project Organization

- **APP/main.py**: Entry point of the application
- **APP/signal_manager_app.py**: Main application window implementation
- **Modules/FileOperation/file_operations.py**: File handling module
- **Modules/DatabaseOperation/database_operations.py**: Database operations module
- **Modules/MenuOperation/menu_operations.py**: Menu handling module
- **Cfg/Resources/styles/dark_theme.qss**: Dark theme stylesheet

### Adding New Modules

1. Create a new Python file in the appropriate Modules subdirectory
2. Import the module in APP/signal_manager_app.py
3. Initialize and use the module in the main application class

### Customizing the UI

The dark theme can be customized by modifying the QSS file at `Cfg/Resources/styles/dark_theme.qss`.

## License

[Your License Information]

## Contributing

[Your Contribution Guidelines]