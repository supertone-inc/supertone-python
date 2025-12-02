# CreateSpeechResponseBody

JSON response with base64 audio and phoneme data (when include_phonemes=true)


## Fields

| Field                                                             | Type                                                              | Required                                                          | Description                                                       | Example                                                           |
| ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- |
| `audio_base64`                                                    | *str*                                                             | :heavy_check_mark:                                                | Base64 encoded audio data                                         | UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhY... |
| `phonemes`                                                        | [Optional[models.Phonemes]](../models/phonemes.md)                | :heavy_minus_sign:                                                | Phoneme timing data with IPA symbols                              |                                                                   |