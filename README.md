# MoSTwo

A Python application for surface mapping and visualization.

## Project Structure

```
mostwo/
├── Controller/         # Application controllers
├── Model/             # Data models and business logic
├── View/              # User interface components
│   ├── binio_frames/  # Binary I/O frame views
│   └── individual_surfaces/  # Surface-specific views
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## Getting Started

### Prerequisites

- Python 3.x
- Required Python packages (install with `pip install -r requirements.txt`)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mostwo
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

Run the main application:
```bash
python Controller/main.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
