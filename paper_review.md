---
layout: default
title: "📄 Paper Reviews"
permalink: /paper_review/
---

<h1>📄 Paper Reviews</h1>

<ul>
  {% for post in site.posts %}
    {% if post.categories contains "paper_review" %}
      <li>
        <a href="{{ post.url }}">{{ post.title }}</a> <small>({{ post.date | date: "%Y-%m-%d" }})</small>
      </li>
    {% endif %}
  {% endfor %}
</ul>
