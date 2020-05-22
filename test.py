# @app.route('/autenticate', methods = ['POST'])
# def autenticate():
#     data = request.get_json()
#     cut = hash_report.df_user.loc[hash_report.df_user['username'] == data['username']]
#     if hashlib.sha512(data['password'] + cut['salt']).hexdigest() == cut['password']:
#         access_token = jwt.encode({'some': hash_report.df_user['username']}, secret, algorithm='HS256')
#         return jsonify({"access_token": access_token})
#     else:
#         return "401 - Unauthorized"


    # salt = uuid.uuid4().hex
    # print(str(salt))
    # print(str(data['password']))
    # hash = hashlib.sha512()
    # hash.update(('%s%s' % (salt, data['password'])).encode('utf-8'))
    # password_hash = hash.hexdigest()