## Installation and Setup Instructions

### 1. Install Ollama

Start by installing Ollama by running the following command in your terminal (https://ollama.com/download):

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Once the installation is complete, pull the llama3 model:

```bash
ollama pull llama3
```

By default, Ollama runs on port 11434, but if another application is already using this port, you can check which port Ollama is using with the following command:

```bash
lsof -i -P | grep LISTEN | grep ollama
```

If necessary, you can change the port by editing the OLLAMA value in config.ini file.

### 2. Creating a Virtual Environment

Create a virtual environment:

```bash
python3 -m venv venv
```

### 3. Activating the Virtual Environment
Activate the virtual environment by running:


```bash
source venv/bin/activate
```

### 4. Installing Dependencies
After activating the virtual environment, install the required dependencies by running:

```bash
pip install -r requirements.txt
```

### 5. Running the Project
```bash
python main.py
```

After running the project, a link will be printed in the terminal, such as:

```
* Running on local URL: http://127.0.0.1:7860
```

### 6. Demo

https://github.com/user-attachments/assets/26644058-9359-4ace-ad2b-caba83e86613
