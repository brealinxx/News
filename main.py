import re
import html
import requests

def get_top_stories_with_content(limit=10):
     response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
     story_ids = response.json()

     stories = []
     for story_id in story_ids[:limit]:
          story_item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
          origin_url = f"https://news.ycombinator.com/item?id={story_id}"
          story_response = requests.get(story_item_url)
        
          story_data = story_response.json()
          story_info = {
               'title': story_data.get('title'),
               'url': story_data.get('url') if story_data.get('url') else origin_url,
               'text': process_text(story_data.get('by'), story_data.get('text'))
          }
          stories.append(story_info)

     return stories
     
def process_text(story_by, story_text):
    if not story_text:
        return None
    
    return story_by + ": " + clean_html_content(story_text)

def clean_html_content(content):
    cleaned_content = re.sub(r'<p>', '\n\n', content)
    cleaned_content = re.sub(r'<a href="[^"]+">([^<]+)</a>', r'\1', cleaned_content)
    cleaned_content = re.sub(r'<[^>]+>', '', cleaned_content)
    cleaned_content = html.unescape(cleaned_content)
    
    return cleaned_content

if __name__ == "__main__":
    top_stories = get_top_stories_with_content()
    i = 1
    for story in top_stories:
        print(f"{i}:")
        print(f"Title: {story['title']}")
        print(f"URL: {story['url']}")
        print(f"Content: {story['text']}\n") 
        i += 1