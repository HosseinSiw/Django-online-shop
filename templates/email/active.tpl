{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello and welcome dear {{ user.username }}
{% endblock %}

{% block html %}
<h6>You can activate your account via this url http://127.0.0.1:7000/users/api/v1/register/activation/{{token}} </h6>
{% endblock %}
