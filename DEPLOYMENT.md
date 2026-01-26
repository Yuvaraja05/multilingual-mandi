# Deployment Guide - Multilingual Mandi

## Google Sheets Integration

### Setup Instructions:

1. **Enable Google Sheets API**
   - Go to Google Cloud Console
   - Enable Google Sheets API
   - Create service account credentials
   - Download JSON key file

2. **Share Your Google Sheet**
   - Open: https://share.google/XTtzUUM5K1idh86yW
   - Share with service account email
   - Give "Editor" permissions

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   ```bash
   # Add to .env file
   GOOGLE_SHEETS_URL=https://share.google/XTtzUUM5K1idh86yW
   GOOGLE_SERVICE_ACCOUNT_KEY=path/to/service-account.json
   ```

5. **Deploy to Streamlit Cloud**
   - Push code to GitHub
   - Connect to Streamlit Cloud
   - Add secrets for Google credentials

## Live Demo URLs:
- **Streamlit Cloud**: [Deploy Here](https://streamlit.io/cloud)
- **Local Development**: `streamlit run app.py`

## Data Format Expected:
Your Google Sheet should have columns:
- Crop Name
- Price (₹/kg)
- Market Name
- Grade
- Trend
- Demand