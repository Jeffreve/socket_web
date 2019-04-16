无框架 本地测试 无美化


routes
- error 404页面
+ current_user、login_required 登陆成功后增加权限


routes_static
- index 主页
- static 照片文件
 
 
routes_user
- login_view 登陆验证
+ 用户验证 
- register_view 注册
- user_profile 用户信息
- user_admin_users 管理员页面


model
- new
- delete
- all
- save
- find
+ add 子类自定义 
+ update 子类自定义


routes_todo
- all todo主页
- edit 编辑页面
+ all delete add edit


routes_weibo
-- weibo 评论导入到微博
- all
- add
- edit
+ redirect页面的id
-- comment
- edit
+ redirect页面的id


ajax todo 用户验证index 其他操作是js 无需验证
- index 加载 loadall 区分多用户
- add 事件绑定 添加用户id
- delete 事件委托
- edit 添加update
- update 事件委托 


ajax weibo