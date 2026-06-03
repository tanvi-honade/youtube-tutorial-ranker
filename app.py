import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
import re

# Your YouTube API Key
API_KEY = "AIzaSyDFPVZkuj9i-mwLU9WM2mOLwp0SJiXBdL8"

# Initialize YouTube API
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Page config
st.set_page_config(page_title="YouTube Tutorial Ranker", layout="wide")

st.title("🎥 YouTube Tutorial Quality Ranker")
st.markdown("Find the best tutorials based on views, comments, and video length (20-40 mins)")

def search_tutorials(query, max_results=10):
    """Search for YouTube videos based on query"""
    request = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=max_results,
        type='video',
        order='viewCount'
    )
    response = request.execute()
    return response

def get_video_stats(video_id):
    """Get detailed stats for a video"""
    request = youtube.videos().list(
        part='statistics,contentDetails,snippet',
        id=video_id
    )
    response = request.execute()
    
    if response['items']:
        item = response['items'][0]
        stats = {
            'views': int(item['statistics'].get('viewCount', 0)),
            'comments': int(item['statistics'].get('commentCount', 0)),
            'duration': item['contentDetails']['duration']
        }
        return stats
    return None

def parse_duration(duration_str):
    """Convert ISO 8601 duration to minutes"""
    pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
    match = re.match(pattern, duration_str)
    
    if match:
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        seconds = int(match.group(3)) if match.group(3) else 0
        
        total_minutes = hours * 60 + minutes + seconds / 60
        return total_minutes
    return 0

def calculate_quality_score(views, comments, duration_minutes):
    """Calculate quality score"""
    views_score = min(views / 1000000, 1) * 100
    comments_score = min(comments / 10000, 1) * 100
    
    if 20 <= duration_minutes <= 40:
        duration_score = 100
    elif 15 <= duration_minutes < 20:
        duration_score = 80
    elif 40 < duration_minutes <= 50:
        duration_score = 80
    else:
        duration_score = 50
    
    quality_score = (views_score * 0.4) + (comments_score * 0.3) + (duration_score * 0.3)
    return round(quality_score, 2)

def rank_tutorials(query, max_results=10):
    """Search and rank tutorials by quality"""
    search_response = search_tutorials(query, max_results)
    tutorials = []
    
    for item in search_response.get('items', []):
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        channel = item['snippet']['channelTitle']
        
        stats = get_video_stats(video_id)
        
        if stats:
            duration_minutes = parse_duration(stats['duration'])
            quality_score = calculate_quality_score(
                stats['views'],
                stats['comments'],
                duration_minutes
            )
            
            tutorials.append({
                'Title': title,
                'Channel': channel,
                'Views': stats['views'],
                'Comments': stats['comments'],
                'Duration (mins)': round(duration_minutes, 1),
                'Quality Score': quality_score,
                'Video ID': video_id,
                'URL': f"https://www.youtube.com/watch?v={video_id}"
            })
    
    tutorials_df = pd.DataFrame(tutorials)
    tutorials_df = tutorials_df.sort_values('Quality Score', ascending=False)
    
    return tutorials_df

# Sidebar for input
st.sidebar.header("Search Settings")
query = st.sidebar.text_input("What tutorial do you want to find?", "Python tutorial")
max_results = st.sidebar.slider("Number of results", 5, 20, 10)

# Search button
if st.sidebar.button("🔍 Search", key="search_btn"):
    st.session_state.search_done = True
    st.session_state.query = query
    st.session_state.max_results = max_results

# Display results
if 'search_done' in st.session_state and st.session_state.search_done:
    with st.spinner("Searching and ranking tutorials..."):
        results = rank_tutorials(st.session_state.query, st.session_state.max_results)
    
    if len(results) > 0:
        st.success(f"Found {len(results)} tutorials!")
        
        # Display as cards
        for idx, (_, row) in enumerate(results.iterrows(), 1):
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### {idx}. {row['Title']}")
                    st.markdown(f"**Channel:** {row['Channel']}")
                    st.markdown(f"**Views:** {row['Views']:,} | **Comments:** {row['Comments']:,} | **Duration:** {row['Duration (mins)']} mins")
                
                with col2:
                    # Quality score badge
                    score = row['Quality Score']
                    if score >= 80:
                        st.success(f"⭐ {score}/100")
                    elif score >= 60:
                        st.info(f"👍 {score}/100")
                    else:
                        st.warning(f"⚠️ {score}/100")
                
                st.markdown(f"[🎬 Watch on YouTube]({row['URL']})")
                st.divider()
    else:
        st.error("No tutorials found. Try a different search.")
else:
    st.info("👈 Enter a search query and click 'Search' to get started!")