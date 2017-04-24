var e = function(sel) {
	return document.querySelector(sel)
}

// method：请求方法 path：请求路径 data：请求数据 Callback：回调函数
var ajax = function(method, path, data, responseCallback) {
	// new 一个 XMLHttpRequest 对象
	var r = new XMLHttpRequest()
	// 设置 method，path，Async=true（异步）
	r.open(method, path, true)
	// 设置请求格式为 json
	r.setRequestHeader('Content-Type', 'application/json')
	// 监测 r 的变化
	r.onreadystatechange = function() {
		// 当返回数据准备完成时（r.readyState 为 4 时）执行回调函数
		if(r.readyState === 4) {
			// r.response 为响应的 body
			responseCallback(r.response)
		}
	}
	data = JSON.stringify(data)
    // 发送请求
    r.send(data)
}

// 注册API
var apilogin = function(form, callback) {
	console.log('api')
	var path = '/login'
	ajax('POST', path, form, callback)
}

var apiregister = function(form, callback) {
	var path = '/register'
	ajax('POST', path, form, callback)
}