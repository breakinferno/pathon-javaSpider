<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<%
String path = request.getContextPath();
String basePath = request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+path+"/";
%>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <base href="<%=basePath%>">
    
    <title>My JSP 'login.jsp' starting page</title>
    
	<meta http-equiv="pragma" content="no-cache">
	<meta http-equiv="cache-control" content="no-cache">
	<meta http-equiv="expires" content="0">    
	<meta http-equiv="keywords" content="keyword1,keyword2,keyword3">
	<meta http-equiv="description" content="This is my page">
	<link rel="stylesheet" type="text/css" href="CSS/login.css">
	<link href="http://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
	<link href="http://cdn.bootcss.com/font-awesome/4.6.3/css/font-awesome.min.css" rel="stylesheet">
  </head>
  
  <body>
    <div class="login-container">
    	<div class="login-wrapper">
    		<div class="container">
    		<div class="row">
        <div class="col-md-offset-3 col-md-6">
            <form class="form-horizontal" action="Login" method="post">
                <span class="heading">用户登录</span>
                <div class="form-group">
                    <input type="text" class="form-control" id="inputEmail3" placeholder="账号" name="account">
                    <i class="fa fa-user"></i>
                </div>
                <div class="form-group help">
                    <input type="password" class="form-control" id="inputPassword3" placeholder="密码" name="password">
                    <i class="fa fa-lock"></i>
                </div>
                <div class="form-group">
                    <div class="main-checkbox">
                        <input type="checkbox" value="None" id="checkbox1" name="check"/>
                        <label for="checkbox1"></label>
                    </div>
                    <button type="submit" class="btn btn-default">立刻登录</button>
                </div>
            </form>
        </div>
    </div>
</div>
    	</div>
    </div>
    <script type="text/javascript">
/*     	(function(){
    	
    		var global = {};
			global.subData = function(url, data, callback) {
				$.ajax({
					type : 'post',
					url : url,
					data : data,
					success : function(data) {
						if (typeof callback === 'function') {
							callback(data);
						}
					},
					error : function(x, h, r) {
						console && console.log(x, h, r)
					}
				})
			}
			
    		$('.btn-default').on('click',function(e){
    			e.preventDefault();
    			var account = '';
    			var password= '';
    			swal('Hello world!');
/*     			global.subData('/CLI/login',{account:account,password:password},function(data){
    				if(data.state){
    					//登陆成功跳转
    				}else{
    					//登录失败
    				}
    			}) */
    		/*});
    	})(); */
    </script>
  </body>
</html>
