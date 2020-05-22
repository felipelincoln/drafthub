# drafthub

[![build](https://img.shields.io/github/workflow/status/drafthub/drafthub/CI)](https://github.com/drafthub/drafthub/actions)
[![docs](https://readthedocs.org/projects/drafthub/badge/?version=latest)](https://drafthub.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/drafthub/drafthub/branch/master/graph/badge.svg)](https://codecov.io/gh/drafthub/drafthub/branch/new)
[![tech](http://img.shields.io/badge/tech-stack-0690fa.svg?style=flat)](https://stackshare.io/felipelincoln/my-stack)

Working intensively on this :nerd_face:


This is an open source blogging website which uses GitHub to serve the posts

## Development
In order to get this website up and running in your localhost it is enough to have docker installed and run
`docker-compose up --build` on your local clone of this repository.

### Technologies
[<img src="https://static.djangoproject.com/img/logos/django-logo-negative.png" height="70">](https://www.djangoproject.com/)
[<img src="https://getbootstrap.com/docs/4.5/assets/brand/bootstrap-solid.svg" height="70">](https://getbootstrap.com/)
[<img src="https://www.docker.com/sites/default/files/d8/styles/role_icon/public/2019-07/vertical-logo-monochromatic.png?itok=erja9lKc" height="70">](https://www.docker.com/)
[<img src="https://www.postgresql.org/media/img/about/press/elephant.png" height="70">](https://www.postgresql.org/)
[<img src="https://brand.heroku.com/static/media/heroku-logotype-vertical.f7e1193f.svg" height="70">](https://dashboard.heroku.com/)
\*No javascript front-end framework.

### Environment variables
The only difference with this repository to the production files are the environment variables. In the production domain
https://drafthub.herokuapp.com the environment variables are set inside Heroku platform, meanwhile in the development domain
these variables are located at the `docker-compose.yml` file.
```yml
environment:
  - ENVIRONMENT=development
  - SECRET_KEY=&d3b2mg6&=twp3q*!n9f!1#(zp($$j34m5ds=e7v2@+t7m&3z4o
  - ADMIN_URL=admin/
  - SOCIAL_AUTH_GITHUB_KEY=7d8639e8eff3fd36d459
  - SOCIAL_AUTH_GITHUB_SECRET=168227076fdb096fe92ec8de97180168169874f7
  ```

## Production
This is a beta release, database may not be kept in the future.

### Why this website matters
Draft noun:  
> A piece of writing or drawing that is done early in the development of a work to help prepare it in its final form  
> \- *dictionary.cambridge.org*

- It eases the pain of writing the perfect article by your own, your publication will receive contribution from the GitHub
community and with time will get as good as it can possibly be;
- Articles writters will got the whole markdown facilities;
- Every article you post are safe as long as GitHub exists;
- The problem of reading an article with some typos and wrong codes won't appear as frequent as it is nowadays;
- Altough [GitHub Flavored Markdown](https://github.github.com/gfm/) does not support math equations, DraftHub will render
every inline equation wrapped by single dollars signs `$ ... $` and block equations
- You get a blog


### How it works
You first push a markdown file to one of your public repository in GitHub, then you log into DraftHub using your GitHub
account, and then put the markdown url in the new draft form. Now you exposed your work to DraftHub readers, can interact
with them in the comment section and may get contribution to enhance your publication quality.


## Final words
As well as its articles this website is also a draft, started by myself, [felipelincoln](https://github.com/felipelincoln).  
DraftHub was made for the open source community and it is meant to be
also maintained by the open source community.
