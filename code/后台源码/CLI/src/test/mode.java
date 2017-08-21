package test;

import java.util.ArrayList;
import java.util.concurrent.SynchronousQueue;

import javax.security.auth.login.LoginContext;
import javax.sound.midi.VoiceStatus;

import com.cli.bean.Article;
import com.cli.bean.Page;
import com.cli.bean.User;
import com.cli.bean.WxNum;
import com.cli.service.impl.ArticleServiceImpl;
import com.cli.service.impl.ArticlesServiceImpl;
import com.cli.service.impl.UserServiceImpl;
import com.cli.service.impl.WxNumServiceImpl;
import com.cli.servlets.RegisterServlet;

public class mode {

	public static void main(String[] args) throws Exception {
		mode mode = new mode();
//		mode.Login();
		mode.register();
		
	}
	
	
	public void  Login() throws Exception{
		String u_name = "黎明";
		String u_password="12345";
		UserServiceImpl userServiceImpl = new UserServiceImpl();
		User user = new User(u_name, u_password);
		try {
			
			if (userServiceImpl.findUser(user)!=null) {
				//登录成果，跳到用户页面
				System.out.println("登录成功");
			}
			else {
				//用户不存在，给予提示信息
				System.out.println("用户不存在，给予提示信息");
			}
			
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	
	public void register(){
		
		String u_name = "晓辉";
		String u_password="12345";
		UserServiceImpl userServiceImpl = new UserServiceImpl();
		User user = new User(u_name, u_password);
		
		try {
			if (u_name==null||u_password==null||u_name.equals("")||u_password.equals("")) {
				System.out.println("用户名和密码不能为空");
			}else {
				if (userServiceImpl.findUserByUserName(u_name)!=null) {
					//用户已经存在。给予提示信息
					System.out.println("用户已存在");
				}else {
					boolean right = userServiceImpl.insertUser(user);
					if (right) {

						//注册成果
						System.out.println("注册成功");
					}
				}
			}
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
		
}
