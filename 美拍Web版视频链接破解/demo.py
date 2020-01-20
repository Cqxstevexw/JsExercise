#!/usr/bin/env python
# -*- coding:utf-8 -*-
import execjs

'''
ad_level: "N"
ar_magic_info: null
aside_info: null
campaign: ""
caption: "看完燃炸的《哥斯拉2》，该如..."
caption_all: "看完燃炸的《哥斯拉2》，该如何正确饲养一只野生哥斯拉？"
caption_complete: "看完燃炸的《哥斯拉2》，该如何正确饲养一只野生哥斯拉？"
caption_origin: "看完燃炸的《哥斯拉2》，该如何正确饲养一只野生哥斯拉？"
caption_url_params: []
category: 1
category_tag_id: 1613
comments_count: 78
convert_cover_pic: null
convert_pic_size: null
cover_pic: "//mvimg10.meitudata.com/5cf51b35933125280.jpg"
cover_pic_resize: null
cover_title: "哥斯拉饲养指南"
created_at: "06-03 21:10"
created_at_origin: "1559567400"
cur_lives_id: ""
cur_lives_type: 0
dangerous_action: false
display_source: 65549
entry_info: null
facebook_share_caption: ""
feed_id: "6698290982171022335"
first_frame_pic: "http://mvimg10.meitudata.com/5cf5fd880949e7554.jpg"
first_frame_pic_size: "1280*720"
follow_media_info: null
geo: null
has_watermark: 0
id: 1115788287
instagram_share_caption: "分享了不起的乌贼君的美拍“看完燃炸的《哥斯拉2》，该如何正确饲养一只野生哥斯拉？”，快来看看！"
is_long: true
is_popular: false
is_prefer: 0
is_safe: 1
is_safe2: 1
is_top: false
likes_count: 1643
locked: false
miniprogram_data: {,…}
new_music: {id: 1115788287, template_type: 1, name: "", singer: "", uploader: "了不起的乌贼君", cid: 0,…}
pic_size: "1280*720"
privacy_config: {allow_save_medias: 1, forbid_stranger_comment: 0, forbid_comment: 0, forbid_repost: 0}
qq_share_caption: "看完燃炸的《哥斯拉2》，该如何正确饲养一只野生哥斯拉？"
qq_share_sub_caption: ""
qzone_share_caption: "看完燃炸的《哥斯拉2》，该如何正确饲养一只野生哥斯拉？"
qzone_share_sub_caption: ""
recommend_caption: null
recommend_cover_pic: null
recommend_cover_pic_size: null
refuse_gift: false
reposts_count: 0
scheme_url: "http://www.meipai.com/media/1115788287?client_id=1089857306&utm_media_id=1115788287&utm_source=meipai_share&utm_content=test&viewCount=1&shareCount=1&gid="
show_controls: false
time: 210
type: "media"
url: "https://www.meipai.com/media/1115788287?client_id=1089857306&utm_media_id=1115788287&utm_source=meipai_share&utm_content=test&viewCount=1&shareCount=1&gid="
user: {id: 1069265146, screen_name: "了不起的乌贼君", country: 2630000, province: 2631700, city: 2631704,…}
user_recommend_cover_pic: null
user_recommend_cover_pic_size: null
video: "8050aE5HR0cDovL212dmlkZW8xMS5tZWl0dWRhdGEuY29tLzVjZjUxYjllMzU3ZTcyNDM2X0gyNjRfTVA1Y2Y1NDYubXA0P2s9ZDlkZjU2MDQ5MzMzNzhjNGI1MmNlZGRmMzc2MTljOGUmdD01ZDFkT8vRLEK6YjQxZQ=="
web_upload: true
weibo_share_caption: "#美拍#看完燃炸的《哥斯拉2》，该如何正确饲养一只野生哥斯拉？"
weixin_friendfeed_share_caption: "哥斯拉饲养指南"
weixin_friendfeed_share_sub_caption: ""
weixin_share_caption: "哥斯拉饲养指南"
weixin_share_sub_caption: "看完燃炸的《哥斯拉2》，该如何正确饲养一只野生哥斯拉？"
'''

# Init environment
print(execjs.get().name)
node = execjs.get()
ctx = node.compile(open('encryption.js', 'r').read())

video_str = "8050aE5HR0cDovL212dmlkZW8xMS5tZWl0dWRhdGEuY29tLzVjZjUxYjllMzU3ZTcyNDM2X0gyNjRfTVA1Y2Y1NDYubXA0P2s9ZDlkZjU2MDQ5MzMzNzhjNGI1MmNlZGRmMzc2MTljOGUmdD01ZDFkT8vRLEK6YjQxZQ=="

js_str = 'get_data_video()'
# data_video = ctx.eval(js_str)
data_video = ctx.call('get_data_video', video_str)
print(data_video)
