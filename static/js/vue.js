// vue.js
Vue.component('dh-tag', {
  props: [
    'href',
    'pack',
    'icon',
  ],
    template: `
      <b-button
        style="font-family:monospace;"
        size="is-small"
        type="is-dark"
        tag="a"
        :href="href"
        :icon-pack="pack"
        :icon-left="icon">
        <slot></slot>
      </b-button>
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
