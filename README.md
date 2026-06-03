# 🎥 YouTube Tutorial Quality Ranker

An AI-powered web application that intelligently ranks YouTube tutorials based on quality metrics including views, comments, and optimal video length (20-40 minutes).

## 🎯 Problem Statement

Students and learners waste significant time scrolling through YouTube search results, trying to find high-quality tutorials that match their learning style.

## ✨ Solution

The YouTube Tutorial Quality Ranker solves this by:
- Fetching YouTube videos based on search queries
- Analyzing video metrics (views, comments, duration)
- Calculating a quality score using a weighted algorithm
- Displaying ranked results sorted by quality

## 🏗️ Architecture

**Components:**
1. Video Search - Uses YouTube API v3 to fetch videos
2. Data Processing - Extracts and processes video metrics
3. Quality Scoring - Calculates scores based on views (40%), comments (30%), and duration (30%)
4. Web Interface - Streamlit-based UI

**Tech Stack:**
- Python 3.14.3
- YouTube API v3
- Pandas
- Streamlit
- Git/GitHub

## 🚀 How to Run

Install dependencies:
```bash
pip install google-api-python-client pandas streamlit