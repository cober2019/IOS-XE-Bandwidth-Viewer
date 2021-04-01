# -*- encoding: utf-8 -*-

from flask import jsonify, render_template, redirect, url_for, flash, request, send_file, Response
from werkzeug.utils import secure_filename
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, NewAccountForm
from app.base.models import User
from app.base.util import verify_pass
import app.Modules.connection as ConnectWith
import app.Modules.BandwidthTool as GetBandwidth
import app.Modules.Snmp as GetSnmp
import app.Modules.Gets as GetDetails


device = None
username = None
password = None
netconf_port = None
ssh_port = None
snmp_comm = None
netconf_session = None
netmiko_session = None
bandwidth_object = {}
bandwidth_interface = None
success_login_form = None

@blueprint.route('/', methods=['POST', 'GET'])
def login():

    global success_login_form, username, password, netconf_port, ssh_port, device, netconf_session, netmiko_session, snmp_comm

    if request.form:

        # Set variable from form data. Set defaults if not entered in the login form
        if not request.form['netconfPort']:
            netconf_port = 830
        else:
            netconf_port = request.form['netconfPort']

        if not request.form['sshPort']:
            ssh_port = 22
        else:
            ssh_port = request.form['sshPort']

        if not request.form['snmpComm']:
            snmp_comm = 'public'
        else:
            snmp_comm = request.form['snmpComm']

        username = request.form['username']
        password = request.form['password']
        device = request.form['ipAddress']

        # Create NETCONF and netmiko session objects
        netconf_session = ConnectWith.create_netconf_connection(request.form['username'], request.form['password'],
                                                                request.form['ipAddress'], netconf_port)
        netmiko_session = ConnectWith.creat_netmiko_connection(request.form['username'], request.form['password'],
                                                                request.form['ipAddress'], ssh_port)


        if netmiko_session == 'Connection Issue':
            return render_template('device_login.html', status="Login Failed")
        if netconf_session == 'Connection Issue':
            return render_template('device_login.html', status="Login Failed")
        else:
            success_login_form = 1
            return redirect(url_for('base_blueprint.index'))
    else:
        return render_template('device_login.html', status=None)

@blueprint.route('/index')
def index():
    """This page displays device interface"""

    if success_login_form is None:
        return redirect(url_for('base_blueprint.login'))
    else:
        # If login successful assign template variables
        return render_template('index.html', interfaces=GetDetails.indivisual_poll(device, username, password, netconf_port),
                               device=device)

@blueprint.route('/int_details', methods=['POST', 'GET'])
def interface_details():
    """Get interface details, CLI view"""

    if success_login_form is None:
        return redirect(url_for('base_blueprint.login'))
    else:
        return render_template('more_int_detials.html',
                               details=GetDetails.more_int_details(device, username, password, ssh_port, request.form.get('details')))


@blueprint.route('/interface_stats', methods=['POST', 'GET'])
def interface_stats():
    """Gets IOS-XE routing table"""

    global bandwidth_object, bandwidth_interface

    if not request.form.get('openPage'):

        if request.form.get('action') == 'cpu':
            # If AJAX dictionary key has been assigned 'cpu' as its value then pool cpu utilization using snmp
            cpu_usage = GetSnmp.get_current_cpu(device, snmp_comm)
            return cpu_usage
        elif request.form.get('action') == 'bandwidth':

            # If AJAX data dictionary key has been assign 'in' to the key, poll inbound bandwidth usage, return to AJAX function
            if request.form.get('direction') == 'in':
                bandwidth_usage_in = bandwidth_object.get(request.form.get('interface')).get_interface_bandwith_in()
                return str(int(bandwidth_usage_in))
            # If AJAX data dictionary key has been assign 'out' to the key, poll outbound bandwidth usage, return to AJAX function
            elif request.form.get('direction') == 'out':
                bandwidth_usage_out = bandwidth_object.get(request.form.get('interface')).get_interface_bandwith_out()
                return str(int(bandwidth_usage_out))
        elif request.form.get('action') == 'discards':

            # If AJAX data dictionary key has been assign 'in' to the key, poll inbound discards, return to AJAX function
            if request.form.get('direction') == 'in':
                discards_in = bandwidth_object.get(request.form.get('interface')).get_interface_bandwith_in_discards()
                return str(int(discards_in))
            # If AJAX data dictionary key has been assign 'out' to the key, poll outbound discards, return to AJAX function
            elif request.form.get('direction') == 'out':
                discards_out = bandwidth_object.get(request.form.get('interface')).get_interface_bandwith_out_discards()
                return str(int(discards_out))

    # Assign global interface variable.
    if not bandwidth_object:
        bandwidth_object[request.form.get('openPage')] = GetBandwidth.CalcBandwidth(device, netconf_port, username,
                                                                                    password,
                                                                                    request.form.get('openPage'))
        bandwidth_interface = request.form.get('openPage')
        # Render template with the selected interface assigned. Inter fave is used in the onload javascipt script for AJAX function
        return render_template('interface_stats.html', interface=bandwidth_interface, device=device)
    elif request.form.get('openPage') is None:
        return render_template('interface_stats.html', interface=bandwidth_interface, device=device)
    else:
        # If key "interface" is in dictionary, create k/v pair with value being the bandwidth tool object
        if bandwidth_object.get(request.form.get('openPage')) is None:
            new_object = GetBandwidth.CalcBandwidth(device, netconf_port, username, password, request.form.get('openPage'))
            bandwidth_object[request.form.get('openPage')] = new_object

        bandwidth_interface = request.form.get('openPage')
        # Render template with the selected interface assigned. Inter fave is used in the onload javascipt script for AJAX function
        return render_template('interface_stats.html', interface=bandwidth_interface, device=device)


@blueprint.route('/logout')
def logout():
    """User logout and re-login"""

    logout_user()
    success_login_form = None
    bandwidth_object = None
    return redirect(url_for('base_blueprint.login'))



