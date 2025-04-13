---
layout: default
title: 최호준의 블로그
---

# 👋 안녕하세요!

이 페이지는 제가 공부하며 기록한 내용을 담은 공간입니다.  
실패한 실험, 좋은 인사이트, 아이디어를 담아두려고 합니다.

---

## 📚 최근 글

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a> <small>{{ post.date | date: "%Y-%m-%d" }}</small>
    </li>
  {% endfor %}
</ul>
