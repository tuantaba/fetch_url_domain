#!/opt/api-sla-sites/sla/bin/python

from flask import Flask, jsonify, request, session, render_template
from flask_httpauth import HTTPBasicAuth

import json
from datetime import datetime

from flaskext.mysql import MySQL #pip install flask-mysql
import pymysql

APP = Flask(__name__)
#APP.config['SECRET_KEY']='hellovccorpbizfly'
#auth = HTTPDigestAuth()
auth = HTTPBasicAuth()

users = {
        "xxxxxx": "xxxxxxxxxxxxxxxx"
        }

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


mysql = MySQL()

 # MySQL configurations
mysql.init_app(APP)


APP.route("/", methods=["GET"])
@auth.login_required
def index():
    return jsonify({
        "hello": "Welcome to SLA Sites on DC, try GET: /api/ for more information"
    })


@APP.route("/sla/api", methods=["GET"])
@auth.login_required
def get_subdomain():
    conn = None
    cursor = None
    if request.method == 'GET':
        domain = request.args.get('domain');
        print domain;
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute('''SELECT  * FROM domain  WHERE domain=%s ORDER BY iddomain DESC LIMIT 1''', (domain) )
            rows = cursor.fetchall()
            resp = jsonify(rows)
            resp.status_code = 200
            return resp
        except Exception as e:
            print (e)
        finally:
            cursor.close()
            conn.close()


@APP.route("/sla/api/domain", methods=["GET"])
@auth.login_required
def get_all_domain():
    conn = None
    cursor = None
    if request.method == 'GET':
        try:

            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute('''select distinct(domain)  from domain''')
            rows = cursor.fetchall()
            domain_array = []
            for row in rows:
            #    print row['domain']
                domain_array.append(row['domain'])
            resp = jsonify(domain_array)
            resp.status_code = 200
            return resp
        except Exception as e:
            print (e)
        finally:
            cursor.close()
            conn.close()



@APP.route("/sla/api/alert/manager", methods=["GET"])
@auth.login_required
def alert_api_manager():
    conn = None
    cursor = None
    if request.method == 'GET':
        _manager = request.args.get('manager')
        print _manager
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute('''select  * from  sla_manager where manager=%s''', (_manager) )
            rows = cursor.fetchall()
            resp = jsonify(rows)
            resp.status_code = 200
            return resp
        except Exception as e:
            print (e)
        finally:
            cursor.close()
            conn.close()


@APP.route("/sla/api/alert", methods=["PUT", "GET", "POST"])
@auth.login_required
def alert_api():
    conn = None
    cursor = None
    if request.method == 'PUT':
        try:
            print type(request)
            _json = request.json
            print type(_json)
            _domain=_json['domain']
            _alert_type=_json['alert_type']
            _alert_time=_json['alert_time']
            print _domain
            print _alert_type
            print _alert_time
            conn = mysql.connect()
            if _domain:
                sql = '''UPDATE sla_domain SET alert_time=%s WHERE domain=%s AND alert_type=%s'''
                data = (_alert_time, _domain, _alert_type)
            else:
                print "no input argumentss"
                return "Error: No Input argument"
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Updated Stats successfully')
            resp.status_code = 200
            cursor.close()
            conn.close()
            return resp
        except Exception as e:
            print (e)

    if request.method == 'GET':
        _domain = request.args.get('domain')
        _alert_type = request.args.get('alert_type')
        print _domain
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute('''select  * from  sla_domain where domain=%s and alert_type=%s''', (_domain, _alert_type) )
            rows = cursor.fetchall()
            resp = jsonify(rows)
            resp.status_code = 200
            return resp
        except Exception as e:
            print (e)
        finally:
            cursor.close()
            conn.close()

    if request.method == 'POST':
        try:
            print type(request)
            _json = request.json
            print type(_json)
            _domain=_json['domain']
            _alert_type=_json['alert_type']
            _threshold=_json['threshold']
            _count=_json['count']
            print _domain
            print _alert_type
            conn = mysql.connect()
            if _domain:
                sql = '''INSERT INTO sla_domain(domain,alert_type,threshold,count) VALUES (%s, %s, %s, %s)'''
                data = (_domain, _alert_type, _threshold, _count)
            else:
                print "no input argumentss"
                return "Error: No Input argument"
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Updated Stats successfully')
            resp.status_code = 200
            cursor.close()
            conn.close()
            return resp
        except Exception as e:
            print (e)


@APP.errorhandler(500)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
            }
    resp =  jsonify(message)
    resp.status_code =  404
    return resp

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=8081, debug=True)



