# git学习笔记
## 参考文档:[git指令说明](https://doc.oazon.com:2096/f/3222671)
---
## 其他知识
+ 主库与子库的关系：子库会作为主库的一个子目录存在，但子库也是个独立的Git仓库。
## 常用指令
+ `git reset HEAD <file>`撤销add提交
+ `git revert <commit>`保留回退之前的提交历史，并创建一个新的提交来撤销指定的提交
+ `git reset <commit>`丢弃指定提交之后的所有提交，并将分支指针移动到指定提交
+ `git checkout -- .`撤销对工作目录中文件的修改
+ ``查看远程仓库修改文件

### 一波流
+ `git st`
+ `git diff * `确定本地文件有哪些修改，并列出   
+ `git stash`将本地修改的内容缓存至本地git
+ `git pull --rebase`从远端拉取最新文件内容状态并同步至本地
+ `git stash pop`将缓存至本地git中的内容弹出
+ `git add `添加本地修改文件至缓冲区
+ `git commit -m ''`将缓冲区文件提交至本地仓库
+ `git st`
+ `git diff *`最后在确定一次修改的文件格式和提交的格式是否正确
+ `git push`将本地仓库更新至云端

## git编写规则
### 1、当添加功能时：git commit -m 'feat(login): support create a user'
### 2、当修改bug时：git commit -m 'fix(login): fix username is null when create a user'
### 3、当重构函数时：git commit -m 'refactor(login): refactor create a user'
### 4、当提交文档更改时：git commit -m 'doc(network): transfer protocol'
### 5、当本次是无关紧要的改动，或者测试代码，或者格式：git commit -m 'chore(test): network unit test'
### 6、当本次版本发布：git commit -m 'release(beta): version 0.63.0 VC-BETA'
### 7、提交测试用例：git commit -m 'fix(login): 登录注册模块测试用例新增or改动 v1.0.0'