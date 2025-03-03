import re
import time

import requests,os,json

print( '#小tips:输入网址时请去掉“#/”,否则可能导致网址解析失败导致无法下载' )
print("#歌单网址例子：https://music.163.com/playlist?id=13388570379")
user_list_url = input("#请输入需要下载的歌单网址:")
user_file = input('请输入榜单名称:')
key=input("#请输入需要下载的音质等级：\n#0 极高音质(约8MB)\n#1 无损音质(约20MB)\n")
os.makedirs(user_file, exist_ok=True)
if key=='0':
    level='exhigh'
elif key=='1':
    level='lossless'
headers = {
    'upgrade-insecure-requests' : '1' ,
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36' ,
    'sec-fetch-dest' : 'iframe' ,
    'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' ,
    'sec-fetch-site' : 'same-origin' ,
    'sec-fetch-mode' : 'navigate' ,
    'referer' : 'https://music.163.com/' ,
    'accept-language' : 'zh-CN,zh;q=0.9,en;q=0.8' ,
    'cookie' : 'S_INFO=1740891963|1|0&60##|m13212338173;__csrf=2ed8d693f8b4510eceb5d32c30b9814c;ntes_utid=tid._.u8tBw9r5vQpAE1AQVBfVjck4OfnG5duI._.0;WNMCID=kdoepx.1740891956118.01.0;NTES_P_UTID=m0l4ND1sj75TgxHcKwRgSOvZWZxqp4Lh|1740629250;gdxidpyhxdE=6k3lXMkrvqbdfrihra4vLnS%2FyGn4VSLIS%2B4DuQ%2FCGcPeYOH%2Fl%2BBznLHVuaWd2tnrgQK%5CI3jrhD0Y%2FB%2BcvJsidb1Ki8evNL1LBTYHlSDiULqwpez%5Cx1eIpqqmMkENZOwpQvqsTCfLanZTS9NkXYANjnEmp0HYatzZDNZZt0ZSMK8oReYG%3A1740892889880;nts_mail_user=13212338173@163.com:-1:1;WEVNSM=1.0.0;WM_NI=QQAm%2BLTGNpVcAoHyCcrR6gFzoX8fyaCBycvfVnP5NK2i9AmdzGGLQVocWBWc11bltZOXTPSs%2Fnhz7yIw2uTiVHyBEqFsF9WgMZTSnWyEXPkU8A4vvMwcqQXOppuD1TlAMkQ%3D;NTES_PASSPORT=Jt3Uccaw_oks7TlSdhTIoNj7ndjnWJke0Wzn5P2S1DbUceKDcQzbiWgRN4dS_K9oWjrEjeu4d_yFyJJMlWn2Tk90B69ur2Nd1EcsMAi6Eo_HpJN0rFxx7fZyJSlDE93A227rrjJ6zK768.awXiUAfLm7I_q_OLcWe2_NYA5n5kheNgtT8aE2kPfEixROmzLKY;WM_TID=jpQUwdaOEchABAVRRFdrsU%2FMsPC%2BlNvc;WM_NIKE=9ca17ae2e6ffcda170e2e6ee85ed6aa6ac82b0e87eb0b48bb6c14f969a9faddb69f197a6b4aa7ca998f7d2e82af0fea7c3b92a938f8f8eaa4898998291d56983b1889ac269b28efa88c572ad88f887fc6b819eb784f56e96b2a0d6cd41f2b7f7a2f070ba9989add45eadbd99a3d669f3efae8df7528d889cb1d279edb2a89bb6738ba9fe96d7639698b7a3c87b86ad8adad66d8f869cb4ed5dbb9b98b1ea5ffc9ffc97f547b5bdbfb2db45b4b0bba5b460b09f838cd437e2a3;__bid_n=1844ca7c818a2e9b9b4207;MUSIC_U=007A08E92E3B68E4C63F81D6DC32E20ED7BA36AF5BC38C4CEB7EDA19C287117E275ED2535690E83167A89729478F1792F82B4602BC4DADCACC7BF13B28AA4BC363106D3847F0004EEF0EF598688048F3137E5B9743E0D4E3F28DC0C4DA60807442B50FB7CD60D143FC5C66C5A4D988D53BB7BDBA6CA0D5061065CAFD0B3245915E5E71CAE25E6A071C6FEBD3C20D5AA80C1F29758D2DD3D7EA112AAD185EEAC2DA9B6D67DAEC164AA69E9E5F1249F8D3AC0AF2484F70C6062C8CE7833A140C9F7B593BEC2C034508A76E157EC5619BA60B8087D215DBC1DB5377759D6AC47F00D6426F21F5CCB9C6DB84C70418D7AFED0787DBAF8A737214AAC47A4989F3A2041BAAC586813B42219B5E00DE3BD29F280F30921A694C8AE972A832E066A5152F978B1934454E2992B423AEC286D0ADC3D31F802D463965006836925E568C4CC2AD;__snaker__id=sxZKsPPX1nqMsZVB;P_INFO=m13212338173@163.com|1740629250|1|mail163|00&99|chq&1740491672&mbmail_android#US&null#10#0#0|132173&1|mail163&mbmail_android|13212338173@163.com;FEID=v10-84d8de442a8807e968612aea94f5ccfb49510011;__xaf_fpstarttimer__=1671951738510;__xaf_fptokentimer__=1671951738656;__xaf_thstime__=1671951738601;_ga=GA1.1.1916839591.1736341093;_ga_EPDQHDTJH5=GS1.1.1736341093.1.1.1736341447.0.0.0;_iuqxldmzr_=32;_ntes_nnid=2fb0ba517864364b6d3a18669b6cf7d3,1740891953263;_ntes_nuid=2fb0ba517864364b6d3a18669b6cf7d3;FPTOKEN=6o2oGP1TjF5XLGlsl8n7aqlqmy8ld9vnpSRjKO+aHswoZPGaQTxIw2tfnrsO420VjLC8R5Wq0skwBodImUznxSRMWoBNNPnojDbSM2hLlPHRmjdLgU2xpplkH9pCGIdqYu/iicD4uVqVVPFoKj3Pj1MpvZS+CV7lin67PocNio9jnLaWe4WCzn0q44VLgwf+Is5jgj/QNHovgTBQFs/495ASvOe5e6eHDkwMz8eWCDtlOtc4tCE+xnU0b+NVA0hSz+xk5w7lthvpXsRB8ws7Hsb/a1uhmqDhfj5Bwa2nRStbHcdfGQqW2psqN/gC0quuERszYFoRdKHxX61MjWjLsz39eKjbZ3Vrotq5ETMQ8ggtRTNPDizgb2tU/0IW6yzPupkpOw56Mnma1EHxvhOQ+A==|i4BT/9pHL6eXrDmFUAip8NyUG0asPdX656oT0fi0TwE=|10|0858e97af2a9182c1213e7670b3736f9;JSESSIONID-WYYY=urfNSQNqsAraOzH8oqZnQMvWRIPr4kvwPg%2BZZjo3mYc1H3scx%2FPjX%5C%2FvD3S%5CQfPM%2FZvwUpTqZAb6gFpyu8Pwr%5C%2F71okSFWeTnz55mX3luRNTGw%2BMJ%5C%5CljNOfhroGIUwGbpPV1f1AbHg6xcSOUF%2B9BJCPFZ70WaahRBoPmHMWfKsVxj4H%3A1740893753232;NMTID=00OKcULsgZzDYzIj0GAlxQOir-NdnAAAAGVVT8X5A;ntes_kaola_ad=1;NTES_SESS=FrP6yswrRxpwME5I2WqoOJcWhASvTM_MO9oZ93BQGw3wEox_E6mDytS5nLcV4xRTt95xOO4tKyQow0z1.x4e0.bIp0BnRaUGNr5ld6m.fo8PpFxGuyaeJlTORLf.3qUeMMmhjeErwkskfn80CrRuu5Ve1kpTh0Bk5zOY.AIoHeuKd5P5fUyzzavdLyCPvn9i6Ox3hDtqfxOGhTDOSOwfpRTTiNTV0BZko;sDeviceId=YD-4mQZmCKdushAR1QQQEfR2MlpPezX4N7w'}

resp = requests.get( url=user_list_url , headers=headers )
html_data = resp.text
prefix = 'https://music.163.com/#/song?id='
info_list = re.findall( '<li><a href="/song\?id=(.*?)">(.*?)</a></li>' , html_data )
music_list = [ prefix + info[ 0 ]  for info in info_list ]
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0',
    'Accept': 'application/json, text/plain, */*',
    "Content-Type": "application/json",
    'Authorization': 'Bearer e01072d5516479c6ebea703718ed8efa'
}
for index, music_url in enumerate(music_list, start=1):
    try:
        data={"url":music_url,
              "level":level,
              "type":"song",
              "token":"50080018feda6f56142ee536753d9f4b"}
        req = requests.post("https://api.toubiec.cn/api/music_v1.php", headers=headers, data=json.dumps(data))
        back = req.json()  # 直接使用 requests 的 json 方法解析响应
        name = back['song_info']['name']
        down_url = back['url_info']['url']
        type=back['url_info']['type']
        song_path = os.path.join(f'./{user_file}/', f"{name}.{type}")
        musci=requests.get(down_url, headers=headers)
        with open(song_path, mode="wb") as f:
            f.write(musci.content)
        print(f"#{index}:{name}歌曲下载完成")
    except requests.RequestException as e:
        print(f"下载 {music_url} 时发生网络错误: {e}")
    except (KeyError, json.JSONDecodeError) as e:
        print(f"解析 {music_url} 的响应数据时发生错误: {e}")
    except Exception as e:
        print(f"下载 {music_url} 时发生未知错误: {e}")
    time.sleep(1)

print("#歌曲全部下载完成")



