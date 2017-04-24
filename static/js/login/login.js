var bindEventClickSignin = function() {
	var signin = e('#id-signin')
	var signup = e('#id-signup')
	var signinform = e('#id-signin-form')
	var signupform = e('#id-signup-form')
	signin.addEventListener('click', function(){
		var navs = signin.parentElement
		navs.dataset.activeIndex = "1"
		signin.classList.add('active')
		signup.classList.remove('active')
		signinform.classList.add('selected')
		signupform.classList.remove('selected')
	})
}

var bindEventClickSignup = function() {
	var signin = e('#id-signin')
	var signup = e('#id-signup')
	var signinform = e('#id-signin-form')
	var signupform = e('#id-signup-form')
	signup.addEventListener('click', function(){
		var navs = signup.parentElement
		navs.dataset.activeIndex = "0"
		signup.classList.add('active')
		signin.classList.remove('active')
		signupform.classList.add('selected')
		signinform.classList.remove('selected')
	})

}
var	state_dict = {
		100: '登录成功',
		101: '密码或账号错误',
		200: '注册成功',
		201: '用户名已被占用',
		202: '密码过短，最少为6位',
		203: '用户名过短，最少为2位',
	}

var bindEventClickLogin = function() {
	var login_btn = e('#id-btn-login')
	login_btn.addEventListener('click', function() {
		var uname = e('#id-login-uname').value
		var password = e('#id-login-password').value
		form = {
		'username': uname,
		'password': password,
		}
		console.log(form)
		apilogin(form, function(r) {
			code = JSON.parse(r).state
			if(code == 100){
				window.location.href='/topic'
			}
			else{
				console.log('is login erroe')
				var state = state_dict[code]
				alert(state)
			}
			
		})
	})
}

var bindEventClickRegister = function() {
	var register_btn = e('#id-btn-register')
	var signin = e('#id-signin')
	register_btn.addEventListener('click', function() {
		var uname = e('#id-register-uname').value
		var password = e('#id-register-password').value
		form = {
		'username': uname,
		'password': password,
		}
		apiregister(form, function(r) {
			console.log(r)
			code = JSON.parse(r).state
			if(code == 200){
				var state = state_dict[code]
				alert(state)
				signin.click()
			}
			else{
				var state = state_dict[code]
				alert(state)
			}
			
		})
	})
}

var bindEvents = function() {
	bindEventClickSignin()
	bindEventClickSignup()
	bindEventClickLogin()
	bindEventClickRegister()
}


var __main = function() {
	bindEvents()
}


__main()
