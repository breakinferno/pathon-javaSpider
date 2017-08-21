package com.cli.servlets;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

import com.cli.bean.Page;
import com.cli.bean.WxNum;
import com.cli.service.impl.WxNumServiceImpl;
import com.cli.ui.UpdateURL;
import com.cli.utils.translateObjToJSON;

public class HandleWxNumOp extends HttpServlet {

	/**
	 * The doGet method of the servlet. <br>
	 *
	 * This method is called when a form has its tag value method equals to get.
	 * 
	 * @param request the request send by the client to the server
	 * @param response the response send by the server to the client
	 * @throws ServletException if an error occurred
	 * @throws IOException if an error occurred
	 */
	public void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {

		response.setContentType("text/html");
		PrintWriter out = response.getWriter();
		out.println("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\">");
		out.println("<HTML>");
		out.println("  <HEAD><TITLE>A Servlet</TITLE></HEAD>");
		out.println("  <BODY>");
		out.print("    This is ");
		out.print(this.getClass());
		out.println(", using the GET method");
		out.println("  </BODY>");
		out.println("</HTML>");
		out.flush();
		out.close();
	}

	/**
	 * The doPost method of the servlet. <br>
	 *
	 * This method is called when a form has its tag value method equals to post.
	 * 
	 * @param request the request send by the client to the server
	 * @param response the response send by the server to the client
	 * @throws ServletException if an error occurred
	 * @throws IOException if an error occurred
	 */
	public void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {

		response.setContentType("application/json;charset=utf-8");
		PrintWriter out = response.getWriter();
		String action = request.getParameter("action");
		String target = request.getParameter("target");

		WxNumServiceImpl wxNumServiceImpl = new WxNumServiceImpl();
		switch (action) {
		case "delete":
			try {
				boolean flag = wxNumServiceImpl.deleteWxNum(target);

				JSONObject rt = new JSONObject();
				rt.put("state", flag);
				rt.put("msg", flag?"删除成功":"删除失败");
				//����ajax
				out.write(rt.toString());
			} catch (Exception e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			break;
		case "refresh":
			//target
			String id = target;
			UpdateURL updateURL = new UpdateURL();
			try {
				//更新
				boolean right = updateURL.updateGZHURL(id);
//				System.out.println("id="+id);
				JSONObject rt = new JSONObject();
				rt.put("state", right);
				rt.put("msg", right?"更新成功":"更新失败");
				//����ajax
				out.write(rt.toString());
			} catch (Exception e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			break;
		case "update":
			String level = request.getParameter("level");
			try {
				boolean flag = wxNumServiceImpl.updateLevelByWxNum(new WxNum(target,"",level));
				JSONObject rt = new JSONObject();
				rt.put("state", flag);
				rt.put("msg", flag?"更新成功":"更新失败");
				//����ajax
				out.write(rt.toString());
			} catch (Exception e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			break;
		default:
			try {

				JSONObject rt = new JSONObject();
				rt.put("state", false);
				rt.put("msg", "非法操作"); 
				//����ajax
				out.write(rt.toString());
			} catch (Exception e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			break;
		}

		out.flush();
		out.close();
	}

}
