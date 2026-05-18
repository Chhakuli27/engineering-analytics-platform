WITH repositories AS (

    SELECT
        repo_name,
        language,
        stars,
        forks,
        created_at,
        updated_at

    FROM `engineering-analytics-platform.engineering_analytics.github_repositories`

)

SELECT
    repo_name,
    language,
    stars,
    forks,
    RANK() OVER (ORDER BY stars DESC) AS popularity_rank

FROM repositories