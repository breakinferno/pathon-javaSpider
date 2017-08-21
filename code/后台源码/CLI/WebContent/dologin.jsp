<%@ page language="java" contentType="text/html; charset=utf-8"  
    pageEncoding="utf-8"%>  
<%  
    String path=request.getContextPath();  
    String basePath=request.getScheme()+"://"+request.getServerName() +":"+request.getServerPort()+path+"/";  
    String username="";  
    String password="";  
    request.setCharacterEncoding("utf-8");  
    username=request.getParameter("account");  
    password=request.getParameter("password");  
    out.println(username);  
    out.println(password);  
    //验证登录
    if("admin".equals(username) && "admin".equals(password)){  
        session.setAttribute("loginUsername", username);  
        session.setAttribute("loginUser",username);  
        response.sendRedirect("main.jsp");  
    }else{  
        response.sendRedirect("login.jsp");  
    }     
%>
