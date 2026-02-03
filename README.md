# 🔍 Chinese Idiom Solver

A Streamlit-based interactive application for searching and discovering Chinese idioms (四字成语) based on pinyin patterns, phonetics, and tones in a 'wordle' like game, but Chinese!.

## Features

- **Pinyin Pattern Search**: Search idioms by entering known initials, finals, or full pinyin for each character position
- **Phonetic Filtering**: Exclude specific initials and finals from search results
- **Tone Matching**: Filter idioms by known tones (1st, 2nd, 3rd, 4th) or exclude certain tones
- **Exclusion Support**: Use `*` prefix to exclude tones or phonetics at a character position instead of matching them

## Installation

### Prerequisites
- Python 3.8+
- SQLite3 database file: `chinese-idioms-12976.db` by **By_syk** https://github.com/by-syk/chinese-idiom-db, copy downloaded on 2026/Feb/3

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ExaSeal/Chinese-Idiom-Solver.git
cd Chinese-Idiom-Solver
```

2. Install dependencies:
```bash
pip install streamlit pandas
```

3. Run the application:
```bash
streamlit run idiom_app.py
```

The app will open in your browser at `http://localhost:8501`

## How to Use

### Pinyin Pattern
- Enter known initials/finals or full pinyin for each of the four character positions
- Example: `zh` for zh-initial, `ang` for ang-final
- Use `*` to exclude (e.g., `*t` excludes t-initial)

### Exclude Phonetics
- Enter specific initials/finals to exclude, separated by underscores
- Example: `y_ch_a_eng` excludes y-initial, ch-initial, a-final, and eng-final

### Known Tones
- 1 = First tone (ā)
- 2 = Second tone (á)
- 3 = Third tone (ǎ)
- 4 = Fourth tone (à)
- Use `_` to allow any tone in that position
- Use `*` to exclude (e.g., `*1` excludes first tone)

## Project Structure

- `idiom_app.py` - Main Streamlit application
- `IdiomGuesser.ipynb` - Jupyter notebook with development notes
- `chinese-idioms-12976.db` - SQLite database containing idiom data

## Database

The application uses a SQLite database containing Chinese idioms with the following columns:
- `char1`, `char2`, `char3`, `char4` - The four characters of the idiom
- `py1`, `py2`, `py3`, `py4` - Pinyin (with tones) for each character
- `pytone1`, `pytone2`, `pytone3`, `pytone4` - Pinyin with tone marks

## Acknowledgments

The Chinese idiom database (`chinese-idioms-12976.db`) used in this project is created by **By_syk**, https://github.com/by-syk/chinese-idiom-db 

