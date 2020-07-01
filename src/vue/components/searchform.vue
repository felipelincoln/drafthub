<template>
  <form
    :action="action"
    method="get">
    <b-input
      :value="value"
      name="q"
      :placeholder="placeholder"
      type="search"
      aria-label="Search">
    </b-input>
  </form>
</template>

<script>
export default {
  props: [
    'value',
    'action',
    'placeholder',
  ],
}
</script>
