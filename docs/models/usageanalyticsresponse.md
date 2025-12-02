# UsageAnalyticsResponse


## Fields

| Field                                                | Type                                                 | Required                                             | Description                                          |
| ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- |
| `data`                                               | List[[models.UsageBucket](../models/usagebucket.md)] | :heavy_check_mark:                                   | Array of time buckets containing usage data          |
| `next_page_token`                                    | *Optional[str]*                                      | :heavy_minus_sign:                                   | Pagination token for next page                       |
| `total`                                              | *float*                                              | :heavy_check_mark:                                   | Total number of time buckets across all pages        |