package routers

import (
	"blog/controllers"

	"github.com/astaxie/beego"
)

func init() {
	beego.Router("/user/get", &controllers.UserController{}, "get:GetUser")
	beego.Router("/user/list", &controllers.UserController{}, "get:ListUser")
	beego.Router("/user/create", &controllers.UserController{}, "post:CreateUser")
	beego.Router("/user/update", &controllers.UserController{}, "get,post:UpdateUser")
	beego.Router("/user/delete", &controllers.UserController{}, "get,post:DeleteUser")
}
