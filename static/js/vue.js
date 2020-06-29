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
              v-show="!isLoading"
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
              v-show="!isLoading"
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
              v-show="!isLoading"
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


Vue.component('articlecover', {
  props: {
    'src': '',
  },
  data: function(){
    return {
      imgLoading: false,
      imgPlaceholder: true,
    }
  },
  template: `
    <figure class="image">
      <b-skeleton
        v-if="imgPlaceholder"
        height="300px"
        :animated="imgLoading">
      </b-skeleton>
      <img
        v-show="!imgPlaceholder"
        :src="src"
        @load="imgPlaceholder=false"
        @error="imgNotLoaded()">
    </figure>
  `,
  methods: {
    imgNotLoaded: function(){
      console.log('img not loaded@');
      this.imgLoading = false;
      this.imgPlaceholder = true;
    },
  },
  watch: {
    src: function(){
      console.log('image changed');
      this.imgLoading = true;
      this.imgPlaceholder = true;
    },
  },
});



Vue.component('preview', {
  delimiters: ['[[', ']]'],
  props: {
    url: '',
  },
  data: function(){
    return {
      mdLoading: false,
      mdPlaceholder: true,
      mdPreview: '',
    }
  },
  template: `
    <div v-if="mdPlaceholder">
      <b-skeleton
        width="80%"
        height="40px"
        :animated="mdLoading">
      </b-skeleton>
      <b-skeleton
        width="100%"
        :count="2"
        :animated="mdLoading">
      </b-skeleton>
      <br>
      <b-skeleton
        width="100%"
        :count="3"
        :animated="mdLoading">
      </b-skeleton>
    </div>
    <div v-else class="markdown-body" v-html="mdPreview">
      [[ mdPreview ]]
    </div>
  `,
  watch: {
    url: function(){
      console.log('url changed');
      this.mdLoading = true;
      this.mdPlaceholder = true;
      fetch(`/api/markdown/?url=${this.url}`)
        .then(res => res.json())
        .then((data) => {
            this.mdLoading = false;
            if(data.markdown != "Data could not be retrieved."){
              this.mdPlaceholder = false;
              this.mdPreview = data.markdown;
              console.log('updating', this.$el);
              this.$nextTick(() => window.renderMathInElement(this.$el));
            }
        })
    },
  },
});

Vue.component('inputtags', {
  props: [
    'api',
    'value',
    'name',
  ],
  data: function(){
    return {
      filteredTags: [],
    }
  },
  template: `
    <div>
      <b-taginput
        ref="taginput"
        :value="value"
        :data="filteredTags"
        autocomplete
        :allow-new="true"
        maxlength="25"
        maxtags="5"
        icon="label"
        placeholder="Add a tag"
        :confirm-key-codes="[13, 188, 9]"
        @input="$emit('input', $event)"
        @remove="showDeletedTag"
        @typing="getFilteredTags">
      </b-taginput>
    <input type="hidden" :name="name" :value="getTagsInputValue">
    </div>
  `,
  methods: {
    getFilteredTags: function(text){
      this.filteredTags = this.api.filter((item) => {
        return item.indexOf(text.toLowerCase()) >= 0
      })
    },
    showDeletedTag: function(){
      let deletedTag = this.value.filter(x => !vm.newArticle.tags.includes(x));
      let lastTag = this.value.slice(-1)[0];
      if(deletedTag == lastTag){
        this.$refs.taginput.newTag = lastTag;
      }
    },
  },
  computed: {
    getTagsInputValue: function(){
      return this.value.join(', ')
    },
  },
});



vm = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    newArticle: {
      apiTags: [],
      tags: [],
      url: '',
      image: '',
      title: '',
      description: '',
      formError: {
        tags: true,
        url: true,
        image: true,
        title: true,
        description: true,
      }
    },
  },
})
