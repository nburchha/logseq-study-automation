---
name: call-anki-connect
description: Sends a structured JSON payload to the local Anki desktop application via the AnkiConnect API to automatically generate flashcards.
---
# Skill: call-anki-connect

## Schema
### Inputs
```json
{
  "type": "object",
  "properties": {
    "deck_name": {
      "type": "string",
      "description": "The name of the destination Anki deck."
    },
    "model_name": {
      "type": "string",
      "description": "The note type in Anki (e.g., 'Basic', 'Cloze')."
    },
    "cards": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "front": { "type": "string", "description": "The front side of the card (HTML supported)." },
          "back": { "type": "string", "description": "The back side of the card (HTML supported)." },
          "tags": {
            "type": "array",
            "items": { "type": "string" },
            "description": "List of tags to apply to the card."
          }
        },
        "required": ["front", "back"]
      },
      "description": "An array of flashcard objects to be added."
    }
  },
  "required": ["deck_name", "model_name", "cards"]
}
```

### Outputs
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "True if the notes were successfully added to Anki."
    },
    "created_ids": {
      "type": "array",
      "items": { "type": "integer" },
      "description": "List of the newly created Note IDs in Anki."
    },
    "errors": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Any error messages returned by AnkiConnect."
    }
  }
}
```

## Logic
1. Ensure the AnkiConnect API URL is targeted at `http://localhost:8765`.
2. Construct the payload for the `addNotes` action:
   ```json
   {
       "action": "addNotes",
       "version": 6,
       "params": {
           "notes": [ ... mapped from inputs ... ]
       }
   }
   ```
3. Issue an HTTP POST request to AnkiConnect.
4. Parse the JSON response. Extract `result` (the array of generated IDs) and `error`.
5. If `error` is present, return `success: false` and populate the `errors` output.
6. If successful, return `success: true` and the `created_ids`.
