// vue.js
Vue.component('draft-tag', {
	props: [
		'tagUrl',
		'tagPack',
		'tagIcon',
	],
		template: `
			<a :href="tagUrl">
				<b-tag type="is-dark" size="is-medium">
					<b-icon v-if="tagIcon != 'None'" :pack="tagPack" :icon="tagIcon" size="is-small"></b-icon>
					<span><slot></slot></span>
				</b-tag>
			</a>
		`
})

new Vue({
	el: '#app'
})
