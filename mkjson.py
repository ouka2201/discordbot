import json

def mkcplus(content, name):
	payload = {
		"utterance": content,
		"username": name,
		"agentState": {
		"agentName": "色々できるBOT",
		"tone": "normal",
		"age": "22歳"},
	"addition": {
		"unknownResponses": [
			"どゆこと？"
		],
		"ngwords": [
			"肩凝った"
		],
		"utterancePairs": [
			{
			"utterance": "肩凝った",
			"response": "適度に運動しないとね"
			}, {
			"utterance": "シージ",
			"response": "消しちゃえ,まだそのクソゲーやってるの？,やめちゃえ"
			}
		]
		}
	}
	enc = json.dumps(payload)
	return enc
