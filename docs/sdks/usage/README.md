# Usage
(*usage*)

## Overview

Usage Analytics API endpoints

### Available Operations

* [get_voice_usage](#get_voice_usage) - Retrieve TTS API usage data
* [get_usage](#get_usage) - Retrieve advanced API usage analytics
* [get_credit_balance](#get_credit_balance) - Retrieve credit balance

## get_voice_usage

Retrieves a list of all TTS API usage records filtered by a specified date range. All dates are in UTC+0 timezone.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_voice_usage" method="get" path="/v1/voice-usage" -->
```python
from supertone import Supertone


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    res = s_client.usage.get_voice_usage(start_date="2024-11-01", end_date="2024-11-30")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `start_date`                                                        | *str*                                                               | :heavy_check_mark:                                                  | The start date in YYYY-MM-DD format.                                | 2024-11-01                                                          |
| `end_date`                                                          | *str*                                                               | :heavy_check_mark:                                                  | The end date in YYYY-MM-DD format.                                  | 2024-11-30                                                          |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.GetUsageListV1Response](../../models/getusagelistv1response.md)**

### Errors

| Error Type                   | Status Code                  | Content Type                 |
| ---------------------------- | ---------------------------- | ---------------------------- |
| errors.SupertoneDefaultError | 4XX, 5XX                     | \*/\*                        |

## get_usage

Retrieves API usage data with advanced features including time bucketing, multi-dimensional breakdowns, and pagination. All timestamps should be in RFC3339 format.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_usage" method="get" path="/v1/usage" -->
```python
from supertone import Supertone, models


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    res = s_client.usage.get_usage(start_time="2024-01-01T00:00:00+09:00", end_time="2024-01-31T23:59:59+09:00", bucket_width=models.BucketWidth.DAY, breakdown_type=[
        models.BreakdownType.VOICE_NAME,
    ], page_size=10)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `start_time`                                                        | *str*                                                               | :heavy_check_mark:                                                  | Start time in RFC3339 format                                        | 2024-01-01T00:00:00+09:00                                           |
| `end_time`                                                          | *str*                                                               | :heavy_check_mark:                                                  | End time in RFC3339 format                                          | 2024-01-31T23:59:59+09:00                                           |
| `bucket_width`                                                      | [Optional[models.BucketWidth]](../../models/bucketwidth.md)         | :heavy_minus_sign:                                                  | Time bucket width for aggregation                                   |                                                                     |
| `breakdown_type`                                                    | List[[models.BreakdownType](../../models/breakdowntype.md)]         | :heavy_minus_sign:                                                  | Dimensions to break down usage data                                 | [<br/>"voice_name"<br/>]                                            |
| `page_size`                                                         | *Optional[float]*                                                   | :heavy_minus_sign:                                                  | Number of results per page                                          |                                                                     |
| `next_page_token`                                                   | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | Pagination token from previous response                             |                                                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.UsageAnalyticsResponse](../../models/usageanalyticsresponse.md)**

### Errors

| Error Type                         | Status Code                        | Content Type                       |
| ---------------------------------- | ---------------------------------- | ---------------------------------- |
| errors.BadRequestErrorResponse     | 400                                | application/json                   |
| errors.UnauthorizedErrorResponse   | 401                                | application/json                   |
| errors.RequestTimeoutErrorResponse | 408                                | application/json                   |
| errors.InternalServerErrorResponse | 500                                | application/json                   |
| errors.SupertoneDefaultError       | 4XX, 5XX                           | \*/\*                              |

## get_credit_balance

Retrieves credit balance of the user.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_credit_balance" method="get" path="/v1/credits" -->
```python
from supertone import Supertone


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    res = s_client.usage.get_credit_balance()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetCreditBalanceResponse](../../models/getcreditbalanceresponse.md)**

### Errors

| Error Type                   | Status Code                  | Content Type                 |
| ---------------------------- | ---------------------------- | ---------------------------- |
| errors.SupertoneDefaultError | 4XX, 5XX                     | \*/\*                        |