<%@ page language="java" import="java.util.*,java.io.*"
	pageEncoding="UTF-8"%>
<%
	String path = request.getContextPath();
	String basePath = request.getScheme() + "://"
			+ request.getServerName() + ":" + request.getServerPort()
			+ path + "/";
%>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<base href="<%=basePath%>">

<title>My JSP 'index.jsp' starting page</title>
<meta name="referrer" content="never">
<meta name="viewport" content="width=device-width, initial-scale=1"/>

<meta http-equiv="pragma" content="no-cache">
<meta http-equiv="cache-control" content="no-cache">
<meta http-equiv="expires" content="0">
<meta http-equiv="keywords" content="keyword1,keyword2,keyword3">
<meta http-equiv="description" content="This is my page">
<link rel="stylesheet" type="text/css" href="./CSS/index.css">
</head>

<body>
	<div class="container">
		<div class="searchForm">
			<div class="search-wrapper">
				<div class="input-holder">
					<input class="search-input" type="text" name="keyword"
						placeholder="">
				</div>
				<span class="search-tag"><span id="search-article">爬文章</span><span id="search-wxnum">爬公众号</span></span>
			</div>
		</div>
		<div class="result">
			<div class="slide">
				<ul>
					<li class="person-info">
						<div class="person-info-container">
							<div class="main">个人信息</div>
							<div class="children" id="person-info">
								<ul class="children-list">
									<li>吕飞</li>
									<li>github.com</li>
									<li>退出登录</li>
								</ul>
							</div>
						</div>
					</li>
					<li>
						<div class="pubnum">
							<div class="main">公众号管理</div>
							<div class="children">
								<ul class="children-list">
									<li id="children-pub-all">全部</li>
									<li id="children-pub-province">省级</li>
									<li id="children-pub-default">其他</li>
								</ul>
							</div>
						</div>
					</li>
					<li>
						<div class="article">
							<div class="main">文章管理</div>
							<div class="children">
								<ul class="children-list">
									<li id="children-art-all">全部文章</li>
									<li id="children-art-positive">正向</li>
									<li id="children-art-negative">负向</li>
									<li id="children-art-balance">中性</li>
								</ul>
							</div>
						</div>
					</li>
				</ul>
			</div>
			<div class="content">
				<div class="rt-container">
					<div class="rt-des">
						<div>
							<span>编号</span>
						</div>
						<div>
							<span>图片</span>
						</div>
						<div>
							<span>详情描述</span>
						</div>
						<div>
							<span>操作</span>
						</div>
					</div>
					<div class="rt-contents">
						<div id="pageLoad"></div>
					</div>
				</div>
			</div>
		</div>

	</div>
	<script src="JS/jquery-3.1.1.min.js"></script>
	<script src="JS/HJpage.js"></script>
	<script src="JS/HJLoadingX.js"></script>
	<script src="JS/template.js" type="text/javascript" charset="utf-8"></script>
	<script language="javascript">
		var HJLoading = new HJLoading('CSS/HJLoadingCSS');
		
		(function($) {
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

			global.getData = function(url, callback) {
				$.ajax({
					type : 'GET',
					url : url,
					success : function(data) {
						if (typeof callback === 'function') {
							callback(data);
						}
					},
					error : function(x, h, r) {
						console && console.log(x, h, r);
					}
				})
			}

			window.global = global;
		})(jQuery || $)
	</script>
	<script type="text/html" id="result-des-tpl">
					<div class="rt-des">
						<div>
							<span>编号</span>
						</div>
						<div>
							<span>图片</span>
						</div>
						<div>
							<span>详情描述</span>
						</div>
						<div>
							<span>操作</span>
						</div>
					</div>
	</script>
		<script type="text/html" id="result-article-des-tpl">
					<div class="rt-des">
						<div>
							<span>编号</span>
						</div>
						<div  id="art-article">
							<span>文章</span>
						</div>
						<div  id="art-op">
							<span>操作</span>
						</div>
						<div id="art-search">
							<input placeholder="搜索文章" onfocus="this.placeholder=''" onblur="this.placeholder='搜索文章'"/>
						</div>
					</div>
	</script>
	<script type="text/html" id="result-tpl">
    {{each data as item i}}
    <div class="rt-content" id="{{item.wx_num}}">
        <div class="number">{{i+1}}</div>
        <div class="rt-header">
            <a target="_blank" href="{{item.wx_num_link}}">
                <img src="{{item.wx_num_img_link}}"/>
            </a>
        </div>
        <div class="rt-body">
            <div class="rt-body-font rt-body-children"><a target="_blank" href="{{item.wx_num_link}}">公众号 ：<span>{{item.wx_num_name}}</span></a></div>
            <div class="rt-body-end rt-body-children">微信号 ：<span>{{item.wx_num}}</span></div>
			<div class="rt-body-children">认证：<span>{{item.authentication?item.authentication:'无认证'}}</span></div>
            <div class="rt-body-level rt-body-children">级别 ：<span>{{item.level?item.level:'没有级别'}}</span></div>
        </div>
        <div class="rt-footer">
            <div class="operation">
                <span class="op-delete">删除</span>
                <span class="op-category">分类
					<ul>
						<li class="category-province">省级</li>
						<li class="category-default">其他</li>
					</ul>
				</span>
            </div>
        </div>
		<div class="rt-refresh">
			<span>链接失效？点这里..</span>
		</div>
    </div>
    {{/each}}
</script>

	<script type="text/html" id="article-tpl">
    {{each data as item i}}
    <div class="rt-content-article" id="{{item.article_id}}">
        <div class="number">{{i+1}}</div>
        <div class="rt-header">
        </div>
        <div class="rt-body">
            <div class="rt-body-title"><a target="_blank" href="{{item.article_url}}"><span>{{item.article_title}}</span></a></div>
            <div class="rt-body-abstract">{{item.article_abstract}}</div>
            <div class="rt-body-others"><span><a target="_blank" href="{{item.article_gzh_url}}"><span>{{item.article_gzh_name}}</span></a></span><span>{{timeConvert(item.article_time)}}</span><span>{{item.category}}</span></div>
        </div>
        <div class="rt-footer">
            <div class="operation">
                <span class="op-delete">删除</span>
                <span class="op-update">更新
					<ul>
						<li class="update-pos">正</li>
						<li class="update-neg">负</li>
						<li class="update-bal">中</li>
					</ul>
				</span>
            </div>
        </div>
		<div class="rt-refresh">
			<span>链接失效？点这里..</span>
		</div>
    </div>
    {{/each}}
</script>

	<script language="javascript">
		(function() {
			var holder = $('.search-wrapper > .input-holder');
			var sInput = $('.search-wrapper input');
			sInput.on('focus', function() {
				holder.addClass('input-focus');
			}).on('blur', function() {
				sInput.val() ? '' : holder.removeClass('input-focus');
			});

		})();
	</script>
	<script>

</script>
	<script language="javascript">
		(function() {
			var content = $('.rt-contents');
			var container = $('.rt-container');
			var des = '';
			var state = '';
			/*content.append(rt);*/

			var input = $('.container>.searchForm input');
			var searchTarget = $('.container .search-tag>span');
			searchTarget.on('click',function(e){
				var  cat = $(e.target).attr('id');
				cat = cat.split('-')[1];
				//检查input值
				var value = $(e.target).parent().prev().children().val();
				if(!value){
					return;
				}
				global.subData('/CLI/search',{type:cat,value:value},function(data){
					if(data.state){
						console.log(data.msg);
						//加载页面
					}
				})
			});
			//插入数据
			template.helper('timeConvert',function(a){
				if(a){
					a = parseInt(a);
					var b,c,d;
					b = parseInt((new Date).getTime()/1E3)-a;
					d = parseInt(b / 86400);
        			c = parseInt(b / 3600);
        			b = parseInt(b / 60);
					if(0 < d && 4 > d){
						return d+ "\u5929\u524d";
					}
					if(0 >= d && 0 < c){
						return c+"\u5c0f\u65f6\u524d";
					}
					if(0 >= c && 0 < b){
						return b+"\u5206\u949f\u524d";
					}
					
					a = new Date(1E3*a);
					return a.getFullYear() + "-" + (a.getMonth() + 1) + "-" + a.getDate();
				}
				return "";
			});
			
			
			var page = 1;
			function pageLoad(curr, options) {
				//操作数据库
/* 				HJLoading.start({
					loadingTPLId:6,
					target:'.container',
					loadingScale:0.1,
					loadingId:'pageLoading'
				}); */
				global.subData('/CLI/' + options.target, {
					page : curr,
					level : options.level,
					title:options.title?options.title:''
				}, function(data) {
					//console.log('subdata successful',data);
					//对文档进行处理

					var result = '';
					if (data.data.length == 0) {
						//啥也没有
						result = "<div class='emptyContent'>没有内容啊</div>"
					}

					if (curr <= data.totalPage) {
						if(options.target==='handleWxNum'){
							result = template('result-tpl', data);
						}else{
							result=template('article-tpl',data);

						}
					}
					
					//移除所有rt-content'
					$('.emptyContent').remove();
					$('.rt-content').remove();
					$('.rt-content-article').remove();
					content.prepend(result);
					//3.操作
					if(options.target==='handleWxNum'){
						var op = $('.rt-content .rt-footer .operation');
						var id = '';
						var category = op.find('.op-category');
						var deleteOp = op.find('.op-delete');
						//失效链接			
						$('.rt-content .rt-refresh span').on('click',function(e){
							id = $(e.target).parents('.rt-content').attr('id');
							global.subData('/CLI/'+options.target+'Op',{action:'refresh',target:id},function(data){
								if(data){
									pageLoad(curr,{action:'refresh',target:options.target,level:options.level});
								}
							});
						});
						if(options.level==="province"){
							category.find('.category-province').css({display:'none'});
						}
						if(options.level === "default"){
							category.find('.category-default').css({display:'none'});
						}	
						category.on('mouseover',function(e){
							$(e.currentTarget).find('ul').css({display:'block'});
						});
						category.on('mouseout',function(e){
							$(e.currentTarget).find('ul').css({display:'none'});
						});
												//失效链接			
						$('.rt-content .rt-refresh span').on('click',function(e){
							id = $(e.target).parents('.rt-content').attr('id');
						});
						
						deleteOp.on('click',function(e){
						    id = $(e.target).parents('.rt-content').attr('id')
							global.subData('/CLI/'+options.target+'Op',{action:'delete',target:id},function(data){
								if(data.state){
									//成功
									pageLoad(curr,{target:options.target,level:options.level});
								}
							});
						});
						
						op.find('.op-category li').on('click',function(e){
							id = $(e.target).parents('.rt-content').attr('id')
							global.subData('/CLI/'+options.target+'Op',{action:'update',target:id,level:e.target.innerText},function(data){
								//回调
								//var tranLevel = e.target.innertext === '省级'?'province':'default';
								if(data.state){
									//弹出对话框并跟新视图
									pageLoad(curr,{target:options.target,level:options.level});
								}
							})									
						})
					}else{
						//操作
						var op = $('.rt-content-article .rt-footer .operation');
						
						var id = '';
						var update = op.find('.op-update');
						var deleteOp = op.find('.op-delete');
						//失效链接			
						$('.rt-content-article .rt-refresh span').on('click',function(e){
							id = $(e.target).parents('.rt-content-article').attr('id');
							global.subData('/CLI/'+options.target+'Op',{action:'refresh',target:id},function(data){
								if(data){
									pageLoad(curr,{target:options.target,level:options.level});
								}
							});
						});
						
						if(options.level==="positive"){
							update.find('.update-pos').css({display:'none'});
						}
						if(options.level === "negative"){
							update.find('.update-neg').css({display:'none'});
						}	
						if(options.level === "balance"){
							update.find('.update-bal').css({display:'none'});
						}
						update.on('mouseover',function(e){
							$(e.currentTarget).find('ul').css({display:'block'});
						});
						update.on('mouseout',function(e){
							$(e.currentTarget).find('ul').css({display:'none'});
						});
						
						
						deleteOp.on('click',function(e){
						    id = $(e.target).parents('.rt-content-article').attr('id')
							global.subData('/CLI/'+options.target+'Op',{action:'delete',target:id},function(data){
								if(data.state){
									//成功
								}
							});
						});
						
						op.find('.op-update li').on('click',function(e){
							id = $(e.target).parents('.rt-content-article').attr('id')
							global.subData('/CLI/'+options.target+'Op',{action:'update',target:id,level:e.target.innerText},function(data){
								//回调
								//var tranLevel = e.target.innertext === '省级'?'province':'default';
								if(data.state){
									//弹出对话框并跟新视图
									pageLoad(curr,{target:options.target,level:options.level});
								}
							})									
						})

					}
					laypage({
						cont : $('#pageLoad')[0],
						pages : data.totalPage,
						curr : curr || 1,
						jump : function(obj, first) {
							if (!first) {
								pageLoad(obj.curr, options);
							}
						}
					});
/* 					setTimeout(function(){
						HJLoading.stop('pageLoading');
					},1000) */
				});
			}
			//分页加载
			//1.对初始的分页
			pageLoad(page, {
				target : 'handleWxNum',
				level : 'all'
			});
			//2.分页
			var li = $('.slide>ul>li');
			var children = li.find('.children');

			li.find('.main').click(function(e) {
				$(e.target).parent().find('.children').toggle(1000);
			});

			var lis = children.find('li');
			lis.each(function(index, value) {
				$(value).on('click', function() {
					lis.removeClass('select');
					$(value).addClass('select');
					var param = $(value).attr('id').replace('children-', '');
					param = param.split('-');
					switch (param[0]) {
					case 'pub':
						if(state!='pub'){
							des = template('result-des-tpl');
							container.find('.rt-des').remove();
							container.prepend(des);
							state = 'pub';
						}
						pageLoad(page, {
							target : 'handleWxNum',
							level : param[1]
						});
						break;
					case 'art':
						if(state!='art'){
							des = template('result-article-des-tpl');
							container.find('.rt-des').remove();
							container.prepend(des);
							//文章搜索
							container.find('.rt-des input').on('keydown',function(e){
								if(e.keyCode === 13){
 									pageLoad(page,{
										target:'handleArticle',
										level:'search',
										title:e.target.value
									}); 
								}
							})
							state = 'art';
						}
						pageLoad(page, {
							target : 'handleArticle',
							level : param[1]
						});
						break;
					default:
						console.error('parameter error');
						break;
					}

				})
			});
		})()
	</script>
</body>
</html>
