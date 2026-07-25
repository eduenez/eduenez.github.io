---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}
{% assign cv = site.data.cv %}

**PDF versions:** [Concise resume]({{ base_path }}/files/cv.pdf) &middot; [Full academic vita]({{ base_path }}/files/cv-full.pdf)

Education
======
<ul>
{% for e in cv.education %}
  <li><strong>{{ e.degree }}</strong>, {{ e.institution }}, {{ e.start_year }}{% if e.end_year and e.end_year != e.start_year %}–{{ e.end_year }}{% endif %}{% if e.details %}. {{ e.details | markdownify | remove: "<p>" | remove: "</p>" }}{% endif %}</li>
{% endfor %}
</ul>

Professional Employment
======
<ul>
{% for e in cv.employment %}
  <li><strong>{{ e.role }}</strong>, {{ e.institution }}, {{ e.start_year }}{% if e.end_year %}{% if e.end_year != e.start_year %}–{{ e.end_year }}{% endif %}{% else %} – Present{% endif %}{% if e.details %}. {{ e.details | markdownify | remove: "<p>" | remove: "</p>" }}{% endif %}</li>
{% endfor %}
</ul>

Research Awards & Grants
======
<ul>
{% for a in cv.awards_grants %}
  <li><strong>{{ a.title }}</strong>{% if a.start_year %} ({{ a.start_year }}{% if a.end_year and a.end_year != a.start_year %}–{{ a.end_year }}{% endif %}){% endif %}{% if a.details %}. {{ a.details | markdownify | remove: "<p>" | remove: "</p>" }}{% endif %}</li>
{% endfor %}
</ul>

Research Interests
======
{{ cv.research_interests.summary | markdownify }}
<ul>
{% for a in cv.research_interests.applications %}
  <li>{{ a }}</li>
{% endfor %}
</ul>

Publications
======
{% for category in site.publication_category %}
  {% assign has_items = false %}
  {% for post in site.publications reversed %}
    {% if post.category == category[0] %}{% assign has_items = true %}{% endif %}
  {% endfor %}
  {% if has_items %}
  <h3>{{ category[1].title }}</h3>
  <ul>
  {% for post in site.publications reversed %}
    {% if post.category == category[0] %}
      {% include archive-single-cv.html %}
    {% endif %}
  {% endfor %}
  </ul>
  {% endif %}
{% endfor %}

Talks
======
<ul>{% for post in site.talks reversed %}
  {% include archive-single-talk-cv.html %}
{% endfor %}</ul>

Teaching
======
<ul>{% for post in site.teaching reversed %}
  {% include archive-single-cv.html %}
{% endfor %}</ul>

Mentorship
======
**Master's Theses**
<ul>
{% for t in cv.mentorship.masters_theses %}
  <li>{{ t.student }}, {{ t.institution }} ({{ t.year }}). {{ t.title }}</li>
{% endfor %}
</ul>

**Undergraduate Theses**
<ul>
{% for t in cv.mentorship.undergraduate_theses %}
  <li>{{ t.student }}, {{ t.institution }} ({{ t.year }}). {{ t.title }}</li>
{% endfor %}
</ul>

**Academic Synergy**
<ul>
{% for s in cv.mentorship.academic_synergy %}
  <li>{{ s.role }}{% if s.start_year %} (since {{ s.start_year }}){% endif %}{% if s.details %}. {{ s.details | markdownify | remove: "<p>" | remove: "</p>" }}{% endif %}</li>
{% endfor %}
</ul>

Professional / Editorial Service
======
<ul>
{% for s in cv.service %}
  <li>{{ s.role }}{% if s.institution %}, {{ s.institution }}{% endif %}{% if s.start_year %} ({{ s.start_year }}{% if s.end_year and s.end_year != s.start_year %}–{{ s.end_year }}{% endif %}){% endif %}{% if s.details %}. {{ s.details | markdownify | remove: "<p>" | remove: "</p>" }}{% endif %}</li>
{% endfor %}
</ul>

Professional Memberships
======
<ul>
{% for m in cv.memberships %}
  <li>{{ m }}</li>
{% endfor %}
</ul>
