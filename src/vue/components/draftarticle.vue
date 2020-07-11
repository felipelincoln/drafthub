<template>
  <article :aria-label="title" tabindex="0" :class="cls.article">
    <figure :class="cls.figure">
      <draftimage :href="href" :src="src" :cls="cls.img" :alt="alt" />
      <draftimage :href="href" :src="src" :cls="cls.imgMobile" :alt="alt" />
    </figure>
    <div :class="cls.content">
      <h2 :class="cls.h2">
        <a :href="href"><strong>{{ title }}</strong></a>
        <b-tooltip v-if="type == 'large'" label="Most popular today"
          type="is-dark"
          position="is-bottom">
          <i class="fas fa-chart-line"></i>
        </b-tooltip>
      </h2>
      <p v-if="type == 'large'" class="has-text-grey"><small>{{ description }}</small></p>
      <p><small>
        <a rel="author" :href="blog">
          <address class="is-inline">{{ author }},</address>
        </a>
        <a :href="href">
          <time v-html="pubdate" :datetime="pubdateDatetime"></time>
          <time v-if="updated" v-html="updatedStr" :datetime="updatedDatetime"></time>
        </a>
      </small></p>
    </div>
  </article>
</template>

<script>
import draftimage from './draftimage.vue';

export default {
  components: {
    'draftimage': draftimage,
  },
  props: [
    'title',
    'description',
    'type',
    'href',
    'src',
    'blog',
    'author',
    'pubdate',
    'updated',
    'pubdateDatetime',
    'updatedDatetime',
  ],
  computed: {
    alt: function(){
      return `Cover image for: ${this.title}`
    },
    updatedStr: function(){
      return `(updated ${this.updated})`
    },
    cls: function(){
      return {
        article: {
          'media': this.type != 'large',
        },
        figure: {
          'media-left': this.type != 'large',
          'image': this.type == 'large',
          'is-3by1': this.type == 'large',
          'mr-2': this.type == 'small',
        },
        content: {
          'media-content': this.type != 'large',
        },
        img: {
          'a-img-default': !this.type,
          'a-img-small': this.type == 'small',
          'a-img-large': this.type == 'large',
          'has-ratio': this.type == 'large',
          'is-hidden-mobile': this.type != 'large',
        },
        imgMobile: {
          'is-hidden-tablet': this.type != 'large',
          'is-hidden': this.type == 'large',
        },
        h2: {
          'is-capitalized': true,
          'is-size-5': this.type == 'large',
          'mt-2': this.type == 'large',
        },
      }
    },
  },
}
</script>

<style scoped>
.a-img-large {
  width: 100%;
}
.a-img-small {
  width: 48px;
  height: 48px;
}
.a-img-default {
  width: 128px;
  height: 100%;
  min-height: 72px;
}
.is-hidden-tablet {
  width: 64px;
  height: 64px;
}
.media-content {
  min-width:20%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
article {
  align-items: stretch;
}
h2 {
  word-wrap:break-word;
}
</style>
