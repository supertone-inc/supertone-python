# Voices
(*voices*)

## Overview

Voice Library API endpoints

### Available Operations

* [list_voices](#list_voices) - Gets available voices
* [search_voices](#search_voices) - Search voices.
* [get_voice](#get_voice) - Get voice details by ID

## list_voices

Gets a paginated list of voices available to the user based on internal group logic, using token-based pagination.

### Example Usage

<!-- UsageSnippet language="python" operationID="list_voices" method="get" path="/v1/voices" -->
```python
from supertone import Supertone


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    res = s_client.voices.list_voices()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `page_size`                                                         | *Optional[float]*                                                   | :heavy_minus_sign:                                                  | Number of items per page (default: 20, min: 10, max: 100)           |
| `next_page_token`                                                   | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | Token for pagination (obtained from the previous page's response)   |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetAPICharacterListResponse](../../models/getapicharacterlistresponse.md)**

### Errors

| Error Type                   | Status Code                  | Content Type                 |
| ---------------------------- | ---------------------------- | ---------------------------- |
| errors.SupertoneDefaultError | 4XX, 5XX                     | \*/\*                        |

## search_voices

Search and filter voices based on various parameters.

### Example Usage

<!-- UsageSnippet language="python" operationID="search_voices" method="get" path="/v1/voices/search" -->
```python
from supertone import Supertone


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    res = s_client.voices.search_voices()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                                            | Type                                                                                                                                                                                                                                                                                                                                 | Required                                                                                                                                                                                                                                                                                                                             | Description                                                                                                                                                                                                                                                                                                                          |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `page_size`                                                                                                                                                                                                                                                                                                                          | *Optional[float]*                                                                                                                                                                                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                   | Number of items per page (default: 20, min: 10, max: 100)                                                                                                                                                                                                                                                                            |
| `next_page_token`                                                                                                                                                                                                                                                                                                                    | *Optional[str]*                                                                                                                                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                   | Token for pagination (obtained from the previous page's response)                                                                                                                                                                                                                                                                    |
| `name`                                                                                                                                                                                                                                                                                                                               | *Optional[str]*                                                                                                                                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                   | Search across name. Space separated.                                                                                                                                                                                                                                                                                                 |
| `description`                                                                                                                                                                                                                                                                                                                        | *Optional[str]*                                                                                                                                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                   | Search across description. Space separated.                                                                                                                                                                                                                                                                                          |
| `language`                                                                                                                                                                                                                                                                                                                           | *Optional[str]*                                                                                                                                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                   | Filter by language (comma-separated)                                                                                                                                                                                                                                                                                                 |
| `gender`                                                                                                                                                                                                                                                                                                                             | *Optional[str]*                                                                                                                                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                   | Filter by gender (comma-separated)                                                                                                                                                                                                                                                                                                   |
| `age`                                                                                                                                                                                                                                                                                                                                | *Optional[str]*                                                                                                                                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                   | Filter by age (comma-separated)                                                                                                                                                                                                                                                                                                      |
| `use_case`                                                                                                                                                                                                                                                                                                                           | *Optional[str]*                                                                                                                                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                   | Filter by use case (comma-separated)                                                                                                                                                                                                                                                                                                 |
| `use_cases`                                                                                                                                                                                                                                                                                                                          | *Optional[str]*                                                                                                                                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                   | Filter by use cases array (comma-separated for OR logic)                                                                                                                                                                                                                                                                             |
| `style`                                                                                                                                                                                                                                                                                                                              | *Optional[str]*                                                                                                                                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                   | Filter by style (comma-separated for OR, semicolon-separated for AND). Mixing comma and semicolon is invalid and will result in 400. Note: AND semantics apply across styles on a single character; cloned voices have a single style and will only match AND when exactly one style is requested and equals the cloned voice style. |
| `model`                                                                                                                                                                                                                                                                                                                              | *Optional[str]*                                                                                                                                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                   | Filter by model (comma-separated)                                                                                                                                                                                                                                                                                                    |
| `retries`                                                                                                                                                                                                                                                                                                                            | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                                     | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                   | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                                  |

### Response

**[models.GetAPICharacterListResponse](../../models/getapicharacterlistresponse.md)**

### Errors

| Error Type                   | Status Code                  | Content Type                 |
| ---------------------------- | ---------------------------- | ---------------------------- |
| errors.SupertoneDefaultError | 4XX, 5XX                     | \*/\*                        |

## get_voice

Gets detailed information about a specific voice by its voice ID. Only supports preset voices.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_voice" method="get" path="/v1/voices/{voice_id}" -->
```python
from supertone import Supertone


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    res = s_client.voices.get_voice(voice_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `voice_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetCharacterByIDResponse](../../models/getcharacterbyidresponse.md)**

### Errors

| Error Type                   | Status Code                  | Content Type                 |
| ---------------------------- | ---------------------------- | ---------------------------- |
| errors.SupertoneDefaultError | 4XX, 5XX                     | \*/\*                        |