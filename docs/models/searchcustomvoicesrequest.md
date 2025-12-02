# SearchCustomVoicesRequest


## Fields

| Field                                                             | Type                                                              | Required                                                          | Description                                                       |
| ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- |
| `page_size`                                                       | *Optional[float]*                                                 | :heavy_minus_sign:                                                | Number of items per page (default: 20, min: 10, max: 100)         |
| `next_page_token`                                                 | *Optional[str]*                                                   | :heavy_minus_sign:                                                | Token for pagination (obtained from the previous page's response) |
| `name`                                                            | *Optional[str]*                                                   | :heavy_minus_sign:                                                | Search across name. Space separated.                              |
| `description`                                                     | *Optional[str]*                                                   | :heavy_minus_sign:                                                | Search across description. Space separated.                       |