# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, session, g
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from apps import app, db
from apps.forms import ArticleForm, CommentForm, ForumForm, JoinForm, LoginForm

from apps.models import (Forum, Board, QnA, QnAComment, Comment, BoardComment, Free, FreeComment, Notice, Humor, HumorComment, FAQ, FAQComment, Member, K_Univ, I_Univ, R_Univ)

@app.route('/', methods=['GET','POST'])
def index():
	if 'user_email' in session:
		return render_template("main.html", username= session['user_email'])
	
	return render_template('main.html')

@app.route('/columbia', methods=['GET','POST'])
def columbia():	
	return render_template('univ/columbia.html')
@app.route('/edinburgh', methods=['GET','POST'])
def edinburgh():	
	return render_template('univ/edinburgh.html')
@app.route('/north', methods=['GET','POST'])
def north():	
	return render_template('univ/north.html')
@app.route('/emory', methods=['GET','POST'])
def emory():	
	return render_template('univ/emory.html')
@app.route('/waseda', methods=['GET','POST'])
def waseda():	
	return render_template('univ/waseda.html')
@app.route('/malaya', methods=['GET','POST'])
def malaya():	
	return render_template('univ/malaya.html')
@app.route('/toronto', methods=['GET','POST'])
def toronto():	
	return render_template('univ/toronto.html')
@app.route('/san', methods=['GET','POST'])
def san():	
	return render_template('univ/sandiego.html')
@app.route('/about', methods=['GET','POST'])
def about():	
	return render_template('about.html')

@app.route('/join', methods=['GET','POST'])
def member_join():
	form = JoinForm()

	if request.method == 'POST':
		if form.validate_on_submit():

			user = Member(
				email=form.email.data,
				pw=generate_password_hash(form.password.data),
				name=form.name.data,
				grade=form.grade.data,
				major=form.major.data,
				univname=form.univname.data
				)	
			db.session.add(user)
			db.session.commit()

			flash(u'가입이 완료 되었습니다.','success')
			return redirect(url_for('index'))
	return render_template('user/join.html' , form=form, active_tab='member_join')

@app.route('/login', methods=['POST','GET'])
def log_in():
	form = LoginForm()

	if request.method == 'POST':
		if form.validate_on_submit():
			email = form.email.data
			pw = form.password.data

			user = Member.query.get(email)

			if user is None:
				flash(u'존재하지 않는 E-mail입니다.', 'danger')
			elif not check_password_hash(user.pw, pw):
				flash(u'비밀번호가 일치하지 않습니다.', 'danger')
			else:
				session.permanent = True
				session['user_email'] = user.email
				session['user_name'] = user.name

				flash(u'로그인 완료', 'success')
				return redirect(url_for('index'))
	return render_template('user/login.html', form=form, active_tab='log_in')

@app.route('/logout', methods=['POST','GET'])
def log_out():
	session.clear()
	return redirect(url_for('index'))

@app.before_request
def befor_request():
	g.user_name = None
	if 'user_email' in session:
		g.user_name = session['user_name']
		g.user_email = session['user_email']

	#구현해야 하는 부분...
	#예제임...
@app.route('/admin/board/create/', methods=['GET','POST'])
def admin_create():
	form = AdminBoardForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			# 사용자가 입력한 글 데이터로 Article 모델 인스턴스를 생성한다.
			board = Board(
				board = form.board_name.data
				)

			# 데이터베이스에 데이터를 저장할 준비를 한다. (게시글)
			db.session.add(board)
			# 데이터베이스에 저장하라는 명령을 한다.
			db.session.commit()

			flash(u'게시판을 생성하였습니다.', 'success')
		return redirect(url_for('board_list'))#추가 되지 않은 함수 : board_list

		context = {	}

		context['board_list'] = Board.query.order_by(desc(Board.board_id)).all()
	return render_template('admin/board.html', form=form, context = context, active_tab='board_create')
##################외국대학교#############
@app.route('/univ', methods=['GET', 'POST'])
def univ_list():
	context = {	}

	context['univ_list'] = I_Univ.query.order_by(desc(I_Univ.date_created)).all()
	if context['univ_list'] :
		return render_template('univ.html', context=context, active_tab='univ_bar')
	else :
		return render_template('univ.html')

@app.route('/univ/create/', methods=['GET','POST'])
def univ_create():
	if g.admin_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		if request.method == 'POST':
			if form.validate_on_submit():
				# 사용자가 입력한 글 데이터로 Article 모델 인스턴스를 생성한다.
				univ = I_Univ(
					name=form.u.data,
					author=form.author.data,
					content=form.content.data
					)

				# 데이터베이스에 데이터를 저장할 준비를 한다. (게시글)
				db.session.add(univ)
				# 데이터베이스에 저장하라는 명령을 한다.
				db.session.commit()

				flash(u'univ을 작성하였습니다.', 'success')
			return redirect(url_for('univ_list'))

		return render_template('univ/create.html', form=form, active_tab='univ_create')

@app.route('/univ/detail/<int:id>', methods=['GET'])
def univ_detail(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		univ = univ.query.get(id)
		# comments = Comment.query.order_by(desc(Comment.date_created)).filter_by(article=article)

		# relationship을 활용한 query
		comments = univ.comments.order_by(desc(Comment.date_created)).all()

		return render_template('univ/detail.html', univ=univ, comments=comments)


@app.route('/univ/update/<int:id>', methods=['GET', 'POST'])
def univ_update(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		univ = univ.query.get(id)
		form = univForm(request.form, obj=univ)
		if request.method == 'POST':
			if form.validate_on_submit():
				form.populate_obj(univ)
				db.session.commit()
			return redirect(url_for('univ_detail', id=id))

		return render_template('univ/update.html', form=form)


@app.route('/univ/delete/<int:id>', methods=['GET', 'POST'])
def univ_delete(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		if request.method == 'GET':
			return render_template('univ/delete.html', univ_id=id)
		elif request.method == 'POST':
			univ_id = request.form['univ_id']
			univ = univ.query.get(univ_id)
			db.session.delete(univ)
			db.session.commit()

			flash(u'질문을 삭제하였습니다.', 'success')
			return redirect(url_for('univ_list'))

#################포럼게시판################### 
@app.route('/forum', methods=['GET', 'POST'])
def forum_list():
	context = {	}

	context['forum_list'] = Forum.query.order_by(desc(Forum.date_created)).all()
	if context['forum_list'] :
		return render_template('forum.html', context=context, active_tab='forum_bar')
	else :
		return render_template('forum.html')

@app.route('/forum/create/', methods=['GET','POST'])
def forum_create():
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		form = ForumForm()
		if request.method == 'POST':
			if form.validate_on_submit():
				# 사용자가 입력한 글 데이터로 Article 모델 인스턴스를 생성한다.
				forum = Forum(
					title=form.title.data,
					author=form.author.data,
					content=form.content.data
					)

				# 데이터베이스에 데이터를 저장할 준비를 한다. (게시글)
				db.session.add(forum)
				# 데이터베이스에 저장하라는 명령을 한다.
				db.session.commit()

				flash(u'Forum을 작성하였습니다.', 'success')
			return redirect(url_for('forum_list'))

		return render_template('forum/create.html', form=form, active_tab='forum_create')

@app.route('/forum/detail/<int:id>', methods=['GET'])
def forum_detail(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		forum = Forum.query.get(id)
		# comments = Comment.query.order_by(desc(Comment.date_created)).filter_by(article=article)

		# relationship을 활용한 query
		comments = forum.comments.order_by(desc(Comment.date_created)).all()

		return render_template('forum/detail.html', forum=forum, comments=comments)


@app.route('/forum/update/<int:id>', methods=['GET', 'POST'])
def forum_update(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		forum = Forum.query.get(id)
		form = ForumForm(request.form, obj=forum)
		if request.method == 'POST':
			if form.validate_on_submit():
				form.populate_obj(forum)
				db.session.commit()
			return redirect(url_for('forum_detail', id=id))

		return render_template('forum/update.html', form=form)


@app.route('/forum/delete/<int:id>', methods=['GET', 'POST'])
def forum_delete(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		if request.method == 'GET':
			return render_template('forum/delete.html', forum_id=id)
		elif request.method == 'POST':
			forum_id = request.form['forum_id']
			forum = Forum.query.get(forum_id)
			db.session.delete(forum)
			db.session.commit()

			flash(u'질문을 삭제하였습니다.', 'success')
			return redirect(url_for('forum_list'))

@app.route('/comment/create/<int:forum_id>', methods=['GET', 'POST'])
def comment_create(forum_id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		form = CommentForm()
		if request.method == 'POST':
			if form.validate_on_submit():
				# comment = Comment(
				#     author=form.author.data,
				#     email=form.email.data,
				#     content=form.content.data,
				#     password=form.password.data,
				#     article_id=article_id
				# )
				comment = Comment(
					author=form.author.data,
					email=form.email.data,
					content=form.content.data,
					password=form.password.data,
					forum=Forum.query.get(forum_id)
					)

				db.session.add(comment)
				db.session.commit()

				flash(u'댓글을 작성하였습니다.', 'success')
			return redirect(url_for('forum_detail', id=forum_id))
		return render_template('comment/create.html', form=form)
###################qna게시판############
@app.route('/qna', methods=['GET', 'POST'])
def qna_list():
	context = {	}

	context['qna_list'] = QnA.query.order_by(desc(QnA.date_created)).all()
	if context['qna_list'] :
		return render_template('qna.html', context=context, active_tab='qna_bar')
	else :
		return render_template('qna.html')

@app.route('/qna/create/', methods=['GET','POST'])
def qna_create():
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		form = ForumForm()
		if request.method == 'POST':
			if form.validate_on_submit():
				# 사용자가 입력한 글 데이터로 Article 모델 인스턴스를 생성한다.
				qna = QnA(
					title=form.title.data,
					author=form.author.data,
					content=form.content.data
					)

				# 데이터베이스에 데이터를 저장할 준비를 한다. (게시글)
				db.session.add(qna)
				# 데이터베이스에 저장하라는 명령을 한다.
				db.session.commit()

				flash(u'QnA을 작성하였습니다.', 'success')
			return redirect(url_for('qna_list'))

		return render_template('qna/create.html', form=form, active_tab='qna_create')

@app.route('/qna/detail/<int:id>', methods=['GET'])
def qna_detail(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		qna = QnA.query.get(id)
		# comments = Comment.query.order_by(desc(Comment.date_created)).filter_by(article=article)

		# relationship을 활용한 query
		comments = qna.comments.order_by(desc(QnAComment.date_created)).all()

		return render_template('qna/detail.html', qna=qna, comments=comments)


@app.route('/qna/update/<int:id>', methods=['GET', 'POST'])
def qna_update(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		qna = QnA.query.get(id)
		form = ForumForm(request.form, obj=forum)
		if request.method == 'POST':
			if form.validate_on_submit():
				form.populate_obj(qna)
				db.session.commit()
			return redirect(url_for('qna_detail', id=id))

		return render_template('qna/update.html', form=form)


@app.route('/qna/delete/<int:id>', methods=['GET', 'POST'])
def qna_delete(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		if request.method == 'GET':
			return render_template('qna/delete.html', qna_id=id)
		elif request.method == 'POST':
			qna_id = request.form['qna_id']
			qna = QnA.query.get(qna_id)
			db.session.delete(qna)
			db.session.commit()

			flash(u'질문을 삭제하였습니다.', 'success')
			return redirect(url_for('qna_list'))

@app.route('/qcomment/create/<int:qna_id>', methods=['GET', 'POST'])
def qcomment_create(qna_id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		form = CommentForm()
		if request.method == 'POST':
			if form.validate_on_submit():
				# comment = Comment(
				#     author=form.author.data,
				#     email=form.email.data,
				#     content=form.content.data,
				#     password=form.password.data,
				#     article_id=article_id
				# )
				comment = QnAComment(
					author=form.author.data,
					email=form.email.data,
					content=form.content.data,
					password=form.password.data,
					qna=QnA.query.get(qna_id)
					)

				db.session.add(comment)
				db.session.commit()

				flash(u'댓글을 작성하였습니다.', 'success')
			return redirect(url_for('qna_detail', id=qna_id))
		return render_template('qcomment/create.html', form=form)
##############board#####################
@app.route('/board', methods=['GET', 'POST'])
def board_list():
	context = {	}

	context['board_list'] = Board.query.order_by(desc(Board.date_created)).all()
	if context['board_list'] :
		return render_template('board.html', context=context, active_tab='board_bar')
	else :
		return render_template('board.html')

@app.route('/board/create/', methods=['GET','POST'])
def board_create():
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		form = ForumForm()
		if request.method == 'POST':
			if form.validate_on_submit():
				# 사용자가 입력한 글 데이터로 Article 모델 인스턴스를 생성한다.
				board = Board(
					title=form.title.data,
					author=form.author.data,
					content=form.content.data
					)

				# 데이터베이스에 데이터를 저장할 준비를 한다. (게시글)
				db.session.add(board)
				# 데이터베이스에 저장하라는 명령을 한다.
				db.session.commit()

				flash(u'게시글을 작성하였습니다.', 'success')
			return redirect(url_for('board_list'))

		return render_template('board/create.html', form=form, active_tab='board_create')

@app.route('/board/detail/<int:id>', methods=['GET'])
def board_detail(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		board = Board.query.get(id)
		# comments = Comment.query.order_by(desc(Comment.date_created)).filter_by(article=article)

		# relationship을 활용한 query
		comments = board.comments.order_by(desc(BoardComment.date_created)).all()

		return render_template('board/detail.html', board=board, comments=comments)


@app.route('/board/update/<int:id>', methods=['GET', 'POST'])
def board_update(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		board = Board.query.get(id)
		form = ForumForm(request.form, obj=forum)
		if request.method == 'POST':
			if form.validate_on_submit():
				form.populate_obj(board)
				db.session.commit()
			return redirect(url_for('board_detail', id=id))

		return render_template('board/update.html', form=form)


@app.route('/board/delete/<int:id>', methods=['GET', 'POST'])
def board_delete(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		if request.method == 'GET':
			return render_template('board/delete.html', board_id=id)
		elif request.method == 'POST':
			board_id = request.form['board_id']
			board = Board.query.get(board_id)
			db.session.delete(board)
			db.session.commit()

			flash(u'질문을 삭제하였습니다.', 'success')
			return redirect(url_for('board_list'))

@app.route('/bcomment/create/<int:qna_id>', methods=['GET', 'POST'])
def bcomment_create(board_id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		form = CommentForm()
		if request.method == 'POST':
			if form.validate_on_submit():
				# comment = Comment(
				#     author=form.author.data,
				#     email=form.email.data,
				#     content=form.content.data,
				#     password=form.password.data,
				#     article_id=article_id
				# )
				comment = BoardComment(
					author=form.author.data,
					email=form.email.data,
					content=form.content.data,
					password=form.password.data,
					board=Board.query.get(board_id)
					)

				db.session.add(comment)
				db.session.commit()

				flash(u'댓글을 작성하였습니다.', 'success')
			return redirect(url_for('board_detail', id=board_id))
		return render_template('bcomment/create.html', form=form)
#####################free######################
@app.route('/free', methods=['GET', 'POST'])
def free_list():
	context = {	}

	context['free_list'] = Free.query.order_by(desc(Free.date_created)).all()
	if context['free_list'] :
		return render_template('free.html', context=context, active_tab='free_bar')
	else :
		return render_template('free.html')

@app.route('/free/create/', methods=['GET','POST'])
def free_create():
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		form = ForumForm()
		if request.method == 'POST':
			if form.validate_on_submit():
				# 사용자가 입력한 글 데이터로 Article 모델 인스턴스를 생성한다.
				free = Free(
					title=form.title.data,
					author=form.author.data,
					content=form.content.data
					)

				# 데이터베이스에 데이터를 저장할 준비를 한다. (게시글)
				db.session.add(free)
				# 데이터베이스에 저장하라는 명령을 한다.
				db.session.commit()

				flash(u'게시글을 작성하였습니다.', 'success')
			return redirect(url_for('free_list'))

		return render_template('free/create.html', form=form, active_tab='free_create')

@app.route('/free/detail/<int:id>', methods=['GET'])
def free_detail(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		free = Free.query.get(id)
		# comments = Comment.query.order_by(desc(Comment.date_created)).filter_by(article=article)

		# relationship을 활용한 query
		comments = free.comments.order_by(desc(FreeComment.date_created)).all()

		return render_template('free/detail.html', free=free, comments=comments)


@app.route('/free/update/<int:id>', methods=['GET', 'POST'])
def free_update(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		free = Free.query.get(id)
		form = ForumForm(request.form, obj=forum)
		if request.method == 'POST':
			if form.validate_on_submit():
				form.populate_obj(free)
				db.session.commit()
			return redirect(url_for('free_detail', id=id))

		return render_template('free/update.html', form=form)


@app.route('/free/delete/<int:id>', methods=['GET', 'POST'])
def free_delete(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		if request.method == 'GET':
			return render_template('free/delete.html', free_id=id)
		elif request.method == 'POST':
			free_id = request.form['free_id']
			free = Free.query.get(free_id)
			db.session.delete(free)
			db.session.commit()

			flash(u'질문을 삭제하였습니다.', 'success')
			return redirect(url_for('free_list'))

@app.route('/frcomment/create/<int:free_id>', methods=['GET', 'POST'])
def frcomment_create(free_id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		form = CommentForm()
		if request.method == 'POST':
			if form.validate_on_submit():
				# comment = Comment(
				#     author=form.author.data,
				#     email=form.email.data,
				#     content=form.content.data,
				#     password=form.password.data,
				#     article_id=article_id
				# )
				comment = FreeComment(
					author=form.author.data,
					email=form.email.data,
					content=form.content.data,
					password=form.password.data,
					free=Free.query.get(free_id)
					)

				db.session.add(comment)
				db.session.commit()

				flash(u'댓글을 작성하였습니다.', 'success')
			return redirect(url_for('free_detail', id=free_id))
		return render_template('frcomment/create.html', form=form)
##################humor##################
@app.route('/humor', methods=['GET', 'POST'])
def humor_list():
	context = {	}

	context['humor_list'] = Humor.query.order_by(desc(Humor.date_created)).all()
	if context['humor_list'] :
		return render_template('humor.html', context=context, active_tab='humor_bar')
	else :
		return render_template('humor.html')

@app.route('/humor/create/', methods=['GET','POST'])
def humor_create():
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		form = ForumForm()
		if request.method == 'POST':
			if form.validate_on_submit():
				# 사용자가 입력한 글 데이터로 Article 모델 인스턴스를 생성한다.
				humor = Humor(
					title=form.title.data,
					author=form.author.data,
					content=form.content.data
					)

				# 데이터베이스에 데이터를 저장할 준비를 한다. (게시글)
				db.session.add(humor)
				# 데이터베이스에 저장하라는 명령을 한다.
				db.session.commit()

				flash(u'게시글을 작성하였습니다.', 'success')
			return redirect(url_for('humor_list'))

		return render_template('humor/create.html', form=form, active_tab='humor_create')

@app.route('/humor/detail/<int:id>', methods=['GET'])
def humor_detail(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		humor = Humor.query.get(id)
		# comments = Comment.query.order_by(desc(Comment.date_created)).filter_by(article=article)

		# relationship을 활용한 query
		comments = humor.comments.order_by(desc(HumorComment.date_created)).all()

		return render_template('humor/detail.html', humor=humor, comments=comments)


@app.route('/humor/update/<int:id>', methods=['GET', 'POST'])
def humor_update(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		humor = Humor.query.get(id)
		form = ForumForm(request.form, obj=forum)
		if request.method == 'POST':
			if form.validate_on_submit():
				form.populate_obj(humor)
				db.session.commit()
			return redirect(url_for('humor_detail', id=id))

		return render_template('humor/update.html', form=form)


@app.route('/humor/delete/<int:id>', methods=['GET', 'POST'])
def humor_delete(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		if request.method == 'GET':
			return render_template('humor/delete.html', humor_id=id)
		elif request.method == 'POST':
			humor_id = request.form['humor_id']
			humor = Humor.query.get(humor_id)
			db.session.delete(humor)
			db.session.commit()

			flash(u'질문을 삭제하였습니다.', 'success')
			return redirect(url_for('humor_list'))

@app.route('/hcomment/create/<int:humor_id>', methods=['GET', 'POST'])
def hcomment_create(humor_id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		form = CommentForm()
		if request.method == 'POST':
			if form.validate_on_submit():
				# comment = Comment(
				#     author=form.author.data,
				#     email=form.email.data,
				#     content=form.content.data,
				#     password=form.password.data,
				#     article_id=article_id
				# )
				comment = HumorComment(
					author=form.author.data,
					email=form.email.data,
					content=form.content.data,
					password=form.password.data,
					humor=Humor.query.get(humor_id)
					)

				db.session.add(comment)
				db.session.commit()

				flash(u'댓글을 작성하였습니다.', 'success')
			return redirect(url_for('humor_detail', id=humor_id))
		return render_template('hcomment/create.html', form=form)
##############notice#################
@app.route('/notice', methods=['GET', 'POST'])
def notice_list():
	context = {	}

	context['notice_list'] = Notice.query.order_by(desc(Notice.date_created)).all()
	if context['notice_list'] :
		return render_template('notice.html', context=context, active_tab='notice_bar')
	else :
		return render_template('notice.html')

@app.route('/notice/create/', methods=['GET','POST'])
def notice_create():
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		form = ForumForm()
		if request.method == 'POST':
			if form.validate_on_submit():
				# 사용자가 입력한 글 데이터로 Article 모델 인스턴스를 생성한다.
				notice = Notice(
					title=form.title.data,
					author=form.author.data,
					content=form.content.data
					)

				# 데이터베이스에 데이터를 저장할 준비를 한다. (게시글)
				db.session.add(notice)
				# 데이터베이스에 저장하라는 명령을 한다.
				db.session.commit()

				flash(u'게시글을 작성하였습니다.', 'success')
			return redirect(url_for('notice_list'))

		return render_template('notice/create.html', form=form, active_tab='notice_create')

@app.route('/notice/detail/<int:id>', methods=['GET'])
def notice_detail(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		notice = Notice.query.get(id)
		# comments = Comment.query.order_by(desc(Comment.date_created)).filter_by(article=article)

		# relationship을 활용한 query
		return render_template('notice/detail.html', notice=notice, comments=comments)


@app.route('/notice/update/<int:id>', methods=['GET', 'POST'])
def notice_update(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		notice = Notice.query.get(id)
		form = ForumForm(request.form, obj=forum)
		if request.method == 'POST':
			if form.validate_on_submit():
				form.populate_obj(notice)
				db.session.commit()
			return redirect(url_for('notice_detail', id=id))

		return render_template('notice/update.html', form=form)


@app.route('/notice/delete/<int:id>', methods=['GET', 'POST'])
def notice_delete(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		if request.method == 'GET':
			return render_template('notice/delete.html', notice_id=id)
		elif request.method == 'POST':
			notice_id = request.form['notice_id']
			notice = Humor.query.get(notice_id)
			db.session.delete(notice)
			db.session.commit()

			flash(u'질문을 삭제하였습니다.', 'success')
			return redirect(url_for('notice_list'))
###################FAQ####################
@app.route('/faq', methods=['GET', 'POST'])
def faq_list():
	context = {	}

	context['faq_list'] = FAQ.query.order_by(desc(FAQ.date_created)).all()
	if context['faq_list'] :
		return render_template('faq.html', context=context, active_tab='faq_bar')
	else :
		return render_template('faq.html')

@app.route('/faq/create/', methods=['GET','POST'])
def faq_create():
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		form = ForumForm()
		if request.method == 'POST':
			if form.validate_on_submit():
				# 사용자가 입력한 글 데이터로 Article 모델 인스턴스를 생성한다.
				faq = FAQ(
					title=form.title.data,
					author=form.author.data,
					content=form.content.data
					)

				# 데이터베이스에 데이터를 저장할 준비를 한다. (게시글)
				db.session.add(faq)
				# 데이터베이스에 저장하라는 명령을 한다.
				db.session.commit()

				flash(u'게시글을 작성하였습니다.', 'success')
			return redirect(url_for('faq_list'))

		return render_template('faq/create.html', form=form, active_tab='faq_create')

@app.route('/faq/detail/<int:id>', methods=['GET'])
def faq_detail(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		faq = FAQ.query.get(id)
		# comments = Comment.query.order_by(desc(Comment.date_created)).filter_by(article=article)

		# relationship을 활용한 query
		comments = faq.comments.order_by(desc(FAQComment.date_created)).all()

		return render_template('faq/detail.html', faq=faq, comments=comments)


@app.route('/faq/update/<int:id>', methods=['GET', 'POST'])
def faq_update(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		faq = FAQ.query.get(id)
		form = ForumForm(request.form, obj=forum)
		if request.method == 'POST':
			if form.validate_on_submit():
				form.populate_obj(faq)
				db.session.commit()
			return redirect(url_for('faq_detail', id=id))

		return render_template('faq/update.html', form=form)


@app.route('/faq/delete/<int:id>', methods=['GET', 'POST'])
def faq_delete(id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		if request.method == 'GET':
			return render_template('faq/delete.html', faq_id=id)
		elif request.method == 'POST':
			faq_id = request.form['faq_id']
			faq = FAQ.query.get(faq_id)
			db.session.delete(faq)
			db.session.commit()

			flash(u'질문을 삭제하였습니다.', 'success')
			return redirect(url_for('faq_list'))

@app.route('/fcomment/create/<int:faq_id>', methods=['GET', 'POST'])
def fcomment_create(humor_id):
	if g.user_name == None:
		flash(u'로그인 후 이용해 주세요.', 'danger')
		return redirect(url_for('log_in'))
	else:
		form = CommentForm()
		if request.method == 'POST':
			if form.validate_on_submit():
				# comment = Comment(
				#     author=form.author.data,
				#     email=form.email.data,
				#     content=form.content.data,
				#     password=form.password.data,
				#     article_id=article_id
				# )
				comment = FAQComment(
					author=form.author.data,
					email=form.email.data,
					content=form.content.data,
					password=form.password.data,
					faq=FAQ.query.get(faq_id)
					)

				db.session.add(comment)
				db.session.commit()

				flash(u'댓글을 작성하였습니다.', 'success')
			return redirect(url_for('faq_detail', id=faq_id))
		return render_template('fcomment/create.html', form=form)
