import json

import requests


# Exception if reach limit in API
class ElevenLabsLimitException(Exception):
    pass


class ElevenLabsAPI:

    def __init__(self, api_key):
        self.api_key = api_key
        self.url_base = 'https://api.elevenlabs.io/v1/'
        self.get_voices()

    def get_voices(self):
        '''Get the list of voices available'''
        url = self.url_base + 'voices'
        headers = {'accept': 'application/json'}
        if self.api_key:
            headers['xi-api-key'] = self.api_key
        response = requests.get(url, headers=headers)
        self.voices = {voice['name']: voice['voice_id'] for voice in response.json()['voices']}
        return self.voices

    def get_remaining_characters(self):
        '''Get the number of characters remaining'''
        url = self.url_base + 'user'
        headers = {'accept': '*/*', 'xi-api-key': self.api_key, 'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            sub = response.json()['subscription']
            return sub['character_limit'] - sub['character_count']
        else:
            raise Exception(response.json()['detail']['message'])

    def generate_voice(self, text, character, filename, stability=0.2, clarity=0.1, voice_id=None):
        '''Generate a voice'''
        # If voice_id is provided directly, use it
        if voice_id:
            pass  # use the provided voice_id
        elif character in self.voices:
            voice_id = self.voices[character]
        else:
            # Assume character is a voice_id if not found in voices list
            print(f"'{character}' not found in voices list, using as voice_id directly")
            voice_id = character
        url = f'{self.url_base}text-to-speech/{voice_id}/stream'
        headers = {'accept': '*/*', 'xi-api-key': self.api_key, 'Content-Type': 'application/json'}
        data = json.dumps(
            {"model_id": "eleven_v3", "text": text, "stability": stability, "similarity_boost": clarity})
        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
                return filename
        else:
            message = response.text
            raise Exception(f'Error in response, {response.status_code} , message: {message}')
