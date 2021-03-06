import re
import emoji

def format_text(text):
    text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
    text = re.sub(r'<:[a-zA-Z0-9_]+:[0-9]+>', "", text)
    text = re.sub(r'<@![0-9]+>', "", text)
    text = re.sub('RT', "", text)
    text = re.sub('お気に入り', "", text)
    text = re.sub('まとめ', "", text)
    text = re.sub('\n', " ", text)#改行文字
    text = re.sub('ぁ', "あ", text)
    text = re.sub('ぃ', "い", text)
    text = re.sub('ぅ', "う", text)
    text = re.sub('ぇ', "え", text)
    text = re.sub('ぉ', "お", text)
    text = re.sub('ーー*', "ー", text)
    text = re.sub('-e', "", text)
    text = re.sub('-c', "", text)
    text = re.sub('-k', "", text)
    text_without_emoji = ''.join(['' if c in emoji.UNICODE_EMOJI else c for c in text])

    return text_without_emoji
