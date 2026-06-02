# UsageAnalyticsResponse


## Fields

| Field                                                  | Type                                                   | Required                                               | Description                                            |
| ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ |
| `data`                                                 | List[[models.UsageBucket](../models/usagebucket.md)]   | :heavy_check_mark:                                     | Array of time buckets containing usage data            |
| `next_page_token`                                      | *OptionalNullable[str]*                                | :heavy_minus_sign:                                     | Pagination token for next page. Null if no more pages. |
| `total`                                                | *float*                                                | :heavy_check_mark:                                     | Total number of time buckets across all pages          |