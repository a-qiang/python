#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ==============================
# @Author:   RoyLau
# @Version:  1.0
# @DateTime: 2018-05-11 10:27:00
# ==============================

from datetime import datetime
from app import db


# 会员（用户）
class User(db.Model):
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True) 			# id 是 整型，主键，自动递增
	name = db.Column(db.String(100), unique=True) 			# 长度100，字段唯一
	pwd  = db.Column(db.String(100))
	email  = db.Column(db.String(100), unique=True)
	phone  = db.Column(db.String(11), unique=True)
	info  = db.Column(db.Text) 								# 个人简介
	face  = db.Column(db.String(255), unique=True)			# 用户头像
	addtime  = db.Column(db.DateTime, index = True, default = datetime.utcnow) 	# 注册时间
	uuid = db.Column(db.String(255), unique=True) 			# 唯一标志符
	userlogs = db.relationship('Userlog', backref='user') 	# 会员日志外键关系
	comments = db.relationship('Comment', backref='user') 	# 评论外键关系
	moviecols = db.relationship('Moviecol', backref='user') 	# 收藏外键关系

	def __repr__(self):
		return "<User %r>" % self.name # %r 占位符，name 昵称

	def check_pwd(self, pwd):
		from werkzeug.security import check_password_hash
		return check_password_hash(self.pwd, pwd)
# 会员登录日志
class Userlog(db.Model):
	__tablename__ = "userlog"
	id = db.Column(db.Integer, primary_key=True) 				# id 是 整型，主键，自动递增
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 	# 整型，定义一个外键（user的id）
	ip = db.Column(db.String(100))								# 登录id
	addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow) # 当前时间，索引，默认时间

	def __repr__(self):
		return "<Userlog %r>" % self.id

# 标签
class Tag(db.Model):
	__tablename__ = "tag"
	id = db.Column(db.Integer, primary_key=True)	# 编号
	name = db.Column(db.String(100), unique=True) 	# 标题
	addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow) # 添加时间
	movies = db.relationship("Movie", backref="tag") # 电影外键关系的关联

	def __repr__(self):
		return "<Tag $r>" % self.name

# 电影
class Movie(db.Model):
	__tablename__ = "movie"
	id = db.Column(db.Integer, primary_key=True) 	# 编号
	title = db.Column(db.String(255), unique=True) 	# 标题
	url = db.Column(db.String(255), unique=True) 	# 地址
	info = db.Column(db.Text) 				# 简介
	logo = db.Column(db.String(255), unique=True) 	# 封面
	star = db.Column(db.SmallInteger) 		# 星级
	playnum = db.Column(db.BigInteger) 		# 播放量
	commentnum = db.Column(db.BigInteger) 	# 评论
	tag_id = db.Column(db.Integer, db.ForeignKey('tag.id')) # 所属标签
	area = db.Column(db.String(255)) 		# 上映地区
	release = db.Column(db.Date) 			# 上映时间
	length = db.Column(db.String(100)) 		# 播放时间
	addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow) # 添加时间
	comments = db.relationship('Comment', backref='movie') 		# 电影外键关系的关联
	moviecols = db.relationship('Moviecol', backref='movie') 	# 收藏外键关系

	def __repr__(self):
		return "<Movie %r>" % self.title

# 上映预告
class Preview(db.Model):
	__tablename__ = "preview"
	id = db.Column(db.Integer, primary_key=True) 	# 编号
	title = db.Column(db.String(255), unique=True) 	# 标题
	logo = db.Column(db.String(255), unique=True) 	# 封面
	addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow) # 添加时间

	def __repr__(self):
		return "<Preview %r>" % self.title

# 评论
class Comment(db.Model):
	__tablename__ = "comment"
	id = db.Column(db.Integer, primary_key=True) 	# 编号
	content = db.Column(db.Text) 					# 内容
	movie_id = db.Column(db.Integer, db.ForeignKey('movie.id')) # 所属电影
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 	# 所属用户
	addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow) # 添加时间

	def __repr__(self):
		return "<Comment %r>" % self.id

# 电影收藏
class Moviecol(db.Model):
	__tablename__ = "moviecol"
	id = db.Column(db.Integer, primary_key=True) # 编号
	movie_id = db.Column(db.Integer, db.ForeignKey('movie.id')) # 所属电影
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 	# 所属用户
	addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow) # 添加时间

	def __repr__(self):
		return "<Moviecol %r>" % self.id

# 权限
class Auth(db.Model):
	__tablename__ = "auth"
	id = db.Column(db.Integer, primary_key=True) 	# 编号
	name = db.Column(db.String(100), unique=True) 	# 名称
	url = db.Column(db.String(255), unique=True) 	# 地址
	addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow) # 添加时间

	def __repr__(self):
		return "<Auth %r>" % self.name

# 角色
class Role(db.Model):
	__tablename__ = "role"
	id = db.Column(db.Integer, primary_key=True) 	# 编号
	name = db.Column(db.String(100), unique=True) 	# 名称
	auths = db.Column(db.String(600)) 				# 权限
	addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow) # 创建时间按
	admins = db.relationship("Admin", backref='role') 	# 管理员外键关系关联

	def __repr__(self):
		return "<Role %r>" % self.name

# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  	# 编号
    name = db.Column(db.String(100), unique=True)  	# 管理员账号
    pwd = db.Column(db.String(100))  		# 管理员密码
    is_super = db.Column(db.SmallInteger)  	# 是否为超级管理员，0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  	# 所属角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    adminlogs = db.relationship("Adminlog", backref='admin')  	# 管理员登录日志外键关系关联
    oplogs = db.relationship("Oplog", backref='admin')  		# 管理员操作日志外键关系关联

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# 操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  	# 登录IP
    reason = db.Column(db.String(600))  # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Oplog %r>" % self.id


if __name__ == "__main__":
    db.create_all()

    role = Role(
        name="超级管理员",
        auths=""
    )
    db.session.add(role)
    db.session.commit()
    from werkzeug.security import generate_password_hash # 转换密码用到的库

    admin = Admin(
        name="imoocmovie",
        pwd=generate_password_hash("123456"),
        is_super=0,
        role_id=1
    )
    db.session.add(admin)
    db.session.commit()