import sys
import requests
from datetime import datetime, timedelta
import time,json
import os.path
import argparse

class SubredditScrapper:
    def __init__(self,subname = "all",batchsize = 1000,timeblock=[1,0],order = 'desc',orderby = 'created_utc',output_path=""):
        self.config = {
            'subname':subname,
            'size':min(1000,batchsize),
            'timeblock':timeblock,
            'sort': order,
            'sort_type': orderby,
        }
        self.output_path = output_path
    
    def SearchQuery(self,subreddit,start,end,size):
        return f"https://api.pushshift.io/reddit/submission/search?subreddit={subreddit}&after={start}&before={end}&size={size}"
    
    def TimeQueryFormat(self,time):
        return int(time.timestamp())
    
    def ExtractFields(self,data):
        author,title,text,subreddit,flair,postid,url,time = 8*[""]
        author = data['author_fullname'] if 'author_fullname' in data else ""
        title = data['title'] if 'title' in data else ""
        text = data['selftext'] if 'selftext' in data else ""
        subreddit = data['subreddit'] if 'subreddit' in data else ""
        flair = data['link_flair_text'] if 'link_flair_text' in data else ""
        postid = data['id'] if 'id' in data else ""
        url = data['url'] if 'url' in data else ""
        time = data['created_utc'] if 'created_utc' in data else ""
        return {'Author':author,'Title':title,'Text':text,'Subreddit':subreddit,'Flair':flair,'Post ID':postid,'Url':url,'Created Time':time}
    
    def GetData(self,query):
        response = requests.get(query)
        
        if response.status_code != 200:
            print(f"Query at '{query}' failed with status code: {response.status_code}")
            return "Error"
        data = response.json()
        posts = data['data']
        result = [self.ExtractFields(x) for x in posts]
        # print(result)
        return result
    
    def getOutputFilename(self,start,end):
        return self.output_path+self.config['subname']+ start.strftime("%m-%d-%Y") +"to"+ end.strftime("%m-%d-%Y") + ".json"
        
    def PostsBetween(self,start,end):
        
        if os.path.exists(self.getOutputFilename(start,end)):
            prompt = input("File already exists, Do you want to continue and overwrite? (y/n)")
            if prompt.lower() == "n":
                return
        else:
            os.makedirs(os.path.dirname(self.getOutputFilename(start,end)), exist_ok=True)
            

        all_posts = []
        current_start = start
        prev_time = None
        
        while current_start < end:
            current_end = current_start + timedelta(hours=self.config['timeblock'][0],minutes=self.config['timeblock'][1])
            current_end = current_end if current_end < end else end
            url = self.SearchQuery(subreddit=self.config['subname'], start=self.TimeQueryFormat(current_start), end=self.TimeQueryFormat(current_end), size=self.config['size'])
#             print(url)
            print(f"Processing for {current_start} and {current_end}")

            data = self.GetData(url)
            if data == 'Error':
                print(f"Returning partial data.")
                return all_posts

            
            if len(data) == 0 and current_start < end:
                print(f"No posts found between {current_start} and {current_end}")
                current_start = current_end
            else:
                data.sort(key=lambda x: x['Created Time'],reverse=False)
                if prev_time == datetime.fromtimestamp(data[-1]['Created Time']):
                    # No new posts found after this start time, exit condition reached
                    return all_posts
                else:
                    all_posts.extend(data)
                    print(f"{len(data)} Data pulled for {current_start} and {current_end}")
                    prev_time = current_start
                    current_start = datetime.fromtimestamp(data[-1]['Created Time']+1)
#             print(data)
#             print(start,current_start,end)
            # Sleep to avoid overloading the server
            time.sleep(2)
        with open(self.getOutputFilename(start,end), 'w', encoding='UTF-8') as f:
            json.dump(all_posts, f)
        return all_posts

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--subreddit")
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--output")
    parser.add_argument("--batch")
    parser.add_argument("--timeblock")
    args = parser.parse_args()
    obj = SubredditScrapper(subname=args.subreddit,output_path=args.output,batchsize=int(args.batch),timeblock=[int(x) for x in args.timeblock.split(':')])
    obj.PostsBetween(start=datetime.strptime(args.start, '%m/%d/%Y'),end=datetime.strptime(args.end, '%m/%d/%Y'))