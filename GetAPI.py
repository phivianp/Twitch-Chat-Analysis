import json
import os
import requests
import time

cid = 'q72ptdef1thm0lzrubb6zfw2hep4dg'
#Don't forget to change your path
path = r'C:\Users\phunous\Documents\Fall 2017\Capstone\TwitchPython\\'
#somehow the path to this has already been set
global gamelist, streamerlist
gamelist = []
streamerlist = set()
def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]
def get_gamelist():
    # Space in http is +
    with open('VideoGamesInfo.txt', 'r') as f:
        for line in f:
            list = line.split(',')
            game = list[0]
            if (' ' in game) is True:
                index = find(game, ' ')
                for x in index:
                    game = game[:x] + '+' + game[x+1:]
            gamelist.append(game)

def get_games():
    #get the top 100 games
    #list index under top are int, so just loop through it
    r = requests.get('https://api.twitch.tv/kraken/games/top/?client_id='+cid+'&limit=100')
    gamesjson = json.loads(r.text)
    gamesjson = gamesjson['top']
    #print(str(gamesjson[0])) #wanted to see the first item
    with open('VideoGamesInfo.txt', 'w') as f:
        for game in gamesjson:
            f.write(str(game['game']['name'])+', '+str(game['game']['popularity'])+', '+str(game['game']['_id'])+', \n')
    #To-Do List: Append Video Game Categories, not found in API

def get_streamers():
    with open('Channels.txt', 'w') as f:
        for x in gamelist:
            print(x)
            r = requests.get('https://api.twitch.tv/kraken/streams/?client_id='+cid+'&game='+x+'&limit=100')
            streamsjson = json.loads(r.text)
            streamsjson = streamsjson['streams']
            for stream in streamsjson:
                #make a unique list first
                print(str(stream['channel']['_links']['self']))
                streamerlist.add(str(stream['channel']['_links']['self']))
        for y in streamerlist:
            f.write(y + '\n')
    f.close()

def get_videos():
    #Create directories
    #Reliable streamer->video id-> video info file + chat data
    with open('Channels.txt', 'r') as f:
        url = f.readline()+ '/videos/?client_id=' + cid +'&limit=100'
        r = requests.get(url)
        videosjson = json.loads(r.text)
        if videosjson['_total'] > 10:
            videosjson = videosjson['videos']
            for video in videosjson:
                if video['language'] is 'en':
                    f.close()


def gather_responses_from_usernames(names: list):
    users_response = []
    for user in names:
        print('(1) starting ' + user + ' crawl')
        # this response does not send the videos on a channels current videos. So idk where these videos are coming from?
        r = requests.get(
            'https://api.twitch.tv/kraken/channels/' + user + '/videos/?client_id=' + cid +'&limit=99')

        response = r.text
        print(response)

        # create a directory of a user to store their responses in.
        newpath = path + user
        if not os.path.exists(newpath):
            os.mkdir(newpath)
        os.chdir(newpath)

        # may need to fix in future. Cant paginate? Only get a select number of videos?
        with open('user_response.txt', 'w') as f:  # write to file so we can possibly use for future?
            try:
                f.write(response)
            except UnicodeEncodeError:
                pass
        # this is seconds not milliseconds. Might not need this since we are only talking to api.
        time.sleep(5)
        print('(2) response has been written for ' + user + '.')
        users_response.append(response)



    return users_response  # need to return for picking out video ids.

def gather_vods(response: list):
    vid_unique = []
    # the true response in is first position of array/list. Get that and convert to dicttionary, then get _id key.
    initalvid = response[0]
    dict_convert = json.loads(initalvid)
    response = dict_convert["videos"]
    for elem in response:
        video = elem["_id"]
        item = video.split('v')  # only care about the number of vod.
        vid = item[1]  # it's always split at the second index of the list.
        if vid not in vid_unique:
            vid_unique.append(vid)
    with open('vid_ids.txt', 'w') as v_file:
        for item in vid_unique:
            v_file.write(item + '\n')

    print("(3) wrote all video ids to a file.")

def get_vid(userid):
    vidlist = []

    return vidlist;

def get_video_chat(line: str, user: str):
    # metadata. NO CHAT URL. May want this at each file?
    # vod_info = requests.get("https://api.twitch.tv/kraken/videos/v" + line, headers={"Client-ID": cid}).json()
    response = None
    name = "v" + line + ".txt"
    newpath = path + user + '\\' + 'v' + line + '.txt'
    # if a video has already been crawled, don't crawl again. We already have chat there's nothing new. Don't want to waste time.
    if (os.path.isfile(newpath)):
        print('chat from video ' + line + ' has been crawled.')
    else:  # if there is no chat for certain video id, send a request.
        while response == None or '_next' in response:
            query = (
                'cursor=' + response[
                    '_next']) if response != None and '_next' in response else 'content_offset_seconds=0'
            response = requests.get("https://api.twitch.tv/v5/videos//" + line + "/comments?" + query,
                                    headers={"Client-ID": cid}).json()
            print('crawling ' + line)
            with open(name, 'a') as file:
                file.write(json.dumps(response))  # dump all chats to a file.


def main():
    #get_games()
    #get_gamelist()
    #get_streamers()
    #get_videos()
    #get_chat()
    with open(path+"\Streamers.txt", "r") as f:
        for x in f:
            userid = f.readline()
            vidlist = get_vid(userid)
            for y in vidlist:
                get_video_chat(y, userid)
    print("Done!")
main()