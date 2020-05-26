// vue.js
Vue.component('draft-tag', {
	props: [
		'tagName',
		'tagUrl',
		'tagPack',
		'tagIcon',
	],
	
		template: `
			<a :href="tagUrl">
				<b-tag type="is-dark" size="is-medium">
					<b-icon v-if="tagIcon != 'None'" :pack="tagPack" :icon="tagIcon"></b-icon>
					<span>{{ tagName }}</span>
				</b-tag>
			</a>
		`
})

new Vue({
	el: '#app'
})
