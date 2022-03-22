import hmac
import json
import time
import pprint
import websocket


# import time
# import hmac
# from requests import Request

def main():
    # ts = int(time.time() * 1000)
    # request = Request('GET', 'https://ftx.com/api')
    # prepared = request.prepare()
    # signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
    # signature = hmac.new('MLvuKeb0xgfC2O6RlCxhOIrHuTxYs_LZ0NgSimir'.encode(), signature_payload, 'sha256').hexdigest()
    #
    # prepared.headers['FTX-KEY'] = 'mwUORjWwcsCQ5czmCFXqXQx9Kl1_AX9pT0KIltmh' # API Key
    # prepared.headers['FTX-SIGN'] = signature
    # prepared.headers['FTX-TS'] = str(ts)
    #
    # Only include line if you want to access a subaccount. Remember to URI-encode the subaccount name if it contains special characters!
    # prepared.headers['FTX-SUBACCOUNT'] = 'my_subaccount_nickname'
    #
    # print(prepared.headers)

    SOCKET = "wss://ftx.com/ws/{'op': 'pong'}"

    api_key = "mwUORjWwcsCQ5czmCFXqXQx9Kl1_AX9pT0KIltmh"
    secret_key = "MLvuKeb0xgfC2O6RlCxhOIrHuTxYs_LZ0NgSimir"
    trade_size = 10000

    def on_open(ws):
        print("opened connection\n\n")
        ts = int(time.time() * 1000)
        signa = hmac.new(secret_key.encode(), f'{ts}websocket_login'.encode(), 'sha256').hexdigest()
        auth = {'op': 'login', 'args': {'key': api_key,
                                        'sign': signa,
                                        'time': ts}}
        ws.send(json.dumps(auth))
        data = {'op': 'subscribe', 'channel': 'trades', 'market': 'BTC-PERP'}
        ws.send(json.dumps(data))

    def on_close(ws):
        print("\nwebsocket closed!\n")

    def on_message(ws, message):
        print("\n")
        json_message = json.loads(message)
        pprint.pprint(json_message)

        market_momentum = 0

        data = json_message['data']
        for i in data:
            buy_or_sell = i['side']
            weight = (i['price'] * i['size'])
            if weight > trade_size:
                if buy_or_sell == 'buy':
                    market_momentum += weight
                    print('\t\t\t\t\tmomentum going up')
                else:
                    market_momentum -= weight
                    print('\t\t\t\t\tmarket momentum going down')

        print(market_momentum)

    ws = websocket
    ws = ws.WebSocketApp(SOCKET, on_open=on_open, on_message=on_message, on_close=on_close)
    ws.run_forever()


if __name__ == "__main__":
    main()
