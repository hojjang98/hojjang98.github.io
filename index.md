---
layout: default
title: Hojun Choi's Blog
---

# 👋 Hello there!

Welcome to my blog — a space where I document what I'm learning, experimenting with, and reflecting on as I grow in the field of data science.

This includes everything from failed experiments and hard-earned insights to spontaneous ideas and personal notes.

---

## 📚 Recent Posts

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a> <small>{{ post.date | date: "%Y-%m-%d" }}</small>
    </li>
  {% endfor %}
</ul>
