##需求规划

### 输入文件
刑法文件：law.pdf

### Index阶段：
一路走 sparse （倒排索引），一路走dense（向量数据库）
反馈：不需要 mongo 已支持混合搜索

### rag agent serving:
	langchain: tool + hybrid retrieval + cross ranker + llm check and response.

### frontend:
	react 界面：
		提示问题 =》 markdown消息渲染 
		查看回答

### 部署

docker-compose 一健部署



## 优化

chunk 规则优化，法律条文特性
