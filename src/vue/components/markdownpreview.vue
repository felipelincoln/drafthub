<template>
  <div v-if="mdPlaceholder">
    <b-skeleton width="40%" :animated="mdLoading"> </b-skeleton>
    <b-skeleton width="50%" :animated="mdLoading"> </b-skeleton>
    <br>
    <b-skeleton height="250px" :animated="mdLoading"> </b-skeleton>
    <br>
    <b-skeleton width="100%" :animated="mdLoading"> </b-skeleton>
    <b-skeleton width="80%" :animated="mdLoading"> </b-skeleton>
    <br>
    <b-skeleton width="100%" :count="2" :animated="mdLoading"> </b-skeleton>
    <b-skeleton width="30%" :animated="mdLoading"> </b-skeleton>
  </div>
  <div v-else class="markdown-body" v-html="mdPreview">
    {{ mdPreview }}
  </div>
</template>

<script>
export default {
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
  methods: {
    renderMarkdown: function(){
      console.log('url changed');
      this.mdLoading = true;
      this.mdPlaceholder = true;
      fetch(`/api/markdown/?url=${this.url}`)
        .then(res => res.json())
        .then((data) => {
            this.mdLoading = false;
            if(data.markdown){
              this.mdPlaceholder = false;
              this.mdPreview = data.markdown;
              console.log('updating', this.$el);
              this.$nextTick(() => window.renderMathInElement(this.$el));
            }
        })
    },
  },
  watch: {
    url: function(){
      this.renderMarkdown();
    },
  },
  created: function(){
    if(this.url){
      this.renderMarkdown();
    }
  },
}
</script>
