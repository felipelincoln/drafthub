// vue.js
Vue.component('draft-tag', {
	props: [
		'tagUrl',
		'tagPack',
		'tagIcon',
	],
		template: `
			<b-button
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

new Vue({
	el: '#app'
})
