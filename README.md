# BookBot — AI-Powered Book Recommendation Chatbot

A domain-specific book recommendation chatbot built using a fine-tuned TinyLlama 1.1B model and a Django web application. The system uses a hybrid AI routing approach — routing book queries to a custom fine-tuned model and general conversation to Groq's LLaMA 3.1 8B.

---

## Project Overview

BookBot fine-tunes a Large Language Model on a real book dataset using parameter-efficient techniques (LoRA) and serves it through a Django web application. All conversations are stored in a database and accessible via Django Admin.

---

## Architecture

```bash
User → Django Web App → services.py
                            ↓
                    Is it a book query?
                   YES ↓           NO ↓
              Colab API          Groq API
          (Fine-tuned          (LLaMA 3.1 8B)
           TinyLlama)
                   ↓               ↓
              Reply saved to SQLite DB
                        ↓
               Shown in chat UI
```

---

## Technology Stack
```bash
### Model Training
| Tool                     | Purpose                         |
|--------------------------|---------------------------------|
| TinyLlama 1.1B           | Base language model             |
| HuggingFace Transformers | Model loading and inference     |
| PEFT (LoRA)              | Parameter efficient fine-tuning |
| BitsAndBytes             | 4-bit quantization              |
| TRL (SFTTrainer)         | Supervised fine-tuning          |
| Google Colab T4 GPU      | Training environment            |

### Web Application
| Tool          | Purpose                             |
|---------------|-------------------------------------|
| Django        | Web framework                       |
| SQLite        | Database                            |
| Django Admin  | Conversation management             |
| Groq API      | General conversation (LLaMA 3.1 8B) |
| Flask + ngrok | Serving fine-tuned model as API     |
```
---

## Project Structure

```bash
BookBot/
├── BookBot/                  ← Django project settings
│   ├── settings.py
│   └── urls.py
├── BookApp/                  ← Main application
│   ├── models.py             ← Message and Suggestions models
│   ├── views.py              ← Request handling
│   ├── services.py           ← AI routing logic
│   ├── urls.py               ← URL routes
│   └── templates/
│       ├── base.html         ← Base template
│       └── home.html         ← Chat interface
├── .env                      ← API keys (not committed)
├── .gitignore
├── requirements.txt
└── manage.py
```

---

## Model Details

```bash
| Property         | Value                                   |
|------------------|-----------------------------------------|
| Base Model       | TinyLlama/TinyLlama-1.1B-Chat-v1.0      |
| Fine-tuned Model | MuskanTara/tinyllama-finetuned-books-v2 |
| Dataset          | swayista/book-recommender-dataset       |
| Training Samples | 5000                                    |
| Epochs           | 2                                       |
| LoRA Rank (r)    | 32                                      |
| LoRA Alpha       | 64                                      |
| Learning Rate    | 2e-4                                    |
| Training Loss    | 1.87                                    |  
| Quantization     | 4-bit NF4                               |

```
---

## Setup and Installation

### 1. Clone the repository
```bash
git clone https://github.com/Muskan-Tarafder/BookBot.git
cd BookBot
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
```
GROQ_API_KEY=your_groq_api_key
HF_API_URL=your_ngrok_url/predict
SECRET_KEY=your_django_secret_key
DEBUG=True
```

### 5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Add suggestions via Admin
```bash
python manage.py runserver
```
Go to `http://127.0.0.1:8000/admin` and add suggestion buttons under the Suggestions model.

---

## Running the Fine-tuned Model (Colab API)

1. Open `LLM_Chatbot.ipynb` in Google Colab
2. Run the Flask API cell — it will print a public ngrok URL
3. Copy the URL and paste it in your `.env` file as `HF_API_URL`
4. Keep the Colab tab open while using the Django app

---

## Usage

1. Start Django server: `python manage.py runserver`
2. Open `http://127.0.0.1:8000`
3. Click a suggestion or type a book query
4. Book queries → answered by fine-tuned TinyLlama
5. General conversation → answered by Groq LLaMA 3.1
6. View all conversations at `http://127.0.0.1:8000/admin`

---

## Evaluation Results

```bash
| Metric             | Score     |
|--------------------|-----------|
| BLEU Score         | 0.0037    |
| ROUGE-1            | 0.1095    |
| ROUGE-L            | 0.0998    |
| Training Loss (v1) | 1.91      |
| Training Loss (v2) | 1.87      |
```
> Note: Low BLEU/ROUGE scores are expected for open-ended generation tasks. These metrics measure word overlap against a single reference answer, which is not suitable for book recommendations where many valid answers exist.

---

## Limitations

- Fine-tuned model occasionally hallucinates book titles and authors
- Requires Colab session to be active for fine-tuned model to work
- Falls back to Groq automatically if Colab goes offline
- ngrok URL changes every time Colab restarts and must be updated in `.env`

---

## Future Improvements

- Retrain with 10+ epochs and larger dataset for better accuracy
- Deploy model on dedicated GPU server to remove Colab dependency
- Replace keyword routing with intent classification for smarter routing
- Add user authentication for personalized recommendation history
- Upgrade to Mistral 7B for significantly better response quality

---

## Requirements

```
django
groq
python-dotenv
requests
peft
transformers
torch
bitsandbytes
trl
datasets
flask
pyngrok
```

---

## Links

- Fine-tuned Model v1: https://huggingface.co/MuskanTara/tinyllama-finetuned-books
- Fine-tuned Model v2: https://huggingface.co/MuskanTara/tinyllama-finetuned-books-v2
- Dataset: https://huggingface.co/datasets/swayista/book-recommender-dataset
- Base Model: https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0

---

## Author

Muskan Tarafder
