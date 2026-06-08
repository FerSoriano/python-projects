# KeePass Downloader

A simple Python script that automatically downloads your KeePass password database file from Google Drive to your local machine.

## What it does

This script:
- Authenticates with Google Drive using a service account
- Searches for a `.kdbx` file in a specified folder
- Downloads the file to a local destination
- Displays download progress

## Requirements

- Python 3.7+
- A Google Cloud service account with Drive access
- A shared Google Drive folder containing your KeePass file

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. **Create a service account** on Google Cloud Console
2. **Download the credentials file** and save it locally
3. **Share the Google Drive folder** with the service account email
4. **Configure environment variables**:
   - Copy `.env-example` to `.env`
   - Fill in the values:
     ```
     SERVICE_ACCOUNT_FILE=/path/to/your/credentials.json
     FOLDER_ID=your_google_drive_folder_id
     DESTINATION_FILE=/path/to/destination/Passwords.kdbx
     ```

## Usage

Run the script:
```bash
python download_keepass.py
```

The script will:
- Search for a `.kdbx` file in the specified Drive folder
- Download it to your local destination
- Show the download progress


## Security

- **Never commit** `.env` or `credentials.json` to version control
- Use `.env-example` as a template for new setups
- Keep your Google service account credentials secure
