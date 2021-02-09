# 概要
jsonファイルから次のマイクロサービスを立ち上げるための情報を読み取り、その情報をkanbanに渡すサービスです。
【概要というより仕様の説明なので、もう少しサービスの目的にフォーカスを当ててみましょう】

# 【事前準備
Dockerfileがbase imageでpython base imageに依存している
base imageの確認ともしくはbuildをする必要があることを明記する】


# 起動方法
kubernatesにdeployされることにより起動されます。
aion-coreで動かす際は、マイクロサービスの1つとして想定しているため、project.yamlで設定されている通り、aion-coreの起動に伴い自動的に起動されます。

# セットアップ
```
git clone git@bitbucket.org:latonaio/direct-next-service-kube.git
cd direct-next-service-kube
make docker-build
```

# I/O
## input
フォルダ内を監視し、jsonファイルが新たに作成されたら、その情報を読み込みます。
【どのフォルダからどう読み込むか】

## output
以下の情報をkanban_outputに返します。    
- connection_key：  
- output_data_path：次のマイクロサービスでoutputに使用されるパス  
- metadata：次のマイクロサービスを立ち上げるためのメタ情報  
- device_name：端末名（端末名の記載がない場合、同じ端末に情報が送られる）  
- file_list：ファイルリスト（ファイルリストがない場合、何も返されない）   
- process_number = 1  
【direct-next-service経由で他端末のkannbanにデータが送られるケースもあります。
どういう条件でそうなるのか、もここで明記する。】