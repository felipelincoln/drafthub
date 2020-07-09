<template>
  <article :aria-label="title" tabindex="0" :class="cls.article">
    <figure :class="cls.figure">
      <a :href="href" :class="cls.img" :aria-label="alt">
        <b-skeleton :active="isLoading"></b-skeleton>
      </a>
      <a :href="href" :class="cls.imgMobile" :aria-label="alt">
        <b-skeleton :active="isLoading"></b-skeleton>
      </a>
    </figure>
    <div class="media-content" style="min-width:20%">
      <h2 style="word-wrap: break-word;text-transform: capitalize;">
        <a :href="href"><strong>
          {{ title }}
        </strong></a>
      </h2>
      <p><small>
        <a rel="author" :href="blog">
          <address class="is-inline">
            {{ author }},
          </address>
        </a>
        <a v-if="!latest" :href="href">
          <time pubdate :datetime="datetime">
            {{ created }}
          </time>
          <span v-if="updated && !tiny">
            (updated <time v-html="updated">{{ updated }}</time> ago)
          </span>
        </a>
        <a v-if="latest" :href="href">
          <time v-html="latest">{{ latest }}</time> ago
        </a>
      </small></p>
    </div>
  </article>
</template>

<script>
export default {
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
    'type',
  ],
  computed: {
    alt: function(){
      return `Cover image for: ${this.title}`
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
        },
        img: {
          'a-img': true,
          'a-img-default': !this.type,
          'a-img-small': this.type == 'small',
          'a-img-large': this.type == 'large',
          'has-ratio': this.type == 'large',
          'is-hidden-mobile': this.type != 'large',
        },
        imgMobile: {
          'a-img': true,
          'is-hidden-tablet': this.type != 'large',
          'is-hidden': this.type == 'large',
        },
      }
    },
  },
  mounted: function(){
    var aImg = this.$el.querySelectorAll('.a-img');
    var bgImg = new Image();
    bgImg.onload = () => {
      aImg.forEach(el => el.style.backgroundImage = `url(${bgImg.src})`);
      this.isLoading = false;
    },
    bgImg.src = this.src;
  },
}
</script>

<style scoped>
.a-img {
  display: block;
  background-size: cover;
  background-position: center center;
  border-radius: 12px;
}
.a-img:hover {
  text-decoration: none;
}
.a-img-large {
  width: 100%;
}
.a-img-small {
  width: 48px;
  height: 48px;
}
.a-img-default {
  width: 128px;
  height: 85px;
}
.is-hidden-tablet {
  width: 64px;
  height: 64px;
}
.b-skeleton,
.b-skeleton-item {
  height: 100%;
}
</style>
