![](./assets/images/sonnet_scripts_banner.png)
# Sonnet Scripts
Sonnet Scripts is a collection of pre-built data architecture patterns that you can quickly spin up on a local machine, along with examples of real-world data that you can use with it.

## Why was Sonnet Scripts created?
One of the challenges of making content and tutorials on data is the lack of established data infrastructure and real-world datasets. I have often found myself repeating this process over and over again, therefore I decided to create an open-source repo to expedite this process.

## Why sonnets?
[According to the Academy of American Poets](https://poets.org/glossary/sonnet), a "...sonnet is a fourteen-line poem written in iambic pentameter, employing one of several rhyme schemes, and adhering to a tightly structured thematic organization." Through the constraints of a particular sonnet format, poets throughout centuries have pushed their creativity to express themselves-- William Shakespear being one of the most well-known. I've similarly seen data architectures fill the same role as a sonnet, where their specific patterns push data practioners to think of creative ways to solve business problems.



## How to use Sonnet Scripts


# 🏗 Sonnet Scripts - Data & Analytics Sandbox

## **Introduction**
Welcome to **Sonnet Scripts** – a fully containerized environment designed for **data analysts, analytics engineers, and data engineers** to experiment with databases, queries, and ETL pipelines. This repository provides a **pre-configured sandbox** where users can ingest data, transform it using SQL/Python, and test integrations with **PostgreSQL, DuckDB, and MinIO**.

## **Who is this for?**
This project is ideal for:
- **Data Engineers** who want a lightweight environment for testing data pipelines.
- **Analytics Engineers** experimenting with dbt and SQL transformations.
- **Data Analysts** looking for a structured PostgreSQL + DuckDB setup.
- **Developers** working on **data APIs** using Python and GoLang.

---

## **🛠 Prerequisites**
Before setting up the environment, ensure you have the following installed:

1. **Docker & Docker Compose**
   - [Install Docker](https://docs.docker.com/get-docker/)
   - [Install Docker Compose](https://docs.docker.com/compose/install/)

2. **Make (for automation)**
   - Linux/macOS: Comes pre-installed
   - Windows: Install via [Chocolatey](https://chocolatey.org/install) → `choco install make`

3. **Python (3.12+)**
   - [Install Python](https://www.python.org/downloads/)

---

## **🚀 Quick Start**
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/onthemarkdata/sonnet-scripts.git
cd sonnet-scrips
```

### **2️⃣ Start the Environment**
```sh
make setup
```
This will:
- Build the Docker images
- Start the PostgreSQL, DuckDB, and Minio containers
- Ensure dependencies are installed

### **3️⃣ Load Sample Data**
```sh
make load-db
```

### **4️⃣ Verify Data Loaded into Database**
```sh
make verify-db
```

### **5️⃣ Run Tests**
```sh
make test
```

### **6️⃣ Access the PythonBase Environment**
```sh
make exec-pythonbase
```

### **7️⃣ Access the PostgreSQL Database**
```sh
make exec-postgres
```

### **8️⃣ Access the DuckDB Database**
```sh
make exec-duckdb
```

## **📜 Project Structure**
```bash
📂 sonnet-scripts
│── 📂 pythonbase/         # Python-based processing container
│── 📂 linuxbase/          # Base container for Linux dependencies
│── 🐳 docker-compose.yml  # Container orchestration
│── 🛠 Makefile            # Automation commands
│── 📜 README.md           # You are here!
```

## **🛠 CI/CD Pipeline**
Github Actions automates builds, test, and environment validation. The pipeline:
1. Builds Docker images (`pythonbase`, `linuxbase`)
2. Starts all services using `docker compose`
3. Runs unit & integration tests (`make test`)
4. Shuts down containers after test pass.

#### **✅ CI is triggered on:**
- Push to `main` or `feature/*`
- Pull Requests to `main`

## **🤝 Contributing**
Want to improve Sonnet Scripts? Here's how:
1. Fork the repository
2. Make your changes and test them locally.
3. Submit a pull request (PR) for review.

For major changes, please open an issue first to discuss your proposal.

## **📧 Support & Questions**

If you have any questions, feel free to open an issue or reach out!
🚀 Happy data wrangling!