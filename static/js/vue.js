// vue.js
Vue.component('dh-article', {
  delimiters: ['[[', ']]'],
  props: [
    'title',
    'href',
    'blog',
    'author',
    'created',
    'updated'
  ],
  template: `
    <article>
      <header>
        <h2 class="is-inline">
          <a class="dh-a" :href="href">
            <span class="has-text-weight-medium has-text-dark">[[ title ]]</span>
          </a>
        </h2>
        <div class="is-inline"><slot></slot></div>
      </header>
      <footer class="is-size-7">
        <a class="dh-a" :href="blog">
        <address style="font-style: normal;" class="is-inline">
          [[ author ]]
        </address>
        </a>
        <a class="dh-a" :href="href">
        <time pubdate>
          [[ created ]]
        </time>
        <time v-if="updated != 'None'">
          [[ updated ]]
        </time>
        </a>
      </footer>
    </article>
  `
});

Vue.component('dh-tag', {
  props: [
    'href',
  ],
    template: `
      <a
        class="tag is-family-monospace is-small is-secondary is-light"
        :href="href">
        <slot></slot>
      </a>
    `
})


const dbTags = ['python', 'albion-pvp', 'django']


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
  }
})
