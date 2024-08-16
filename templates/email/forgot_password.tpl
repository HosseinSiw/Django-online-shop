{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello and welcome dear {{ user.username }}
{% endblock %}

{% block html %}
<h6>You can change your password via this url https://127.0.0.1:8000/users/api/v1/reset-password/{{token}}/</h6>
{% endblock %}