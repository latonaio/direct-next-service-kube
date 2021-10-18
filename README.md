# direct-next-service-kube
direct-next-service-kube は、マイクロサービス間の通信を仲介するマイクロサービスです。  
direct-next-service-kube は、jsonファイル(メッセージファイル)の生成を監視し、生成された場合にファイル内の情報を読み取ります。  
そして、その情報がメッセージングアーキテクチャに渡されることで、マイクロサービス間の通信が可能になります。   

# 動作環境
direct-next-serviceは、下記の動作環境を前提としています。  
- OS: Linux OS     
- CPU: ARM/AMD/Intel     
- Kubernetes     
- AION のリソース   

# セットアップ
```
git clone git@github.com:latonaio/direct-next-service-kube.git
cd direct-next-service-kube
make docker-build
```

# 起動方法
direct-next-service-kube を aion-core 上で動作させる場合、aion-service-definitions/services.ymlに定義を記載してください。  

# Input/Output
## input
指定されたパスを監視し、その中でメッセージファイルが新たに作成されたら、そのファイル内の情報を読み込みます。

## output
通信先がローカル(内部のマイクロサービス)である場合：  
```
- connection_key     
- output_data_path：内部のマイクロサービスでoutputに使用されるパス  
- metadata   
- file_list：ファイルリスト（ファイルリストがない場合、何も返されない）   
```

通信先がリモート(外部のマイクロサービス)である場合：   
```
- connection_key   
- output_data_path   
- metadata：外部のマイクロサービスのメタ情報  
- device_name：端末名  
- file_list   
- process_number = 1   
```  
 