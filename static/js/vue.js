// vue.js
Vue.component('dh-search', {
  props: [
    'value',
    'action',
    'placeholder',
  ],
  template: `
    <form
      :action="action"
      method="get">
      <b-input
        :value="value"
        name="q"
        :placeholder="placeholder"
        type="search"
        aria-label="Search">
      </b-input>
    </form>
  `
});

Vue.component('dh-heading', {
  props: [
    'id',
  ],
  template:`
    <h1
      :id="id"
      style="text-transform:uppercase"
      class="pb-5">
      <strong><slot></slot></strong>
    </h1>
  `
});

Vue.component('dh-article', {
  delimiters: ['[[', ']]'],
  data: function(){
    return {
      isLoading: true,
    }
  },
  props: [
    'title',
    'href',
    'blog',
    'author',
    'created',
    'updated',
    'datetime',
    'src',
    'tiny',
    'latest',
  ],
  template: `
    <article :aria-label="title" tabindex="0" class="media">
      <figure v-if="tiny" class="media-left mr-2" :aria-label="alt">
        <p class="image is-48x48">
          <a :href="href">
            <img
              style="max-height:48px;"
              :src="src"
              @load="isLoading=false"
              @error="isLoading=false"
              :alt="alt">
          </a>
          <b-skeleton height="48px" :active="isLoading"></b-skeleton>
        </p>
      </figure>
      <figure v-else class="media-left" :aria-label="alt">
        <p class="image is-128x128 is-hidden-mobile">
          <a :href="href">
            <img
              style="max-height:128px;"
              :src="src"
              @load="isLoading=false"
              @error="isLoading=false"
              :alt="alt">
          </a>
          <b-skeleton height="85px" :active="isLoading"></b-skeleton>
        </p>
        <p class="image is-64x64 is-hidden-tablet">
          <a :href="href">
            <img
              style="max-height:64px;"
              :src="src"
              @load="isLoading=false"
              @error="isLoading=false"
              :alt="alt">
          </a>
          <b-skeleton height="64px" :active="isLoading"></b-skeleton>
        </p>
      </figure>
      <div class="media-content" style="min-width:20%">
        <p><small>
          <a rel="author" :href="blog">
            <address class="is-inline">
              [[ author ]],
            </address>
          </a>
          <a v-if="!latest" :href="href">
            <time pubdate :datetime="datetime">
              [[ created ]]
            </time>
            <span v-if="updated">
              (updated <time v-html="updated">[[ updated ]]</time> ago)
            </span>
          </a>
          <a v-if="latest" :href="href">
            <time v-html="latest">[[ latest ]]</time> ago
          </a>
        </small></p>
        <h2 style="word-wrap: break-word;text-transform: capitalize;">
          <a :href="href"><strong>
            [[ title ]]
          </strong></a>
        </h2>
        <p v-if="!tiny"><small><slot></slot></small></p>
      </div>
    </article>
  `,
  computed: {
    alt: function(){
      return `Cover image for: ${this.title}`
    }
  }
});


let dbTags = [];
//fetch('http://127.0.0.1:8000/api/tags')
fetch('https://drafthub-development.herokuapp.com/api/tags')
  .then(res => res.json())
  .then(data => dbTags = data.tags)


new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data:{
    tags: [],
    filteredTags: dbTags,
  },
  methods: {
    getFilteredTags(text){
      this.filteredTags = dbTags.filter((item) => {
        return item.indexOf(text.toLowerCase()) >= 0
      })
    },
    getTagsInputValue(){
      return this.tags.join(', ')
    },
  },
})
