// vue.js
Vue.component('dh-search', {
  props: [
    'action',
    'placeholder'
  ],
  template: `
    <form
      :action="action"
      method="get">
      <b-input
        name="q"
        :placeholder="placeholder"
        size="is-small"
        type="search"
        rounded>
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
      class="has-text-weight-bold has-text-grey-light pb-5 is-size-7">
      <slot></slot>
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
    'hits',
    'src',
    'tiny'
  ],
  template: `
    <article :aria-label="title" class="media">
      <figure v-if="tiny" class="media-left">
        <p class="image is-48x48">
          <a :href="href">
            <img
              style="border-radius:6px;max-height:48px;"
              :src="src"
              @load="isLoading=false">
          </a>
          <b-skeleton height="48px" :active="isLoading"></b-skeleton>
        </p>
      </figure>
      <figure v-else class="media-left">
        <p class="image is-128x128 is-hidden-mobile">
          <a :href="href">
            <img
              style="border-radius:6px;max-height:128px;"
              :src="src"
              @load="isLoading=false">
          </a>
          <b-skeleton height="85px" :active="isLoading"></b-skeleton>
        </p>
        <p class="image is-64x64 is-hidden-tablet">
          <a :href="href">
            <img
              style="border-radius:6px;max-height:64px;"
              :src="src"
              @load="isLoading=false">
          </a>
          <b-skeleton height="64px" :active="isLoading"></b-skeleton>
        </p>
      </figure>
      <section class="media-content">
        <div class="is-size-7 is-flex">
          <p style="flex-grow:1;">
            <a class="dh-a" :href="blog">
            <address class="is-inline">
              [[ author ]],
            </address>
            </a>
            <a class="dh-a" :href="href">
            <time v-if="!updated" pubdate>
              [[ created ]]
            </time>
            <time v-else pubdate>
              updated [[ updated ]]
            </time>
            </a>
          </p>
          <p v-if="!tiny">
            <a :href="href" class="dh-a">[[ hits ]] views</a>
          </p>
        </div>
        <h2 style="word-wrap: break-word;">
          <a class="dh-a has-text-weight-medium has-text-dark" :href="href">
            [[ title ]]
          </a>
        </h2>
        <p v-if="!tiny"><slot></slot></p>
      </section>
    </article>
  `,
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
});


const dbTags = ['python', 'albion-pvp', 'django'];


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
