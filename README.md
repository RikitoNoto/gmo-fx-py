# gmo-fx-py
GMOが提供するFX用APIのSDKです。
GMOのAPIについては[こちら](https://api.coin.z.com/fxdocs/)のリファレンスを参照してください。

## インストール
```shell
pip install gmo-fx
```

## 使い方
各APIのエンドポイントの頭にgetをつけたメソッドを定義しています。
そのメソッドを実行することで、APIの呼び出しを行います。
※例：「KLine情報の取得」APIの場合
```python
from gmo_fx import KlinesApi, KlineInterval, Symbol
from datetime import datetime

response = KlinesApi()(
  symbol=Symbol.USD_JPY,
  price_type="BID",
  interval=KlineInterval.M1, # 1分足
  date=datetime.now(),
)
print(response.klines)
```

### タイムアウト
各APIクラスのコンストラクタに`timeout`を指定すると、API呼び出しのタイムアウトを設定できます。
値は[requests](https://requests.readthedocs.io/en/latest/user/advanced/#timeouts)の`timeout`にそのまま渡されます。
秒数、または`(接続タイムアウト, 読み取りタイムアウト)`のタプルを指定してください。
未指定（`None`）の場合はタイムアウトせず、応答があるまで待ち続けます。

```python
from gmo_fx.api.klines import KlinesApi
from gmo_fx.api.order import OrderApi

# Public API
klines_api = KlinesApi(timeout=10)

# Private API
order_api = OrderApi(api_key="API_KEY", secret_key="SECRET_KEY", timeout=(3.05, 10))
```

タイムアウトした場合は`requests.exceptions.Timeout`が送出されます。

```python
from requests.exceptions import Timeout

try:
    response = klines_api(...)
except Timeout:
    # 再試行などを行う
    ...
```

> [!WARNING]
> 注文系のAPI（`OrderApi`、`IFDOrderApi`、`CloseOrderApi`、`ChangeOrderApi`、`CancelOrdersApi`など）は、
> タイムアウトしてもサーバー側では処理が完了している可能性があります。
> そのまま再試行すると二重に注文される恐れがあるため、`ActiveOrdersApi`や`OrdersApi`などで注文状況を確認してから再試行してください。
> `client_order_id`を指定しておくと、注文の確認がしやすくなります。
