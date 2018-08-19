# 頂点カラー付きobjファイルをblenderへインポートしてポリゴン数を削減して、同じ形式のobjファイルにエクスポートするサンプル
## 事前準備

事前にこれでvertex colorのついたobjをインポートできるようにしておく。
https://github.com/shimawork/io_scene_obj_vertex_color

## 使い方

blenderをpythonスクリプトで起動(macの場合)

```
/Applications/Blender/blender.app/Contents/MacOS/blender -P ~/Desktop/blenderScripts/obj2obj.py -- test.obj decimated_test.obj 0.3
```

### 「--」以降の引数は以下
* test.obj ・・・ 元になるobjファイル　　
* decimated_test.obj ・・・ decimatでポリゴン削減したobjファイル　　
* 0.3  ・・・ decimateで指定するrate  
