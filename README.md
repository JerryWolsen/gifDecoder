# gifDecoder
parse gif into frames and zip

## usage
- 1. create a folder named 'gifInput' in desktop
- 2. put json files in the folder
- 3. json format example: 
      {"100001": {
        "Id": "100002",
        "Address": "https://qipai.56.com/u_logo?url=http://i3.itc.cn/20180828/3a49_cbc80e89_2143_3cf4_a892_b6ca278555ad_1.gif"} }
  
- 4. run gifDecoder.py
- 5. a folder will be created on Desktop
- 6. all gifs in json files are parsed into frames, and then zipped with its Id, like 100001.zip
