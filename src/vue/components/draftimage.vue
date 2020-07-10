<template>
  <a :href="href" :class="cls" :style="stl" :aria-label="alt">
    <b-skeleton :active="loading"></b-skeleton>
  </a>
</template>

<script>
export default {
  data: function(){
    return {
      loading: true,
    }
  },
  props: [
    'href',
    'alt',
    'src',
    'cls',
    'stl',
  ],
  mounted: function(){
    var img = new Image();
    img.onload = () => {
      this.$el.style.backgroundImage = `url(${img.src})`;
      this.loading = false;
    },
    img.onerror = (() => this.loading = false);
    img.src = this.src;
  },
}
</script>
<style scoped>
a {
  display: block;
  background-size: cover;
  background-position: center center;
  border-radius: 2px;
}
a:hover {
  text-decoration: none;
}
.b-skeleton,
.b-skeleton-item {
  height: 100%;
}
</style>
