# Urgent Action Data Importer and API
An API to retrieve random or specific Urgent Action documents. Currently only delivers Stop Actions.

## Data Importer
The importer scans through all the .txt urgent actions and imports only those that have been identified as stop actions.
Importing stop actions consists in saving the textual content of the file into a MongoDB database.

## API
### GET /api/urgent-action/stop-action/random
Returns a random Urgent Action Stop Action document.

### GET /api/urgent-action/stop-action/\<ua_doc_id\>
Returns the Urgent Action Stop Action document specified by the given UA document id.
