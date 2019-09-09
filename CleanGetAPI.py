#This program gets only the important values from the responses, So don't expect more
#Post the file here to not waste time on more programming
import json
import os
import requests

cid = 'q72ptdef1thm0lzrubb6zfw2hep4dg'
path = r'C:/Users/phunous/Documents/Fall 2017/Capstone/TwitchPython/'

def get_videos(user):
    videoid = []
    url = 'https://api.twitch.tv/kraken/channels/'+user+'/videos/?client_id=' + cid + '&limit=10'
    r = requests.get(url)
    videosjson = json.loads(r.text)
    videosjson = videosjson['videos']
    for video in videosjson:
        id = video["_id"]
        videoid.append(id)


    return videoid

def get_video_chat(line: str, user: str):
    # metadata. NO CHAT URL. May want this at each file?
    # vod_info = requests.get("https://api.twitch.tv/kraken/videos/v" + line, headers={"Client-ID": cid}).json()
    line = line.strip('v')
    response = None
    name = "v" + line + ".txt"
    newpath = path + user + '\\' + 'v' + line + '.txt'
    # if a video has already been crawled, don't crawl again. We already have chat there's nothing new. Don't want to waste time.
    if (os.path.isfile(newpath)):
        print('chat from video ' + line + ' has been crawled.')
    else:  # if there is no chat for certain video id, send a request.
        #before we send a request, write your first line
        with open(name, 'a') as file:
            #videoid, streamer name, game played, length of the video
            link = "https://api.twitch.tv/kraken/videos/"+line+"?client_id=q72ptdef1thm0lzrubb6zfw2hep4dg"
            r = requests.get(link)
            videojson = json.loads(r.text)
            file.write(line+", "+user+", "+videojson["game"]+", "+str(videojson["length"])+"\n")
            while response == None or '_next' in response:
                query = (
                    'cursor=' + response[
                        '_next']) if response != None and '_next' in response else 'content_offset_seconds=0'
                response = requests.get("https://api.twitch.tv/v5/videos//" + line + "/comments?" + query,
                                        headers={"Client-ID": cid}).json()
                # print('crawling ' + line)

                comments = response.get("comments", "no comment")
                for comment in comments:
                    try:
                        file.write(
                            str(comment["content_offset_seconds"]) + " &*^ " + comment["message"]["body"] + " &*^ " + str(
                                comment["message"]["fragments"]) + "\n")
                        file.newlines
                    except UnicodeEncodeError:
                        pass
        file.close()
        print("Finished Crawling " + line)



def main():
    #Problem with stripping \n while reading the file, make a list of streamers instead
    streamers = []
    with open("Streamers.txt", "r") as file:
        streamers = file.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        streamers = [x.strip() for x in streamers]
    file.close()
    for streamer in streamers:
        newpath = path + str(streamer)
        if not os.path.exists(newpath):
            os.mkdir(newpath)
        os.chdir(newpath)
        print("Current Path:" + os.getcwd())
        vid = get_videos(streamer)
        for id in vid:
            get_video_chat(id, streamer)



    print("Done!")
main()
