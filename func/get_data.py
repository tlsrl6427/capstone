#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def get_data(keyword = '축구', length = 1000 ,client_id = "mFVJrDtj4trdT2ermoVF", client_secret = "hbpIY84KD3", naver_api = False):
    text1 = [] #데이터 값
    text_amount = []        # 본문 분량
    keyword_mentioned = []  # 키워드 언급 횟수
    commentNum = []         # 댓글 개수
    keyword_100 = []        # 첫 100단어안에 키워드 포함 여부(포함1, 미포함0)
    keyword_title_data = [] # 제목에 키워드 포함 여부
    link_num_data = []      # 링크 개수
    player_num_data = []    # 동영상 개수
    img_num_data = []       # 이미지 개수
    poDate = []

    # naver api
    if naver_api:
        blog_url = naver_api_blog_url(keyword, client_id, client_secret)

    else :
        blog_url = blog_search(keyword, length)

    for url in blog_url :
        text2 = ""
        # response1 = requests.get(items[i]['link'])
        # soup = BeautifulSoup(response1.text)
        # idx = str(soup.find_all('iframe').pop()).find('src')
        # source = str(soup.find_all('iframe').pop())[idx+5:-11]
        # source = source.replace('amp;', '')
        # url = 'http://blog.naver.com' + source
        response1 = requests.get(url)
        soup = BeautifulSoup(response1.text)
        # 예외처리
        temp = soup.find_all("div", "se-main-container") + soup.find_all("div", id="postViewArea")
        try:
            temp1 = BeautifulSoup(str(temp.pop()))
        except:
            continue
        text = temp1.text.replace('\n', ' ')
        text1.append([processString(text)])
        title = soup.title.text

        #지난 날짜, 포스트 날짜
        poDate += [postDate(soup)]


        #댓글 갯수
        commentNu = _commentNum(soup)
        
        
        try:
            commentNum.append(int(commentNu))
        except:
            commentNum.append(0)
            

        # 키워드 언급 개수
        keyword_mentioned.append(keyword_search(text, keyword))
            
        # 본문 분량
        text2 += processText(text)
        text_amount.append(len(text2))
        
        if keyword_in_100(text) == True:
            keyword_100.append(1)
        else:
            keyword_100.append(0)
            
        if type(keyword) != list:
            keyword_list = keyword.split()
        keyword_title = []
        
        for k in keyword_list:
            keyword_title += [k in title]
            
        if keyword_title == [True]:
            keyword_title_data.append(1)
        else:
            keyword_title_data.append(0)
                
        
        link_num = len(temp1.find_all('div', class_="se-module se-module-oglink"))
        link_num_data.append(link_num)
        
        player_num= len(temp1.find_all('div', class_= 'se-component se-video se-l-default') + temp1.find_all('a', class_="se-link"))
        player_num_data.append(player_num)

        img_num= len(temp1.find_all('img'))
        img_num_data.append(img_num)

    data_dict = {}
    data_dict['text_amount'] = text_amount
    data_dict['keyword_mentioned'] = keyword_mentioned
    data_dict['commentNum'] = commentNum
    data_dict['keyword_100'] = keyword_100
    data_dict['keyword_title_data'] = keyword_title_data
    data_dict['link_num_data'] = link_num_data
    data_dict['player_num_data'] = player_num_data
    data_dict['img_num_data'] = img_num_data
    data_dict['post_date'] = poDate
    
    
    return data_dict, text1

