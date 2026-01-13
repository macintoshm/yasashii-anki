"""Anki Connect API client for interfacing with Anki desktop application"""

import os
import json
import requests
from urllib.parse import quote
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class AnkiClient:
    """Client for connecting to the Anki Connect API"""
    
    def __init__(self):
        self.api_url = os.getenv('ANKI_URL')
        self.deck_name = os.getenv('AUTO_ANKI_DECK_NAME')
    
    def post(self, payload):
        try:
            # Make POST request to Anki Connect API
            response = requests.post(self.api_url, json=payload, timeout=10)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Parse JSON response
            data = response.json()
            
            # Check if API returned an error
            if data.get('error') is not None:
                raise ValueError(f"Anki API error: {data['error']}")
            
            # Return the list of card IDs
            return data.get('result', [])
        except requests.exceptions.RequestException as e:
            raise requests.RequestException(f"Failed to connect to Anki Connect API at {self.api_url}: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response from Anki Connect API: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error while getting cards: {e}")


    def get_cards(self, deck=None):
        """
        Get cards from a specific deck
        
        Args:
            deck (str, optional): Name of the deck. If not provided, uses ANKI_DECK_NAME from .env
            
        Returns:
            list: List of card IDs from the deck
            
        Raises:
            requests.RequestException: If the API request fails
            ValueError: If the API returns an error
        """
        # Use provided deck name or fall back to environment variable
        target_deck = deck if deck is not None else self.deck_name
        
        # Prepare the API request payload
        payload = {
            "action": "findCards",
            "params": {"query": f"deck:{target_deck}"},
            "version": 6
        }
        return self.post(payload)

    def get_card_info(self, card_ids):
        """
        Get card information from a specific deck
        
        Args:
            card_ids (list): List of card IDs
            
        Returns:
            list: List of card information
        """
        if not isinstance(card_ids, list):
            card_ids = [card_ids]

        payload = {
                "action": "cardsInfo",
                "version": 6,
                "params": {
                    "cards": card_ids
                }
        }
        
        return self.post(payload)

    def _format_meanings_for_card(self, meanings_dict):
        """
        Format the meanings dictionary into a string suitable for Anki cards
        
        Args:
            meanings_dict (dict): Dictionary with part_of_speech -> glosses structure
            
        Returns:
            str: Formatted string for the Anki card
        """
        if not meanings_dict:
            return "No meanings found"
            
        formatted_meanings = []
        sense_number = 1
        for sense_key, glosses in meanings_dict.items():
            glosses_str = ', '.join(glosses)
            # Extract part of speech from sense key (format: "sense1 v5k-s, vi")
            pos = sense_key.split(' ', 1)[1] if ' ' in sense_key else sense_key
            formatted_meanings.append(f"{sense_number}. ({pos}) {glosses_str}<br><br>")
            sense_number += 1
        
        return '\n'.join(formatted_meanings)

    def _validate_audio_url(self, url):
        """
        Check if audio URL redirects to a valid CDN file

        Args:
            url (str): The LanguagePod101 audio URL to validate

        Returns:
            bool: True if audio exists, False otherwise
        """
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            # Valid audio redirects to CDN and returns 200
            return (response.status_code == 200 and
                    'cdn.innovativelanguage.com' in response.url)
        except requests.RequestException:
            return False

    def create_card(self, card_info):
        """
        Create a new card in the Anki deck
        
        Args:
            card_info (dict): Dictionary containing card information
        """
        card_type=os.getenv('AUTO_ANKI_CARD_TYPE')
        word_field=os.getenv('AUTO_ANKI_WORD_FIELD')
        reading_field=os.getenv('AUTO_ANKI_READING_FIELD')
        meaning_field=os.getenv('AUTO_ANKI_MEANING_FIELD')
        sentence_field=os.getenv('AUTO_ANKI_SENTENCE_FIELD')
        sentence_translation_field=os.getenv('AUTO_ANKI_SENTENCE_TRANSLATION_FIELD')
        audio_field=os.getenv('AUTO_ANKI_AUDIO_FIELD')

        # Build audio URL using kanji and kana reading
        kanji_list = card_info.get('kanji', [])
        readings_list = card_info.get('readings', [])
        word = card_info.get('word', '')

        # Use kanji if available, otherwise fall back to the word itself
        kanji = kanji_list[0] if kanji_list else word
        # Use reading if available, otherwise use the word (for kana-only words)
        kana = readings_list[0] if readings_list else word

        # URL encode the parameters for special characters
        audio_url = f"https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji={quote(kanji)}&kana={quote(kana)}"
        audio_filename = f"yasashii_{kana}_{kanji}.mp3"

        # Validate audio URL before adding to card
        audio_available = self._validate_audio_url(audio_url)

        # Initialize sentence variables with defaults
        sentence = ''
        sentence_translation = ''
        if card_info.get('examples'):
            example = card_info['examples'][0]
            sentence = example['sentences']['japanese']
            sentence_translation = example['sentences']['english']

        # Build note payload
        note = {
            "deckName": self.deck_name,
            "modelName": card_type,
            "fields": {
                word_field: card_info.get('word'),
                reading_field: ', '.join(card_info.get('readings', [])),
                meaning_field: self._format_meanings_for_card(card_info.get('meanings', {})),
                sentence_field: sentence if sentence else '',
                sentence_translation_field: sentence_translation if sentence_translation else '',
            },
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
                "duplicateScopeOptions": {
                    "deckName": self.deck_name,
                    "checkChildren": False,
                    "checkAllModels": False
                }
            },
            "tags": [
                "auto-anki"
            ]
        }

        # Only add audio if validation passed
        if audio_available:
            note["audio"] = [{
                "url": audio_url,
                "filename": audio_filename,
                "fields": [audio_field]
            }]

        payload = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": note
            }
        }

        result = self.post(payload)
        return {"note_id": result, "audio_available": audio_available, "deck_name": self.deck_name}
