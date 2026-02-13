# Yasashii Anki

A CLI and GUI tool for automatically creating Anki flashcards from Japanese words. Look up any Japanese word and instantly create a flashcard with readings, meanings, example sentences, and audio pronunciation.

## Features

- **Dictionary Lookup**: Search 200,000+ Japanese words using JMDict
- **Auto Card Creation**: Create Anki cards with one command
- **Audio Pronunciation**: Automatically adds audio from JapanesePod101
- **Example Sentences**: Includes example sentences with translations
- **Multiple Meanings**: Shows all word meanings with parts of speech
- **GUI Interface**: Easy-to-use graphical interface for batch processing
- **Batch Processing**: Process multiple words from command line or file

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/macintoshm/yasashii-anki.git
cd yasashii-anki

# 2. Run the setup script
./scripts/setup.sh

# 3. Make sure Anki is running with AnkiConnect installed

# 4. Look up a word
yasashii 猫

# 5. Look up and create a card
yasashii 猫 -c
```

## Important: Anki Must Be Running

**To create cards, you must have:**
1. **Anki desktop app open and running**
2. **AnkiConnect addon installed** ([Get it here](https://ankiweb.net/shared/info/2055492159))

Yasashii communicates with Anki through AnkiConnect's local API. If Anki isn't running, you can still look up words, but card creation will fail.

## Prerequisites

- **Python 3.13+**
- **[uv](https://github.com/astral-sh/uv)** - Python package manager (setup script will install this)
- **[Anki](https://apps.ankiweb.net/)** - Desktop app (must be running when creating cards)
- **[AnkiConnect](https://ankiweb.net/shared/info/2055492159)** - Anki addon for API access

## Installation

### Option 1: Automated Setup (Recommended)

```bash
git clone https://github.com/macintoshm/yasashii-anki.git
cd yasashii-anki
./scripts/setup.sh
```

The setup script will:
- Check for Python 3.13+
- Install uv if needed
- Unzip the JMDict dictionary
- Create your `.env` configuration
- Install the package

### Option 2: Manual Installation

```bash
# Clone and enter directory
git clone https://github.com/macintoshm/yasashii-anki.git
cd yasashii-anki

# Unzip the dictionary
unzip jmdict-with-examples.zip

# Create configuration
cp .env.example .env
# Edit .env with your settings

# Install with uv
uv pip install -e .
```

## Configuration

Edit the `.env` file to configure Yasashii Anki:

```bash
# Path to JMDict dictionary file
JMDICT_PATH=./jmdict-with-examples.json

# AnkiConnect URL (default works for local Anki)
ANKI_URL=http://localhost:8765

# Your Anki deck name
AUTO_ANKI_DECK_NAME=Japanese

# Card type/model name in Anki
AUTO_ANKI_CARD_TYPE=Basic

# Field names in your Anki card type
AUTO_ANKI_WORD_FIELD=Front
AUTO_ANKI_READING_FIELD=Reading
AUTO_ANKI_MEANING_FIELD=Back
AUTO_ANKI_SENTENCE_FIELD=Sentence
AUTO_ANKI_SENTENCE_TRANSLATION_FIELD=SentenceTranslation
AUTO_ANKI_AUDIO_FIELD=Audio
```

## Usage

> **Note:** To use the `-c` flag (create cards), make sure Anki is open with AnkiConnect installed.

### Command Line Interface

```bash
# Look up a single word (no Anki needed)
yasashii 猫

# Look up multiple words (no Anki needed)
yasashii 猫 犬 鳥

# Look up and create Anki card (requires Anki running)
yasashii 猫 -c

# Create cards for multiple words (requires Anki running)
yasashii 猫 犬 鳥 -c

# Process words from a file (no Anki needed)
yasashii -f words.txt

# Process words from file and create cards (requires Anki running)
yasashii -f words.txt -c
```

### Graphical Interface

```bash
yasashii-gui
```

> **Note:** If "Add cards to Anki" is checked, make sure Anki is open with AnkiConnect installed.

The GUI provides an easy way to process multiple words at once:

**How to use:**
1. Launch with `yasashii-gui`
2. Enter Japanese words in the text box:
   - One word per line, OR
   - Comma-separated (e.g., `猫, 犬, 鳥`)
3. Check/uncheck "Add cards to Anki" (checked by default)
4. Click **Submit**
5. View results in the results panel below

**Features:**
- **Batch processing**: Add dozens of words at once
- **Preview before adding**: See readings and meanings before creating cards
- **Status indicators**: Green = added, Orange = duplicate, Red = not found
- **Non-blocking**: UI stays responsive while processing

**Example workflow:**
```
# In the text box, enter:
食べる
飲む
寝る
起きる

# Click Submit
# Results show each word with meanings
# Cards are automatically added to your Anki deck
```

### Example Output (CLI)

```
📚 猫
Word:           猫
Reading:        ねこ
Meaning:
        1. (n) cat (esp. the domestic cat, Felis catus)
        2. (n) shamisen
        3. (n) geisha
Example:        あなたのサイトは、猫に興味のある人達にとって魅力的です。
Translation:    Your site appeals to people who are interested in cats.

🎴 Added 猫 to deck Japanese with audio
```

## Anki Setup Guide

### 1. Install AnkiConnect

1. Open Anki
2. Go to **Tools** → **Add-ons** → **Get Add-ons...**
3. Enter code: `2055492159`
4. Restart Anki

### 2. Create Your Deck

1. In Anki, click **Create Deck**
2. Name it (e.g., "Japanese")
3. Update `AUTO_ANKI_DECK_NAME` in `.env`

### 3. Create Card Type (Note Type)

For best results, create a custom note type with these fields:

| Field | Description |
|-------|-------------|
| Front | The Japanese word |
| Reading | Hiragana/katakana reading |
| Back | English meanings |
| Sentence | Example sentence in Japanese |
| SentenceTranslation | English translation of example |
| Audio | Audio pronunciation |

**To create:**
1. Go to **Tools** → **Manage Note Types**
2. Click **Add** → **Add: Basic**
3. Name it (e.g., "Japanese Vocabulary")
4. Click **Fields** and add the fields above
5. Update `AUTO_ANKI_CARD_TYPE` in `.env`

### 4. Match Field Names

Make sure the field names in `.env` match exactly what you named them in Anki:

```bash
AUTO_ANKI_WORD_FIELD=Front
AUTO_ANKI_READING_FIELD=Reading
AUTO_ANKI_MEANING_FIELD=Back
# etc.
```

## Troubleshooting

### GUI box showing squares for Japanese characters
It is likely that you are using WSL on Windows. 
To fix this, install a Japanese font in Ubuntu:
```
sudo apt update
sudo apt install fonts-noto-cjk
```
This installs Noto Sans CJK, which fully supports Japanese. Run the GUI again and it should work.

### "Failed to connect to Anki Connect API"

- Make sure Anki is running
- Check that AnkiConnect addon is installed
- Verify `ANKI_URL` in `.env` is correct (default: `http://localhost:8765`)

### "No translation found"

- The word may not be in the dictionary
- Try a different form (e.g., dictionary form of verbs)
- Check spelling

### "Card already exists in deck"

- A card with this word already exists
- This prevents duplicates

### "Field not found" errors

- Field names in `.env` don't match your Anki card type
- Check spelling and capitalization exactly match

### Audio not playing

- Audio is downloaded from JapanesePod101
- Some words may not have audio available
- Check your Anki audio settings

## Resources

- [AnkiConnect Documentation](https://foosoft.net/projects/anki-connect/)
- [JMDict Simplified](https://github.com/scriptin/jmdict-simplified)
- [Anki Manual](https://docs.ankiweb.net/)

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
