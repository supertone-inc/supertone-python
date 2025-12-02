# Phonemes

Phoneme timing data with IPA symbols


## Fields

| Field                                       | Type                                        | Required                                    | Description                                 | Example                                     |
| ------------------------------------------- | ------------------------------------------- | ------------------------------------------- | ------------------------------------------- | ------------------------------------------- |
| `symbols`                                   | List[*str*]                                 | :heavy_minus_sign:                          | List of IPA phonetic symbols                | [<br/>"",<br/>"h",<br/>"ɐ",<br/>"ɡ",<br/>"ʌ",<br/>""<br/>] |
| `start_times_seconds`                       | List[*float*]                               | :heavy_minus_sign:                          | Start times for each phoneme in seconds     | [<br/>0,<br/>0.092,<br/>0.197,<br/>0.255,<br/>0.29,<br/>0.58<br/>] |
| `durations_seconds`                         | List[*float*]                               | :heavy_minus_sign:                          | Duration for each phoneme in seconds        | [<br/>0.092,<br/>0.104,<br/>0.058,<br/>0.034,<br/>0.29,<br/>0.162<br/>] |