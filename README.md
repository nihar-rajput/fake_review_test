# 🛡️ Fake Review Detection

A Machine Learning based web application that detects whether a product review is **Genuine** or **Fake** using Natural Language Processing (NLP) techniques.

The project helps identify deceptive reviews that can mislead customers on e-commerce platforms.

---

## ✨ Features

- Detect fake and genuine reviews
- Text preprocessing and cleaning
- Machine Learning based prediction
- User-friendly web interface
- Real-time review analysis
- Easy to extend with new datasets and models

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask

### Machine Learning
- Scikit-learn
- Pandas
- NumPy
- NLTK

### Frontend
- HTML
- CSS
- Bootstrap
- JavaScript

---

## 📂 Project Structure

```
fake_review_test/
│
├── app.py                 # Main Flask application
├── model/                 # Trained ML model
├── templates/             # HTML pages
├── static/                # CSS, JS and images
├── dataset/               # Training dataset
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/nihar-rajput/fake_review_test.git
```

### 2. Navigate to the project

```bash
cd fake_review_test
```

### 3. Create a virtual environment (Optional)

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

```bash
python app.py
```

Open your browser and visit

```
http://127.0.0.1:5000
```

---

## 🧠 Machine Learning Pipeline

1. Collect review dataset
2. Clean and preprocess text
3. Tokenization
4. Stopword removal
5. Feature extraction using TF-IDF
6. Train Machine Learning model
7. Save trained model
8. Predict whether a review is Fake or Genuine

---

## 📊 Example

**Input**

```
"This product is amazing! Best purchase ever!!"
```

**Output**

```
Prediction: Genuine Review
```

---

## 📦 Requirements

- Python 3.9+
- Flask
- scikit-learn
- pandas
- numpy
- nltk
- joblib

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## 🚀 Future Improvements

- Deep Learning (LSTM/BERT)
- Explainable AI predictions
- Confidence score
- REST API
- User authentication
- Review history
- Docker support
- Deployment on Render/AWS

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Added new feature"
```

4. Push to GitHub

```bash
git push origin feature-name
```

5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Nihar Rajput**

- GitHub: https://github.com/nihar-rajput

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
