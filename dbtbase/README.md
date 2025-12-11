# dbtbase - dbt for DuckDB Transformations

This container provides dbt (data build tool) configured to run transformations using DuckDB with the `postgres_scanner` extension to query PostgreSQL directly.

## Quick Start

### 1. Install dbt packages
```bash
make dbt-deps
```

### 2. Test connection
```bash
make dbt-debug
```

### 3. Run dbt models
```bash
make dbt-run
```

### 4. Run dbt tests
```bash
make dbt-test
```

### 5. Complete workflow (deps + run + test)
```bash
make dbt-build
```

## Data Flow

```
PostgreSQL (pgduckdb)
    |
    | raw_claims table (loaded via pipelinebase)
    |
    v (postgres_scanner extension)
DuckDB (/apps/dbt.duckdb)
    |
    | dbt transformations
    |
    +-- staging.stg_claims (view)
    |
    +-- marts.fct_claims_summary (table)
```

## Project Structure

```
dbt_project/
  dbt_project.yml    # Project configuration
  profiles.yml       # Connection profiles
  packages.yml       # dbt packages (dbt-utils, dbt-expectations)
  models/
    staging/         # Cleaned views of raw data
      stg_claims.sql
    marts/           # Business-ready aggregated tables
      fct_claims_summary.sql
    schema.yml       # Model documentation and tests
  macros/            # Reusable SQL functions
  seeds/             # Static reference data (CSV files)
  tests/             # Custom data quality tests
```

## Available Makefile Commands

| Command | Description |
|---------|-------------|
| `make exec-dbtbase` | Open shell in dbtbase container |
| `make dbt-debug` | Test dbt connection |
| `make dbt-deps` | Install dbt packages |
| `make dbt-run` | Run all dbt models |
| `make dbt-test` | Run dbt tests |
| `make dbt-build` | Run deps + run + test |
| `make dbt-run-model model=stg_claims` | Run specific model |
| `make dbt-compile` | Compile SQL without running |
| `make dbt-docs-generate` | Generate documentation |
| `make verify-dbt` | Check transformed data in DuckDB |

## Connection Profiles

### dev (default)
- Uses DuckDB at `/apps/dbt.duckdb`
- Queries PostgreSQL via `postgres_scanner` extension
- Best for: Interactive development, learning

### prod
- Uses separate DuckDB at `/apps/dbt_prod.duckdb`
- Best for: CI/CD, isolated testing

Switch profiles:
```bash
DBT_TARGET=prod make dbt-run
```

## Creating Your Own dbt Project

### Option 1: Modify in Place
Edit files in `dbtbase/dbt_project/` and rebuild:
```bash
make rebuild
```

### Option 2: Volume Mount for Live Development
Uncomment the volume mount in `docker-compose.yml`:
```yaml
volumes:
  - ./dbtbase/dbt_project:/apps/dbt_project
```

Then restart:
```bash
make stop && make setup
```

Now you can edit files on your host machine and run dbt immediately without rebuilds.

### Option 3: Create Custom Project from Scratch
1. Fork the repository
2. Create your own models in `dbtbase/dbt_project/models/`
3. Update `dbt_project.yml` with your project name
4. Commit and rebuild

## Example Models

### stg_claims.sql
Staging model that:
- Queries `raw_claims` from PostgreSQL using `postgres_scan()`
- Renames columns to snake_case
- Casts payment amounts to decimal
- Filters null claim IDs

### fct_claims_summary.sql
Mart model that:
- Aggregates claims by patient
- Calculates total and average payments
- Counts distinct diagnoses, providers, procedures

## Data Quality Tests

Tests are defined in `models/schema.yml`:
- **Generic tests**: `not_null`, `unique`
- **dbt-expectations**: Value range validation

## Troubleshooting

### Connection Issues
```bash
make dbt-debug
```

### View DuckDB contents
```bash
make exec-dbtbase
duckdb /apps/dbt.duckdb
.tables
SELECT * FROM staging.stg_claims LIMIT 10;
```

### Clear dbt artifacts
```bash
make exec-dbtbase
rm -rf /apps/dbt_project/target/*
rm -rf /apps/dbt_project/dbt_packages/*
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DBT_TARGET` | `dev` | Which profile to use |
| `DB_HOST` | `pgduckdb` | PostgreSQL host |
| `DB_USER` | `postgres` | PostgreSQL user |
| `DB_PASSWORD` | `postgres` | PostgreSQL password |
| `DB_NAME` | `postgres` | PostgreSQL database |
