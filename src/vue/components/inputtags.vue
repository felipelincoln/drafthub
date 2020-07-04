<template>
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
      :confirm-key-codes="[13, 188, 9]"
      @input="$emit('input', $event)"
      @remove="showDeletedTag"
      @typing="getFilteredTags">
    </b-taginput>
  <input type="hidden" :name="name" :value="getTagsInputValue">
  </div>
</template>

<script>
export default {
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
}
</script>
