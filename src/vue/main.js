import Vue from 'vue';
import Buefy from 'buefy'
import searchform from './components/searchform.vue';
import searchitem from './components/searchitem.vue';
import block from './components/block.vue';
import draftarticle from './components/draftarticle.vue';
import coverpreview from './components/coverpreview.vue';
import markdownpreview from './components/markdownpreview.vue';
import inputtags from './components/inputtags.vue';
import scrollnav from './components/scrollnav.vue';
import draftimage from './components/draftimage.vue';

Vue.use(Buefy);

window.vm = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  components: {
    'searchform': searchform,
    'searchitem': searchitem,
    'block': block,
    'draftarticle': draftarticle,
    'coverpreview': coverpreview,
    'markdownpreview': markdownpreview,
    'inputtags': inputtags,
    'scrollnav': scrollnav,
    'draftimage': draftimage,
  },
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
