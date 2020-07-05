<template>
  <div @keydown="getCurrentOption()">
    <b-taginput
      :id="id"
      ref="taginput"
      :value="value"
      :data="filteredTags"
      autocomplete
      :allow-new="true"
      maxlength="25"
      maxtags="5"
      icon="label"
      :confirm-key-codes="getKeyCodes()"
      @input="$emit('input', $event)"
      @remove="showDeletedTag"
      @add="filteredTags = []"
      @typing="getFilteredTags"
      role="combobox"
      aria-autocomplete="list"
      aria-haspopup="true"
      :aria-expanded="filteredTags.length? 'true':'false'"
      :aria-describedby="ariaDescribedby"
      :aria-required="ariaRequired"
      :aria-invalid="ariaInvalid">
      <template v-slot:default="item">
        <span :role="option == item.option? 'alert' : undefined">
          {{ item.option }}
        </span>
      </template>
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
    'id',
    'ariaDescribedby',
    'ariaRequired',
    'ariaInvalid',
  ],
  data: function(){
    return {
      filteredTags: [],
      option: undefined,
    }
  },
  methods: {
    getFilteredTags: function(text){
      if(text){
        this.filteredTags = this.api
          .filter(x => !this.value.includes(x))
          .filter(x => x.indexOf(text.toLowerCase()) >= 0)
      }else{
        this.filteredTags = []
      }
    },
    showDeletedTag: function(){
      let deletedTag = this.value.filter(x => !vm.newArticle.tags.includes(x));
      let lastTag = this.value.slice(-1)[0];
      if(deletedTag == lastTag){
        this.$refs.taginput.newTag = lastTag;
      }
    },
    getKeyCodes: function(){
      console.log('keycode changed!');
      if('taginput' in this.$refs){
        if(this.$refs.taginput.newTag) return [13, 188, 9]
      }
      return [13, 188]
    },
    getCurrentOption: function(){
      let el = document.querySelector('.is-hovered');
      if(el) this.option = el.innerText;
      else { this.option = undefined }
      console.log('update aria-label', this.option);
    },
  },
  computed: {
    getTagsInputValue: function(){
      return this.value.join(', ')
    },
  },
}
</script>
