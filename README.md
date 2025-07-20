# 🚦 Traffic Violation Detection System

A secure and intelligent web-based system that allows authenticated users to upload vehicle images for automatic detection of traffic violations. The system uses CNN-based image analysis, OCR-based number plate recognition, and integrates multiple AWS services to notify the vehicle owner with relevant details and fines.

---

## 📌 Features

- 🔐 **User Authentication** using AWS Cognito (Login & Registration)
- 🌐 **Streamlit Web UI** with two pages: Login/Register and Image Upload
- 🧠 **CNN-based Violation Detection** for images (Helmet, Triple Riding, No Seatbelt, etc.)
- 🔍 **OCR-based License Plate Recognition** using EasyOCR / Tesseract
- 🔗 **Owner Info Retrieval** using mock data or simulated VAHAN lookup
- 📩 **Email Notification** to the violator using Gmail SMTP or AWS SNS
- 🗃️ **Data Storage** in AWS DynamoDB (violations & user info)
- 📊 **Redshift Logging** for long-term analytics and logs

---

## 🛠️ Tech Stack

| Category              | Tools / Technologies Used                      |
|-----------------------|------------------------------------------------|
| Front-End             | Streamlit, HTML/CSS                           |
| Back-End              | Python, OpenCV, EasyOCR/Tesseract, CNN        |
| Authentication        | AWS Cognito                                   |
| Cloud & Storage       | AWS S3 (image storage), DynamoDB, Redshift    |
| Email Notification    | Gmail SMTP / AWS SNS                          |
| Version Control       | Git & GitHub                                  |

---

## 📁 Folder Structure

```

📦traffic-violation-detection
┣ 📂cnn\_model/
┃ ┗ model.h5
┣ 📂data/
┃ ┣ captured\_images/
┃ ┗ trained\_images/
┣ 📂streamlit\_ui/
┃ ┗ app.py
┣ 📂utils/
┃ ┣ ocr.py
┃ ┣ aws\_helpers.py
┃ ┗ fine\_calculator.py
┣ 📄requirements.txt
┣ 📄README.md
┗ 📄.gitignore

````

---

## 🧪 Sample Workflow

1. User signs in or registers using AWS Cognito.
2. Uploads a vehicle image through the Streamlit UI.
3. Image is sent to:
   - CNN model for violation classification.
   - OCR for license plate detection.
4. License plate number is matched with mock owner data.
5. Violation details and total fine calculated.
6. Owner receives an email with the violation summary and fine.

---

## 🚀 Installation & Running Locally

```bash
# Clone the repository
git clone https://github.com/your-username/traffic-violation-detection.git
cd traffic-violation-detection

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run streamlit_ui/app.py
````

---


## 💡 Future Scope

* Connect to real VAHAN API for owner verification
* Add mobile notifications with Twilio or WhatsApp
* Add live video stream detection
* Host on AWS EC2 with HTTPS and domain

---

## 📝 License

This project is open-source and available under the MIT License.

