<template>
  <h1
    :id="id"
    style="text-transform:uppercase"
    class="pb-5">
    <strong><slot></slot></strong>
  </h1>
</template>

<script>
export default {
  props: [
    'id',
  ],
}
</script>
