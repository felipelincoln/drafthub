// vue.js
Vue.component('draft-tag', {
	props: [
		'tagUrl',
		'tagPack',
		'tagIcon',
	],
		template: `
			<b-button
				style="font-family:monospace;"
				size="is-small"
				type="is-dark"
				tag="a"
				:href="tagUrl"
				:icon-pack="tagPack"
				:icon-left="tagIcon">
				<slot></slot>
			</b-button>
		`
})


const dbTags = ['python', 'albion-pvp', 'django']


new Vue({
	el: '#app',
	delimiters: ['[[', ']]'],
	data:{
		tags: [],
		filteredTags: dbTags,
	},
	methods: {
		getFilteredTags(text){
			this.filteredTags = dbTags.filter((item) => {
				return item.indexOf(text.toLowerCase()) >= 0
			})
		},
	}
})
