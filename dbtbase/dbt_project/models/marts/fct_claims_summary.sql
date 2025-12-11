{{
  config(
    materialized='table',
    tags=['marts', 'claims', 'summary']
  )
}}

{#
  Patient-level claims summary mart.
  Aggregates claims data by patient to provide key metrics.
#}

with staged_claims as (
    select * from {{ ref('stg_claims') }}
),

aggregated as (
    select
        patient_id,

        -- Claim counts
        count(distinct claim_id) as total_claims,

        -- Date range
        min(claim_from_date) as first_claim_date,
        max(claim_thru_date) as last_claim_date,

        -- Diagnosis diversity (count of unique primary diagnoses)
        count(distinct diagnosis_code_1) as distinct_primary_diagnoses,

        -- Provider diversity
        count(distinct provider_npi_1) as distinct_primary_providers,

        -- Procedure diversity
        count(distinct procedure_code_1) as distinct_primary_procedures,

        -- Payment totals (sum across first 4 line items)
        coalesce(sum(payment_amount_1), 0) +
        coalesce(sum(payment_amount_2), 0) +
        coalesce(sum(payment_amount_3), 0) +
        coalesce(sum(payment_amount_4), 0) as total_payment_amount,

        -- Allowed charge totals
        coalesce(sum(allowed_amount_1), 0) +
        coalesce(sum(allowed_amount_2), 0) +
        coalesce(sum(allowed_amount_3), 0) +
        coalesce(sum(allowed_amount_4), 0) as total_allowed_amount,

        -- Average payment per claim
        case
            when count(distinct claim_id) > 0 then
                (coalesce(sum(payment_amount_1), 0) +
                 coalesce(sum(payment_amount_2), 0) +
                 coalesce(sum(payment_amount_3), 0) +
                 coalesce(sum(payment_amount_4), 0)) / count(distinct claim_id)
            else 0
        end as avg_payment_per_claim,

        -- Metadata
        current_timestamp as dbt_created_at

    from staged_claims
    group by patient_id
)

select * from aggregated
where total_claims > 0
