<div>

  <h1>Marrow-Find</h1>

  <p>This is a web-based Flask application for classifying medical images into categories such as <strong>Benign</strong>, <strong>Pre</strong>, <strong>Pro</strong>, and <strong>Early</strong> using a trained deep learning model. It includes user authentication, prediction history tracking, and downloadable PDF reports.</p>

  <p>GitHub Repository: <a href="https://github.com/gunavardhanlomada/Marrow-Find" target="_blank">Marrow-Find</a></p>
  <code>https://github.com/gunavardhanlomada/Marrow-Find</code>

  <h2>📋 Dataset</h2>
  <p>This project uses the <strong>Blood Cells Cancer (ALL) 4‑class</strong> dataset from Kaggle, which contains images for Acute Lymphoblastic Leukemia classification:</p>
  <p><a href="https://www.kaggle.com/datasets/mohammadamireshraghi/blood-cell-cancer-all-4class" target="_blank">https://www.kaggle.com/datasets/mohammadamireshraghi/blood-cell-cancer-all-4class</a></p>

  <h2>🚀 Features</h2>
  <ul>
    <li>✅ User Registration & Login</li>
    <li>🖼️ Image Upload and Classification</li>
    <li>📈 Prediction History per User</li>
    <li>🧾 PDF Report Generation</li>
    <li>🔒 Session-Based Access Control</li>
  </ul>

  <h2>🛠️ Tech Stack</h2>
  <ul>
    <li><strong>Framework:</strong> Flask</li>
    <li><strong>Machine Learning:</strong> TensorFlow / Keras</li>
    <li><strong>Database:</strong> SQLite</li>
    <li><strong>Frontend:</strong> Jinja2 + Bootstrap</li>
    <li><strong>PDF Generation:</strong> ReportLab</li>
  </ul>

  <h2>📦 Installation & Setup Guide</h2>

  <h3>1. Clone the Repository</h3>
  <pre>
git clone https://github.com/gunavardhanlomada/Marrow-Find
cd Marrow-Find
  </pre>

  <h3>2. Create a Virtual Environment</h3>
  <pre>
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
  </pre>

  <h3>3. Install Dependencies</h3>
  <pre>
pip install -r requirements.txt
  </pre>

  <h3>4. Download and Prepare the Dataset</h3>
  <p>Download the Kaggle dataset from the link above and place it in a folder (e.g. <code>datasets/</code>). Make sure your preprocessing or loading script points to the correct path.</p>

  <h3>5. Setup the Database</h3>
  <pre>
sqlite3 database.db &lt; schema.sql
  </pre>

  <h3>6. Ensure Model File Exists</h3>
  <p>Make sure the file <code>mymodel2.h5</code> is in the <code>model/</code> directory.</p>

  <h3>7. Run the Application</h3>
  <pre>
python app.py
  </pre>

  <p>Then open your browser and visit: <code>http://localhost:5000</code></p>

  <h2>📁 Project Structure</h2>
  <pre>
├── app.py
├── model/
│   └── mymodel2.h5
├── static/
│   ├── uploads/
│   └── output/
├── templates/
│   ├── index.html
│   ├── register.html
│   ├── dashboard.html
│   ├── result.html
│   └── about.html
├── database.db
├── schema.sql
├── requirements.txt
└── README.md
  </pre>

  <h2>📄 License</h2>
  <p>This project is open-source and available under the <a href="https://github.com/gunavardhanlomada/Volunteer-Verse/blob/main/LICENSE" target="_blank">MIT License</a>.</p>

</div>
