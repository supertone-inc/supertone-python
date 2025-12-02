# CreateClonedVoiceRequest

Audio file and voice metadata


## Fields

| Field                                                    | Type                                                     | Required                                                 | Description                                              |
| -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| `files`                                                  | [models.Files](../models/files.md)                       | :heavy_check_mark:                                       | Audio file to clone voice from (WAV/MP3 format, max 3MB) |
| `name`                                                   | *str*                                                    | :heavy_check_mark:                                       | Name of the cloned voice                                 |
| `description`                                            | *Optional[str]*                                          | :heavy_minus_sign:                                       | Description of the cloned voice                          |