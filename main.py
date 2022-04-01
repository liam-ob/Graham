import hmac
import json
import time
import websocket
import math
import datetime


class TimedValue:
    def __init__(self, timeout_value):
        self.timeout_value = timeout_value
        self._started_at = datetime.datetime.utcnow()

    def __call__(self):
        time_passed = datetime.datetime.utcnow() - self._started_at
        if time_passed.total_seconds() > self.timeout_value:
            return True
        return False


def main():

    SOCKET = "wss://ftx.com/ws/{'op': 'pong'}"

    api_key = "mwUORjWwcsCQ5czmCFXqXQx9Kl1_AX9pT0KIltmh"
    secret_key = "MLvuKeb0xgfC2O6RlCxhOIrHuTxYs_LZ0NgSimir"
    trade_size = 100

    global sixty_seconds
    sixty_seconds = TimedValue(60)

    global twenty_seconds
    twenty_seconds = TimedValue(20)

    global market_momentum
    market_momentum = 0

    def on_open(ws):
        print("opened connection\n\n")
        ts = int(time.time() * 1000)
        signa = hmac.new(secret_key.encode(), f'{ts}websocket_login'.encode(), 'sha256').hexdigest()
        auth = {'op': 'login', 'args': {'key': api_key,
                                        'sign': signa,
                                        'time': ts}}
        ws.send(json.dumps(auth))
        data = {'op': 'subscribe', 'channel': 'trades', 'market': 'SHIB-PERP'}
        ws.send(json.dumps(data))

    def on_close(ws):
        print("\nwebsocket closed!\n")

    def on_message(ws, message):
        print('\nRECIEVED MESSAGE')

        print(twenty_seconds())
        global market_momentum

        json_message = json.loads(message)
        data = json_message['data']

        for i in data:
            buy_or_sell = i['side']
            weight = (i['price'] * i['size'])

            if buy_or_sell == 'sell':
                market_momentum -= weight
                print('market momentum taken')
            else:
                market_momentum += weight
                print('market momentum added')

        print(market_momentum)
        # print('\tmarket momentum: ' + market_momentum)
        if twenty_seconds():
            try:
                print('\ttwenty seconds passed')
                trade_potential = (math.sqrt(int(market_momentum)))
                print('\t\tTrade potential: ' + str(trade_potential))
                if trade_potential > 50:
                    print('\t\t\tWe trading with this potential // do trade here')
                else:
                    print('\t\t\tNot trading with this potential')
            except Exception as e:
                print(e.args)

        if sixty_seconds():
            market_momentum = 0
            try:
                twenty_seconds._started_at = datetime.datetime.utcnow()
                sixty_seconds._started_at = datetime.datetime.utcnow()
            except Exception as e:
                print(e.args)


    ws = websocket
    ws = ws.WebSocketApp(SOCKET, on_open=on_open, on_message=on_message, on_close=on_close)
    ws.run_forever()


if __name__ == "__main__":
    main()
