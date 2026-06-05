import streamlit as st
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import matplotlib.pyplot as plt

try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

st.set_page_config(page_title="Transcript Sentiment Analyzer", layout="wide")

st.title("📊 Transcript Sentiment Analyzer")
st.markdown("Analyze sentiment shifts in conversations to understand emotional dynamics")

# Input
transcript_text = st.text_area("Paste your transcript:", height=150, 
                               placeholder="Speaker: Text format")

if st.button("🔍 Analyze"):
    if transcript_text:
        lines = transcript_text.strip().split('\n')
        data = []
        
        for line in lines:
            if ':' in line:
                speaker, text = line.split(':', 1)
                speaker = speaker.strip()
                text = text.strip()
                
                scores = sia.polarity_scores(text)
                
                data.append({
                    'Speaker': speaker,
                    'Text': text,
                    'Sentiment Score': scores['compound']
                })
        
        if data:
            df = pd.DataFrame(data)
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Statements", len(df))
            col2.metric("Avg Sentiment", f"{df['Sentiment Score'].mean():.2f}")
            col3.metric("Range", f"{df['Sentiment Score'].min():.2f} to {df['Sentiment Score'].max():.2f}")
            
            # Results table
            st.subheader("Results")
            st.dataframe(df)
            
            # Chart
            fig, ax = plt.subplots()
            ax.plot(range(len(df)), df['Sentiment Score'], marker='o', color='blue')
            ax.axhline(y=0, color='red', linestyle='--')
            ax.set_title('Sentiment Trend')
            ax.set_ylabel('Score')
            st.pyplot(fig)
        else:
            st.error("Could not parse. Use format: Speaker: Text")
    else:
        st.error("Please paste a transcript")