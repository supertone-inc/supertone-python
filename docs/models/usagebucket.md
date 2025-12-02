# UsageBucket


## Fields

| Field                                                | Type                                                 | Required                                             | Description                                          | Example                                              |
| ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- |
| `starting_at`                                        | *str*                                                | :heavy_check_mark:                                   | RFC3339 timestamp for bucket start                   | 2024-01-01T00:00:00+09:00                            |
| `ending_at`                                          | *str*                                                | :heavy_check_mark:                                   | RFC3339 timestamp for bucket end                     | 2024-01-01T01:00:00+09:00                            |
| `results`                                            | List[[models.UsageResult](../models/usageresult.md)] | :heavy_check_mark:                                   | Array of usage results within this time bucket       |                                                      |