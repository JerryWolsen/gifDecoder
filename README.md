# gifDecoder
parse gif into frames and zip

## usage
- 1. create a folder named 'gifInput' in desktop
- 2. put json files in the folder
- 3. json format example: 
      {"100001": {
        "Id": "100002",
        "Address": "https://qipai.56.com/u_logo?url=http://i0.itc.cn/20180828/3a49_e86e4072_90cb_fdb1_f997_ad97db50ce57_1.gif"} }
  
- 4. run gifDecoder.py
- 5. a folder named 'gifZips' will be created on Desktop
- 6. In the folder, all gifs in json files are parsed into frames, and then zipped with name of its Id, like '100001.zip'
