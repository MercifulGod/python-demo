package models

import (
	"time"

	"github.com/astaxie/beego/orm"
)

type User struct {
	Id      int       `orm:"pk;auto"` // 注释
	Name    string    `orm:"unique"`
	Age     int       `orm:"default(1)" description:"用户年龄"`
	Created time.Time `orm:"auto_now_add;type(datetime)"`
	Updated time.Time `orm:"auto_now;type(datetime)"`
}

func init() {
	// 需要在init中注册定义的model
	orm.RegisterModel(new(User))
}
