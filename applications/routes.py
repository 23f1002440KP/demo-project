from flask import current_app as app, jsonify, render_template_string, request
from flask_security import auth_required, verify_password, hash_password, roles_required
from applications.models import db

datastore = app.security.datastore


@app.route("/")
def home():
    return render_template_string(
        """
        <h1>Homepage</h1>
        """
    )


@app.get("/protected")
@auth_required("token")
def protected():
    return jsonify({"msg": "Hello"})


@app.route("/login", methods=["GET", "POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "invalid inputs"}), 404

    user = datastore.find_user(email=email)

    if not user:
        return jsonify({"message": "invalid email"}), 404

    if verify_password(password, user.password):
        return jsonify(
            {
                "token": user.get_auth_token(),
                "email": user.email,
                "role": user.roles[0].name,
                "id": user.id,
            }
        )

    return jsonify({"message": "password wrong"}), 400


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not email or not password or role not in ["stud", "inst"]:
        return jsonify({"msg": "Invalid Input"})
    user = datastore.find_user(email=email)

    if user:
        return jsonify({"msg": "User already exist"})
    try:
        datastore.create_user(
            email=email, password=hash_password(password), roles=[role], active=1
        )
        db.session.commit()
        return jsonify({"msg": "User Created"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "error Creating User", "error": str(e)}), 400
