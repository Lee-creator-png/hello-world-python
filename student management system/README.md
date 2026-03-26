# Student Management System (SMS) PRO

A modern, professional-grade desktop application for managing student records, academic performance, and institutional reporting. Built with Python and Tkinter, featuring a high-performance SQLite backend and a contemporary web-app inspired interface.

## 🚀 Key Features

- **Modern Dashboard**: Get an instant overview of system statistics (Total Students, Classes, Average Marks, etc.).
- **Student Directory**: Comprehensive management of student profiles with search and filter capabilities.
- **Academic Records**: Track student performance across different subjects and terms with ease.
- **Visual Analytics**: Generate performance charts and graphs (requires `matplotlib`).
- **Professional Reporting**: Export detailed student performance reports to PDF (requires `reportlab`).
- **Role-Based Access**: Secure login system with Admin and Staff roles.
- **SaaS-Inspired UI**: A clean, indigo-themed interface with modern components, zebra-striped tables, and intuitive navigation.

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **GUI Framework**: Tkinter (with custom modern styling)
- **Database**: SQLite3
- **Visualization**: Matplotlib (Optional)
- **PDF Generation**: Reportlab (Optional)

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd "student management system"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: If requirements.txt is not present, manually install optional features:*
   ```bash
   pip install matplotlib reportlab
   ```

## 🚦 Getting Started

Run the application using the main entry point:

```bash
python main.py
```

### **Default Admin Credentials**
- **Username**: `admin`
- **Password**: `admin123`
*(Note: These are standard for initial setup. Please update them in the User Management section after logging in.)*

## 📁 Project Structure

- `main.py`: Application entry point.
- `sms_app/`:
    - `app.py`: Core UI logic, theme definitions, and window management.
    - `db.py`: Database schema and student/mark management logic.
    - `reports.py`: Student report generation and PDF export.
    - `security.py`: Password hashing and verification utilities.

## 📊 Grading System

The SMS uses a standardized grading scale for converting numeric marks (0-100) to letter grades:

| Mark Range  | Grade |
|-------------|-------|
| 75 – 100    | A     |
| 65 – 74     | B     |
| 50 – 64     | C     |
| 40 – 49     | D     |
| Below 40    | F     |

Grades are automatically calculated and displayed:
- In the **Academic Records** tab alongside numeric marks
- In **PDF Reports** for each subject and term
- Throughout the system for quick performance assessment
