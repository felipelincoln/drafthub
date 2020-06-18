// vue.js
Vue.component('dh-article', {
  delimiters: ['[[', ']]'],
  props: [
    'title',
    'href',
    'blog',
    'author',
    'created',
    'updated',
    'hits',
    'src',
    'tiny'
  ],
  template: `
    <article class="media">
      <figure v-if="tiny" class="media-left">
        <p class="image is-48x48" style="height:auto;">
          <img style="border-radius:2px;max-height:48px;" :src="src">
        </p>
      </figure>
      <figure v-else class="media-left">
        <p class="image is-128x128 is-hidden-mobile" style="height:auto;">
          <img style="border-radius:6px;max-height:128px;" :src="src">
        </p>
        <p class="image is-64x64 is-hidden-tablet" style="height:auto;">
          <img style="border-radius:6px;max-height:64px;" :src="src">
        </p>
      </figure>
      <section class="media-content">
        <div class="is-size-7" style="display:flex">
          <p style="flex-grow:1;">
            <a class="dh-a" :href="blog">
            <address style="font-style: normal;" class="is-inline">
              [[ author ]],
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
          </p>
          <p v-if="!tiny" class="is-size-7"><a :href="href" class="dh-a">[[ hits ]] views</a></p>
        </div>
        <h2>
          <a class="dh-a" :href="href">
            <span class="has-text-weight-medium has-text-dark">[[ title ]]</span>
          </a>
        </h2>
        <p v-if="!tiny"><slot></slot></p>
      </section>
    </article>
  `
});

Vue.component('dh-tag', {
  props: [
    'href',
  ],
    template: `
      <a
        class="dh-a is-size-7"
        :href="href">
        #<slot></slot>
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
