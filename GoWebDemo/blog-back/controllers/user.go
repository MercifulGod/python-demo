package controllers

import (
	"blog/models"
	"strconv"

	"github.com/astaxie/beego"
	"github.com/astaxie/beego/orm"
)

type JSONS struct {
	//必须的大写开头
	Code  string       `json:"code"`
	Total int64        `json:"total"`
	Rows  []orm.Params `json:"rows"`
}
type UserController struct {
	beego.Controller
}

func (this *UserController) ListUser() {
	name := this.GetString("search")
	offset, _ := this.GetInt("offset")
	limit, _ := this.GetInt("limit")
	o := orm.NewOrm()
	qs := o.QueryTable("user")
	total, _ := qs.Count()
	if name != "" {
		qs = qs.Filter("name", name)
	}
	if limit != 0 || offset != 0 {
		qs = qs.Offset(offset).Limit(limit)
		beego.Info(offset)
		beego.Info(limit)
	}

	var users []orm.Params
	_, err := qs.Values(&users, "id", "name", "age")
	if err == orm.ErrMultiRows {
		// 多条的时候报错
		beego.Info("Returned Multi Rows Not One")
	}
	if err == orm.ErrNoRows {
		// 没有找到记录
		beego.Info("Not row found")
	}

	// var data JSONS
	// data.Total = num
	// data.Rows = users
	data := JSONS{"200", total, users}
	this.Data["json"] = &data
	this.ServeJSON()
}

func (this *UserController) GetUser() {
	id := this.GetString("id")
	beego.Info("UserID ", id)

	o := orm.NewOrm()

	// var user models.User
	// err := o.QueryTable("user").Filter("id", id).One(&user)

	var users []orm.Params
	_, err := o.QueryTable("user").Filter("id", id).Values(&users, "id", "name", "age")
	if err == orm.ErrMultiRows {
		// 多条的时候报错
		beego.Info("Returned Multi Rows Not One")
	}
	if err == orm.ErrNoRows {
		// 没有找到记录
		beego.Info("Not row found")
	}
	// var data = make(map[string]string)
	this.Data["json"] = &users
	this.ServeJSON()
}

func (this *UserController) CreateUser() {
	name := this.GetString("name")
	age := this.Input().Get("age")
	ageInt, _ := strconv.Atoi(age)
	var user models.User
	user.Name = name
	user.Age = ageInt

	beego.Debug(user)

	o := orm.NewOrm()
	_, err := o.Insert(&user)
	var data = make(map[string]string)
	data["success"] = "0"
	if err == nil {
		data["success"] = "1"
	}
	this.Data["json"] = &data
	this.ServeJSON()
}

func (this *UserController) UpdateUser() {
	id := this.GetString("id")
	idInt, _ := strconv.Atoi(id)
	name := this.GetString("name")
	age := this.Input().Get("age")
	ageInt, _ := strconv.Atoi(age)

	var data = make(map[string]string)
	data["success"] = "0"
	data["mes"] = "更新用户失败"

	o := orm.NewOrm()
	user := models.User{Id: idInt}
	if o.Read(&user) == nil {
		user.Name = name
		user.Age = ageInt
		if _, err := o.Update(&user); err == nil {
			data["success"] = "1"
			data["mes"] = "更新用户成功"
		}
	}
	this.Data["json"] = &data
	this.ServeJSON()
}

func (this *UserController) DeleteUser() {
	id := this.GetString("id")
	idInt, _ := strconv.Atoi(id)

	var data = make(map[string]string)
	data["success"] = "0"
	data["mes"] = "删除用户失败"

	o := orm.NewOrm()
	if _, err := o.Delete(&models.User{Id: idInt}); err == nil {
		data["success"] = "1"
		data["mes"] = "删除用户成功"
	}
	this.Data["json"] = &data
	this.ServeJSON()
}
