{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello and welcome dear {{ user.username }}
{% endblock %}

{% block html %}
<h6>You can change your password via this url {{ url }}</h6>
{% endblock %}