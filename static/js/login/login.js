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
		100: 'OK',
		101: '用户名已被占用',
		102: '密码或账号错误',
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
}


var __main = function() {
	bindEvents()
}


__main()
