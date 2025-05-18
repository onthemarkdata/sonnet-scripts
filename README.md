![](./assets/images/sonnet_scripts_banner.png)
# Sonnet Scripts
Sonnet Scripts is a collection of pre-built data architecture patterns that you can quickly spin up on a local machine, along with examples of real-world data that you can use with it.

## Why was Sonnet Scripts created?
One of the challenges of making content and tutorials on data is the lack of established data infrastructure and real-world datasets. I have often found myself repeating this process over and over again, therefore we decided to create an open-source repo to expedite this process.

## Why sonnets?
[According to the Academy of American Poets](https://poets.org/glossary/sonnet), a "...sonnet is a fourteen-line poem written in iambic pentameter, employing one of several rhyme schemes, and adhering to a tightly structured thematic organization." Through the constraints of a particular sonnet format, poets throughout centuries have pushed their creativity to express themselves-- William Shakespear being one of the most well-known. I've similarly seen data architectures fill the same role as a sonnet, where their specific patterns push data practioners to think of creative ways to solve business problems.



## How to use Sonnet Scripts


# 🏗 Sonnet Scripts - Data & Analytics Sandbox

## **Introduction**
Welcome to **Sonnet Scripts** – a fully containerized environment designed for **data analysts, analytics engineers, and data engineers** to experiment with databases, queries, and ETL pipelines. This repository provides a **pre-configured sandbox** where users can ingest data, transform it using SQL/Python, and test integrations with **PostgreSQL, DuckDB, MinIO** and more!

## **Who is this for?**
This project is ideal for:
- **Data Engineers** who want a lightweight environment for testing data pipelines.
- **Analytics Engineers** experimenting with dbt and SQL transformations.
- **Data Analysts** looking for a structured PostgreSQL + DuckDB setup.
- **Developers** working on **data APIs** using Python.

---

## **🛠 Prerequisites**
Before setting up the environment, ensure you have the following installed:

1. **Docker & Docker Compose**
   - [Install Docker](https://docs.docker.com/get-docker/)
   - [Install Docker Compose](https://docs.docker.com/compose/install/)

2. **[Make](https://www.gnu.org/software/make/) (for automation)**
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
- Start the PostgreSQL, DuckDB, and other containers
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

### **6️⃣ Access the PythonBase Command Line Interface (CLI)**
```sh
make exec-pythonbase
```

### **7️⃣ Access the PostgreSQL Database**
```sh
make exec-postgres
```

### **8️⃣ Access the DuckDB CLI**
```sh
make exec-duckdb
```

### **9️⃣ Access the Pipeline Container CLI**
```sh
make exec-pipelinebase
```

### **🔄 Data Pipeline Commands**

#### **Export Data from PostgreSQL to MinIO**
```sh
make load-db-postgres-to-minio
```
This command:
- Exports a sample of data from PostgreSQL to CSV
- Transfers the CSV to the pipelinebase container
- Converts the CSV to Parquet and uploads to MinIO
- Cleans up temporary files

#### **Import Data from MinIO to DuckDB**
```sh
make load-db-minio-to-duckdb
```

#### **Check MinIO Status and Contents**
```sh
make check-minio
```

#### **Verify Data in DuckDB**
```sh
make check-duckdb
```

#### **Run the Complete Data Pipeline**
```sh
make run-all-data-pipelines
```
This runs the entire ETL process from PostgreSQL to MinIO to DuckDB.

### **🧹 Environment Management**

#### **Stop All Containers**
```sh
make stop
```

#### **Rebuild Containers**
```sh
make rebuild
```

#### **Complete Rebuild (Clean)**
```sh
make rebuild-clean
```
This removes all containers, volumes, and images before rebuilding from scratch.

#### **Check Container Status**
```sh
make status
```

#### **View Container Logs**
```sh
make logs
```
For a specific container: `make logs c=container_name`

## **📜 Project Structure**
```bash
📂 sonnet-scripts
│── 📂 pythonbase/         # Python-based processing container
│── 📂 pipelinebase/       # ETL pipeline and data ingest container
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
2. Make your changes and test them locally
3. Submit a pull request (PR) for review

For major changes, please open an issue first to discuss your proposal.

We follow [Conventional Commits](https://www.conventionalcommits.org/) for all commit messages.

## **📧 Support & Questions**

Maintained by:
- [Juan Pablo Urrutia]
   **GitHub**: [jpurrutia](https://github.com/jpurrutia)
   **LinkedIn**: [Juan Pablo Urrutia](https://www.linkedin.com/in/jpurrutia/)

- [Mark Freeman]
   **GitHub**: [onthemarkdata](https://github.com/onthemarkdata)
   **LinkedIn**:

If you have questions or encounter issues, feel free to:
- Open a GitHub issue
- Contact directly via LinkedIn
- COMING SOON: Join our [Discord community](https://discord.gg/your-invite-link)

🚀 Happy data wrangling!
