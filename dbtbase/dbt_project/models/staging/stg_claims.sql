{{
  config(
    materialized='view',
    tags=['staging', 'claims']
  )
}}

{#
  Staging model for raw claims data.
  Queries PostgreSQL directly using DuckDB's postgres_scanner extension.
  Performs basic type casting and cleaning.
#}

with source as (
    select * from postgres_scan(
        '{{ var("pg_connection_string") }}',
        'public',
        'raw_claims'
    )
),

cleaned as (
    select
        -- Patient identifier
        DESYNPUF_ID as patient_id,

        -- Claim identifier
        CLM_ID as claim_id,

        -- Date fields (keeping as text for now, cast in downstream models if needed)
        CLM_FROM_DT as claim_from_date,
        CLM_THRU_DT as claim_thru_date,

        -- Diagnosis codes (first 4)
        ICD9_DGNS_CD_1 as diagnosis_code_1,
        ICD9_DGNS_CD_2 as diagnosis_code_2,
        ICD9_DGNS_CD_3 as diagnosis_code_3,
        ICD9_DGNS_CD_4 as diagnosis_code_4,

        -- Provider NPIs (first 4)
        PRF_PHYSN_NPI_1 as provider_npi_1,
        PRF_PHYSN_NPI_2 as provider_npi_2,
        PRF_PHYSN_NPI_3 as provider_npi_3,
        PRF_PHYSN_NPI_4 as provider_npi_4,

        -- HCPCS/Procedure codes (first 4)
        HCPCS_CD_1 as procedure_code_1,
        HCPCS_CD_2 as procedure_code_2,
        HCPCS_CD_3 as procedure_code_3,
        HCPCS_CD_4 as procedure_code_4,

        -- Payment amounts (first 4 line items)
        try_cast(LINE_NCH_PMT_AMT_1 as decimal(10,2)) as payment_amount_1,
        try_cast(LINE_NCH_PMT_AMT_2 as decimal(10,2)) as payment_amount_2,
        try_cast(LINE_NCH_PMT_AMT_3 as decimal(10,2)) as payment_amount_3,
        try_cast(LINE_NCH_PMT_AMT_4 as decimal(10,2)) as payment_amount_4,

        -- Allowed charge amounts (first 4 line items)
        try_cast(LINE_ALOWD_CHRG_AMT_1 as decimal(10,2)) as allowed_amount_1,
        try_cast(LINE_ALOWD_CHRG_AMT_2 as decimal(10,2)) as allowed_amount_2,
        try_cast(LINE_ALOWD_CHRG_AMT_3 as decimal(10,2)) as allowed_amount_3,
        try_cast(LINE_ALOWD_CHRG_AMT_4 as decimal(10,2)) as allowed_amount_4,

        -- Metadata
        current_timestamp as dbt_loaded_at

    from source
)

select * from cleaned
where claim_id is not null
