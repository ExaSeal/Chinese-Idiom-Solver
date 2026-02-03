import streamlit as st
import pandas as pd
import sqlite3

# Set page config
st.set_page_config(page_title="Chinese Idiom Guesser", layout="wide")
st.title("🔍 Chinese Idiom Guesser")

# Load data once (cached)
@st.cache_resource
def load_data():
    conn = sqlite3.connect('chinese-idioms-12976.db')
    df = pd.read_sql_query("SELECT * FROM idiom", conn)
    return df

@st.cache_resource
def prepare_data():
    df = load_data()
    df_edit = df.copy()
    
    List1Tone = ["ā","ē","ī","ō","ū","ǖ"]
    List2Tone = ["á","é","í","ó","ú","ǘ"]
    List3Tone = ["ǎ","ě","ǐ","ǒ","ǔ","ǚ"]
    List4Tone = ["à","è","ì","ò","ù"]
    
    # Extract initials and finals
    for pos in range(1, 5):
        py_col = f'py{pos}'
        df_edit[f'initials_py{pos}'] = df_edit[py_col].str.extract(r'(^zh|^ch|^sh|^[bpmfdtnlgkhjqxrcsywz])', expand=False)
        df_edit[f'finals_py{pos}'] = df_edit[py_col].str.extract(r'(ang$|eng$|ing$|ong$|ai$|ei$|ui$|ao$|ou$|iu$|ie$|ve$|er$|an$|en$|in$|un$|vn$|a$|o$|e$|i$|u$|v$)', expand=False)
    
    # Convert tones
    for i in range(1, 5):
        tone_col = f'pytone{i}'
        tone_col_edit = f'Intpytone{i}'
        mask1 = df_edit[tone_col].str.contains('|'.join(List1Tone), na=False, regex=True)
        mask2 = df_edit[tone_col].str.contains('|'.join(List2Tone), na=False, regex=True)
        mask3 = df_edit[tone_col].str.contains('|'.join(List3Tone), na=False, regex=True)
        mask4 = df_edit[tone_col].str.contains('|'.join(List4Tone), na=False, regex=True)
        df_edit.loc[mask1, tone_col_edit] = 1
        df_edit.loc[mask2, tone_col_edit] = 2
        df_edit.loc[mask3, tone_col_edit] = 3
        df_edit.loc[mask4, tone_col_edit] = 4
    
    return df_edit

def IdentifyInitialsAndFinals(String):
    parts = String.split('_')
    temp_df = pd.DataFrame(parts, columns=['input'])
    temp_df['initials'] = temp_df['input'].str.extract(r'(^zh|^ch|^sh|^[bpmfdtnlgkhjqxrcsywz])', expand=False)
    temp_df['finals'] = temp_df['input'].str.extract(r'(ang$|eng$|ing$|ong$|ai$|ei$|ui$|ao$|ou$|iu$|ie$|ve$|er$|an$|en$|in$|un$|vn$|a$|o$|e$|i$|u$|v$)', expand=False)
    result = list(zip(temp_df['initials'], temp_df['finals']))
    return result

def GuessIdiom(String, StringOfNones=None, StringOfTones=None, StringOfNoneTones=None):
    df_edit = prepare_data()
    parts = String.split('_')
    matched = df_edit.copy()
    
    # Remove Tones First
    if StringOfNoneTones and StringOfNoneTones.strip():
        ToneParts = StringOfNoneTones.split('_')
        for i, tone_input in enumerate(ToneParts):
            if not tone_input:
                continue
            tone_name = f'Intpytone{i+1}'
            matched = matched[matched[tone_name] != int(tone_input)]

    # Match Tones
    if StringOfTones and StringOfTones.strip():
        ToneParts = StringOfTones.split('_')
        for i, tone_input in enumerate(ToneParts):
            if not tone_input:
                continue
            if tone_input.startswith('*'):
                tone_input = tone_input[1:]
                tone_name = f'Intpytone{i+1}'
                matched = matched[matched[tone_name] != int(tone_input)]
            else:
                tone_name = f'Intpytone{i+1}'
                matched = matched[matched[tone_name] == int(tone_input)]

    # Remove Non-Matches
    if StringOfNones and StringOfNones.strip():
        for InitAndFin in IdentifyInitialsAndFinals(StringOfNones):
            NonInitials, NonFinals = InitAndFin
            for i in range(1, 5):
                col_name_initial = f'initials_py{i}'
                col_name_final = f'finals_py{i}'
                matched = matched[(matched[col_name_initial] != NonInitials) & (matched[col_name_final] != NonFinals)]

    # Search
    for i, input in enumerate(parts):
        if not input:
            continue
        initials_name = f'initials_py{i+1}'
        finals_name = f'finals_py{i+1}'
        Initial, Final = IdentifyInitialsAndFinals(input)[0]
        
        if input.startswith('*'):
            input = input[1:]
            if pd.notna(Initial):
                matched = matched[matched[initials_name] != Initial]
            if pd.notna(Final):
                matched = matched[matched[finals_name] != Final]
        else:
            if pd.notna(Initial):
                matched = matched[matched[initials_name] == Initial]
            if pd.notna(Final):
                matched = matched[matched[finals_name] == Final]

    matched = matched.head(20)
    if len(matched) > 0:
        MatchedIdiom = matched[['char1','char2','char3','char4']].agg(''.join, axis=1)
        MatchedIdiomPy = matched[['pytone1','pytone2','pytone3','pytone4']].agg(''.join, axis =1)
        return MatchedIdiom, MatchedIdiomPy
    return []

# Create four text input boxes in columns
st.subheader("Search Parameters")

col1, col2 = st.columns(2)
with col1:
    st.write("**Pinying Pattern**")
    inner_col1, inner_col2, inner_col3, inner_col4 = st.columns(4)
    with inner_col1:
        InputChar1 = st.text_input(
        "1st Character",
        value="",
        key="Char1Py",
    )
    with inner_col2:
        InputChar2 = st.text_input(
        "2nd Character",
        value="",
        key="Char2Py",
    )
    with inner_col3:
        InputChar3 = st.text_input(
        "3rd Character",
        value="",
        key="Char3Py",
    )
    with inner_col4:
        InputChar4 = st.text_input(
        "4th Character",
        value="",
        key="Char4Py",
    )

with col2:
    st.write("**Exclude Phonetics**")
    exclude_input = st.text_input(
        "Exclude phonetics",
        value="",
        key="exclude",
        help="Separate by underscore. Example: y_ch_a_eng"
    )

col3, col4 = st.columns(2)
with col3:
    st.write("**Known Tones**")
    inner_col1, inner_col2, inner_col3, inner_col4 = st.columns(4)
    with inner_col1:
        InputChar1Tone = st.text_input(
        "1st Character",
        value="",
        key="Char1Tone",
    )
    with inner_col2:
        InputChar2Tone = st.text_input(
        "2nd Character",
        value="",
        key="Char2Tone",
    )
    with inner_col3:
        InputChar3Tone = st.text_input(
        "3rd Character",
        value="",
        key="Char3Tone",
    )
    with inner_col4:
        InputChar4Tone = st.text_input(
        "4th Character",
        value="",
        key="Char4Tone",
    )


with col4:
    st.write("**Exclude Tones**")
    exclude_tones_input = st.text_input(
        "Exclude tones",
        value="",
        key="exclude_tones",
        help="Tones to exclude. Use 1_2_3_4, separate by underscore."
    )

# Search button
if st.button("🔎 Search", use_container_width=True):
    pinyin_input = InputChar1+"_"+InputChar2+"_"+InputChar3+"_"+InputChar4
    tones_input = InputChar1Tone+"_"+InputChar2Tone+"_"+InputChar3Tone+"_"+InputChar4Tone
    if pinyin_input.strip():
        with st.spinner("Searching..."):
            results = GuessIdiom(
                pinyin_input,
                exclude_input if exclude_input.strip() else None,
                tones_input if tones_input.strip() else None,
                exclude_tones_input if exclude_tones_input.strip() else None
            )
        
        if len(results) > 0:
            st.success(f"Found {len(results[0])} idiom(s):")
            MatchedIdiom = results[0].reset_index(drop=True)
            MatchedIdiomTone = results[1].reset_index(drop=True)
            # Display results in a nice format
            for i in range(len(MatchedIdiom)):
                st.write(f"**{i+1}.** {MatchedIdiom[i]}  {MatchedIdiomTone[i]}")
        else:
            st.warning("No idioms found matching your criteria.")
    else:
        st.error("Please enter a pinyin pattern.")

# Help section
with st.expander("📖 Help & Guide"):
    st.write("""
    ### How to use:
    
    **Pinyin Pattern:**
    - Input known initials/finals or full pinying of corresponding positions of a four word idiom
    - Use `*` to exclude (e.g., `*t` excludes the initial 't')
    
    **Exclude Phonetics:**
    - Exclude specific initials/finals separated by underscores
    - Example: `y_ch_a_eng` excludes y-initial, ch-initial, a-final, eng-final
    
    **Tones (1-4):**
    - 1 = first tone (ā)
    - 2 = second tone (á)
    - 3 = third tone (ǎ)
    - 4 = fourth tone (à)
    - Use `_` to allow any tone in that position
    - Use `*` to exclude (e.g., `*1` excludes first tone)
    """)
