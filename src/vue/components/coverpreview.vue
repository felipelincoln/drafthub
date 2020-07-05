<template>
  <figure class="image mb-3">
    <b-skeleton
      v-if="imgPlaceholder"
      height="200px"
      :animated="imgLoading">
    </b-skeleton>
    <img
      v-show="!imgPlaceholder"
      :src="src"
      :alt="alt"
      @load="imgPlaceholder=false"
      @error="imgNotLoaded()">
  </figure>
</template>

<script>
export default {
  props: [
    'src',
    'alt',
  ],
  data: function(){
    return {
      imgLoading: false,
      imgPlaceholder: true,
    }
  },
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
}
</script>
