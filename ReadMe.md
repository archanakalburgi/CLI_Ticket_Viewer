# Install
pyenv install 3.9.1
pyenv virtualenv 3.9.1 zen-desk
pyenv local zen-desk
pip install -r requirements.txt

# Update Credentials
In `src/creds.py`

Please update the user credentials

# Run
python main.py

A sample run video is here `sample_screencast.mov`


## Separation of concerns.
API module encapsulates all the logic to talk to the zendesk API.
Tickets module holds the "State" and the representation of the tickets.

## Error Handling
HTTP Error - Are handled and a message is displayed if there is error talking to API.
Parsing Error - Are handled and a message is displayed if there is error parsing the response. And tells this cannot be fixed by retrying.

## Testing
API responses are mocked and tests for HTTP error and parsing error are written.

## UI
Used Python's CMD module's loop to run the application.
