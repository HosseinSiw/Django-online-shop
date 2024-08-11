{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello and welcome dear {{ user.username }}
{% endblock %}

{% block html %}
<h6>You can activate your account via this url https://127.0.0.1/user/activate/{{token}}/ </h6>
{% endblock %}