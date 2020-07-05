<template>
  <form
    :action="action"
    method="get">
    <b-input
      :value="value"
      name="q"
      :placeholder="placeholder"
      type="search"
      :aria-label="placeholder">
    </b-input>
    <input v-if="where" type="hidden" name="where" :value="where">
    <input v-if="who" type="hidden" name="who" :value="who">
  </form>
</template>

<script>
export default {
  props: [
    'value',
    'action',
    'placeholder',
    'where',
    'who',
  ],
}
</script>
