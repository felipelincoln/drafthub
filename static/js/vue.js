// vue.js
Vue.component('dh-article', {
  delimiters: ['[[', ']]'],
  props: [
    'title',
    'author',
    'created',
    'updated'
  ],
  template: `
    <article>
      <header>
        <h2 class="dh-title">
          <strong>[[ title ]]</strong>
        </h2>
        <div class="dh-taglist"><slot></slot></div>
      </header>
      <footer class="is-size-7">
        <address class="dh-author">
          [[ author ]]
        </address>
        <time pubdate>
          [[ created ]]
        </time>
        <time v-if="updated != 'None'">
          [[ updated ]]
        </time>
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
