# House 

Old bot stuff I wrote when I lived with crazy people xddddd

```yaml
token: 'HERE'

manhole_enable: true
manhole_bind: 127.0.0.1:7272

max_reconnects: 0

encoder: etf

bot:
  commands_require_mention: false
  commands_prefix: '!'
  storage_serializer: yaml
  plugins:
    - house.laundry
    - house.trash
```
