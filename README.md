# drafthub
> Hosted blogging platform based on GitHub

[![build](https://img.shields.io/github/workflow/status/drafthub/drafthub/CI)](https://github.com/drafthub/drafthub/actions)
[![docs](https://readthedocs.org/projects/drafthub/badge/?version=latest)](https://drafthub.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/drafthub/drafthub/branch/master/graph/badge.svg)](https://codecov.io/gh/drafthub/drafthub/)
[![tech](http://img.shields.io/badge/tech-stack-0690fa.svg?style=flat)](https://stackshare.io/felipelincoln/my-stack)

Start your own developer blog using git and markdown and integrate the GitHub community :nerd_face:.

[![](https://i.ibb.co/McvBBRT/drafthub-1.png)](https://drafthub.herokuapp.com)

## Features
- It's free and totally open source :thinking:
- No registration needed, GitHub OAuth only :relieved:
- Write your posts in markdown :blush:
- Math equations supported :yum:
- Your content is always safe on GitHub :smiling_face_with_three_hearts:
- Get contribution from your readers :heart_eyes:

## Contribute
- [Write documentation](https://github.com/drafthub/drafthub/milestone/1) (easy :hugs:)
- [Enhance code quality](https://github.com/drafthub/drafthub/milestone/2) (easy :hugs:)
- [Code some tests](https://github.com/drafthub/drafthub/milestone/3)
- [Solve an issue in general](https://github.com/drafthub/drafthub/issues)

## The stack
[<img src="https://img.stackshare.io/service/1052/YMxUfyWf.png" height="80px"><img src="https://img.stackshare.io/service/993/pUBY5pVj.png" height="80px"><img src="https://img.stackshare.io/service/1101/C9QJ7V3X.png" height="80px">
<img src="https://img.stackshare.io/service/2538/kEpgHiC9.png" height="80px"><img src="https://img.stackshare.io/service/1028/ASOhU5xJ.png" height="80px"><img src="https://img.stackshare.io/service/994/4aGjtNQv.png" height="80px">
<img src="https://img.stackshare.io/service/133/3wgIDj3j.png" height="80px"><img src="https://img.stackshare.io/service/1147/markdown.png" height="80px"><img src="https://img.stackshare.io/service/1091/gunicorn.png" height="80px">
<img src="https://img.stackshare.io/service/1598/TtqoAo1V.png" height="80px"><img src="https://img.stackshare.io/service/384/OhsWgbsr.png" height="80px"><img src="https://img.stackshare.io/service/27/sBsvBbjY.png" height="80px">
<img src="https://img.stackshare.io/service/1046/git.png" height="80px"><img src="https://img.stackshare.io/service/586/n4u37v9t_400x400.png" height="80px"><img src="https://img.stackshare.io/service/3136/docker-compose.png" height="80px">
<img src="https://img.stackshare.io/service/2673/Codecov_Mark_Circle_Pink.png" height="80px"><img src="https://img.stackshare.io/service/4837/py.jpg" height="80px"><img src="https://img.stackshare.io/service/3244/1_Mr1Fy00XjPGNf1Kkp_hWtw_2x.png" height="80px"><img src="https://img.stackshare.io/service/109/-CvHThPk_400x400.jpg" height="80px">](https://stackshare.io/drafthub/drafthub)

# drafthub-development :rocket:
> The [development branch](https://github.com/drafthub/drafthub/tree/development) deploys into the [development version](https://drafthub-development.herokuapp.com) of the website.

[![build](https://img.shields.io/github/workflow/status/drafthub/drafthub/CI/development)](https://github.com/drafthub/drafthub/actions?query=branch%3Adevelopment++)
[![docs](https://readthedocs.org/projects/drafthub-development/badge/?version=latest)](https://drafthub-development.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/drafthub/drafthub/branch/development/graph/badge.svg)](https://codecov.io/gh/drafthub/drafthub/branch/development)
[![tech](http://img.shields.io/badge/tech-stack-0690fa.svg?style=flat)](https://stackshare.io/felipelincoln/drafthub-development)

## New features
- Bulma/Buefy user interface
  [<img title="Vue.js" src="https://miro.medium.com/max/2440/1*scPMiJ0EMOnQbWX2TiANvQ.gif" width="800px">](https://bulma.io/)
  
- SEO plus page titles and favicon
  ```html
  <title>drafthub: blog like a developer</title>
  <meta name="title" content="drafthub: blog like a developer">
  <meta name="description" content="Start your own developer blog using git and markdown and integrate the GitHub community">
  ```
- Vue components
  ```javascript
  Vue.component('draft-tag', {
	props: [
	  'tagUrl',
	  'tagPack',
	  'tagIcon',
	],
	  template: `
      <a :href="tagUrl">
        <b-tag type="is-dark" size="is-medium">
          <b-icon v-if="tagIcon != 'None'" :pack="tagPack" :icon="tagIcon" size="is-small"></b-icon>
          <span><slot></slot></span>
        </b-tag>
      </a>
      `
  })
  ```
- Buefy input tags to the *New Draft* form  
  [<img title="Vue.js" src="https://i.ibb.co/PZ9k1Fp/ezgif-com-gif-maker-3.gif" width="400px">](https://buefy.org/documentation/taginput/)
  
  
## New to the stack
[<img title="Vue.js" src="https://img.stackshare.io/service/3837/paeckCWC.png" height="80px"><img title="Buefy" src="https://img.stackshare.io/service/10410/26799900.png" height="80px"><img title="Bulma" src="https://img.stackshare.io/service/5204/bulma-logo.png" height="80px">](https://stackshare.io/felipelincoln/drafthub-development)
