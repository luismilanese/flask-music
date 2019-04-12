from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from sqlalchemy.sql.functions import user
from flask import jsonify
from app import app, login_manager
from app.forms.album_form import AlbumForm
from app.forms.login_form import LoginForm
from app.models.user import User
from app.repositories import album_repository
from app.repositories.artist_repository import get_all_artists
from app.services.import_from_gspread import Importer


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("Auth?", "error")
        return redirect(url_for("add_album"))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Incorrect user/password", "error")
            return redirect(url_for("login"))

        if not user.validate_password(password):
            flash("Incorrect user/password", "error")
            return redirect(url_for("login"))

        login_user(user)

        next_page = request.args.get('next')

        if not next_page:
            redirect(url_for('index'))

        return redirect(url_for("add_album"))
    return render_template("auth/login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/")
def index():
    return render_template("albums/index.html")


@app.route("/add-new", methods=["GET", "POST"])
@login_required
def add_album():
    form = AlbumForm()
    form.artists.choices = get_all_artists()

    if form.validate_on_submit():
        try:
            album_repository.insert_album(form)
            return redirect(url_for("listing"))
        except Exception as e:
            print(str(e))

    return render_template("albums/form.html", form=form)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_album(id):
    album = album_repository.get_by_id(id)
    form = AlbumForm(obj=album)
    form.artists.choices = get_all_artists()

    if form.validate_on_submit():
        try:
            album_repository.update_album(id, form)
            return redirect(url_for("listing"))
        except Exception as e:
            print(str(e))

    form.artists.data = [artist.id for artist in album.artists]

    return render_template("albums/form.html", form=form)


@app.route("/delete/<int:id>", methods=["GET"])
@login_required
def delete_album(id):
    album = album_repository.get_by_id(id)

    try:
        album_repository.delete_album(album)
        return redirect(url_for("listing"))
    except Exception as e:
        print(str(e))


@app.route("/all")
def listing():
    albums = album_repository.list_albums()

    return render_template("albums/list.html", albums=albums)


@app.route("/import-from-spreadsheet")
@login_required
def import_from_gspread():
    try:
        result = Importer().importer()

    except Exception as e:
        print(str(e))


