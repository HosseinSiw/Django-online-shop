{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello and welcome dear {{ user.username }}
{% endblock %}

{% block html %}
<h1>Hello dear {{ user.username }}</h1><br>
<h6>You can change your password via this url <br></h6>
<a href='{{ url }}'> reset. </a>
{% endblock %}