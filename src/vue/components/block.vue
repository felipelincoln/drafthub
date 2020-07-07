<template>
  <section class="mb-6" :aria-labelledby="id">
    <h1 :id="id" class="pb-5">
      <strong>{{ heading }}</strong>
    </h1>
    <slot></slot>
  </section>
</template>

<script>
export default {
  props: [
    'id',
    'heading',
  ],
}
</script>
<style scoped>
h1 {
  text-transform: uppercase;
}
</style>
