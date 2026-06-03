from googleapiclient.discovery import build
import pandas as pd

# Your YouTube API Key
API_KEY = "AIzaSyDFPVZkuj9i-mwLU9WM2mOLwp0SJiXBdL8"

# Initialize YouTube API
youtube = build('youtube', 'v3', developerKey=API_KEY)

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
    """Get detailed stats for a video (views, duration, etc)"""
    
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
    # Format: PT1H30M45S
    import re
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
    """
    Calculate quality score based on:
    - Views (40% weight)
    - Comments (30% weight)
    - Duration preference (30% weight) - 20-40 mins is ideal
    """
    
    # Normalize views (cap at 1 million for scoring)
    views_score = min(views / 1000000, 1) * 100
    
    # Normalize comments (cap at 10k for scoring)
    comments_score = min(comments / 10000, 1) * 100
    
    # Duration score (20-40 mins is ideal = 100 points)
    if 20 <= duration_minutes <= 40:
        duration_score = 100
    elif 15 <= duration_minutes < 20:
        duration_score = 80
    elif 40 < duration_minutes <= 50:
        duration_score = 80
    else:
        duration_score = 50
    
    # Weighted quality score
    quality_score = (views_score * 0.4) + (comments_score * 0.3) + (duration_score * 0.3)
    
    return round(quality_score, 2)

def rank_tutorials(query, max_results=10):
    """Search and rank tutorials by quality"""
    
    # Get search results
    search_response = search_tutorials(query, max_results)
    
    tutorials = []
    
    for item in search_response.get('items', []):
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        channel = item['snippet']['channelTitle']
        
        # Get detailed stats
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
    
    # Sort by quality score (highest first)
    tutorials_df = pd.DataFrame(tutorials)
    tutorials_df = tutorials_df.sort_values('Quality Score', ascending=False)
    
    return tutorials_df

# Test the function
if __name__ == "__main__":
    print("Searching for Python tutorials...")
    results = rank_tutorials("Python tutorial", max_results=10)
    
    print("\n" + "="*80)
    print("TOP PYTHON TUTORIALS (Ranked by Quality)")
    print("="*80 + "\n")
    
    # Display results
    for idx, (_, row) in enumerate(results.iterrows(), 1):
        print(f"{idx}. {row['Title']}")
        print(f"   Channel: {row['Channel']}")
        print(f"   Views: {row['Views']:,}")
        print(f"   Comments: {row['Comments']:,}")
        print(f"   Duration: {row['Duration (mins)']} minutes")
        print(f"   Quality Score: {row['Quality Score']}/100")
        print(f"   Link: {row['URL']}")
        print()
     