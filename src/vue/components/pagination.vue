<template>
  <nav class="pagination mt-5" :style="!hasNext? 'flex-direction: row': ''">
    <a rel="next" v-if="hasNext" :href="href+nextPage">
      <span>{{ nextText }}</span><b-icon icon="chevron-right"></b-icon>
    </a>
    <a rel="prev" v-if="hasPrev" :href="href+prevPage">
      <b-icon icon="chevron-left"></b-icon><span>{{ prevText }}</span>
    </a>
  </nav>
</template>

<script>
export default {
  props: {
    hasNext: {
      type: Boolean,
      default: true,
    },
    nextText: {
      type: String,
      default: 'More articles'
    },
    hasPrev: Boolean,
    prevText: String,
    href: String,
    page: Number,
  },
  computed: {
    nextPage: function(){
      if(this.page) return '&page='+ (this.page + 1)
      return ''
    },
    prevPage: function(){
      if(this.page) return '&page='+ (this.page - 1)
      return ''
    },
  },
}
</script>

<style scoped>
nav {
  flex-direction: row-reverse;
  justify-content: space-between;
}
span { 
  vertical-align: middle;
}
</style>
