# 📊 Transcript Sentiment Analyzer

An AI-powered web app that analyzes sentiment shifts in conversations to understand emotional dynamics.

## 🎯 Problem

Understanding how emotions change during meetings, interviews, or conversations is difficult. You can't easily see:
- When sentiment shifted
- Who was more positive/negative
- How the conversation evolved emotionally

## ✨ Solution

This analyzer:
- Parses transcripts by speaker
- Calculates sentiment for each statement (-1 to +1)
- Shows emotional trends over time
- Identifies key turning points
- Provides conversation health score

## 🚀 Live Demo

**[Try it here](https://bnhbtgwabysltjpkegp3vu.streamlit.app/)**

## 🏗️ Architecture

**Components:**
1. **Transcript Parser** - Extract speakers and text
2. **VADER Sentiment Analyzer** - Score sentiment (-1 to +1)
3. **Data Processing** - Organize and analyze data
4. **Visualization** - Create charts and graphs

**Tech Stack:**
- Python 3.14
- NLTK (VADER sentiment analysis)
- Pandas (data processing)
- Matplotlib (charts)
- Streamlit (web interface)

## 📖 How to Use

1. Go to [Live Demo](https://bnhbtgwabysltjpkegp3vu.streamlit.app/)
2. Paste transcript in format: `Speaker: Text`
3. Click "Analyze"
4. View results instantly

**Example transcript:**
Tanvi: I'm really excited about this project!
Manager: Actually, I have serious concerns.
Tanvi: Let's discuss them. I appreciate your feedback.
Manager: Thank you. I'm feeling more optimistic now.

## 📊 What You Get

- **Sentiment Scores:** -1 to +1 for each statement
- **Trend Analysis:** How sentiment changes throughout conversation
- **Speaker Comparison:** Who was more positive/negative
- **Health Score:** Overall conversation quality (0-100)

## 🎓 Key Features

✅ Real-time sentiment analysis
✅ Interactive visualizations  
✅ Speaker statistics
✅ Instant results
✅ Simple intuitive interface

## 💡 Use Cases

- **HR Teams:** Analyze interview dynamics
- **Managers:** Track team morale in meetings
- **Support Teams:** Identify frustrated customers
- **Researchers:** Study conversation patterns
- **Trainers:** Improve communication coaching

## 📚 What I Learned

- VADER sentiment analysis algorithm
- Natural Language Processing (NLP)
- Data visualization with Matplotlib
- Streamlit web development
- Cloud deployment (Streamlit Cloud)
- GitHub integration

## 🎬 Interview Talking Points

"I built a sentiment analysis tool that analyzes conversations to show emotional dynamics. It uses the VADER algorithm to score sentiment (-1 to +1) and provides insights into how emotions change over time. The app is deployed on Streamlit Cloud and available publicly. This project demonstrates NLP skills, data visualization, and web development."

## 🔮 Future Enhancements

- Real-time transcription from audio
- Multi-language support
- Emotion detection (beyond sentiment)
- Speaker interruption analysis
- Batch processing of multiple transcripts
- Topic extraction and analysis

## 📁 Project Structure

youtube-tutorial-ranker/
├── sentiment_analyzer.py    # Main Streamlit app
├── requirements.txt         # Dependencies
├── README.md               # Documentation
├── app.py                  # YouTube ranker app
└── main.py                 # YouTube ranker logic
## 🔗 Links

- **Live App:** https://bnhbtgwabysltjpkegp3vu.streamlit.app/
- **GitHub:** https://github.com/tanvi-honade/youtube-tutorial-ranker
- **Author:** Tanvi Honade

## 📝 License

MIT License - Feel free to use and modify

---

**Built with ❤️ for better conversations**