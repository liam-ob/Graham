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

    SOCKET = "wss://ftx.com/ws/trades"

    def on_open(ws):
        print("opened connection\n\n")
        print(ws)

    def on_close(ws):
        print("\nwebsocket closed!\n")

    def on_message(ws, message):
        print(message)
    ws = websocket
    ws = ws.WebSocketApp(SOCKET, on_open=on_open,on_message=on_message, on_close=on_close)
    ws.run_forever()


if __name__ == "__main__":
    main()
