<template>
<h1 :id="id" class="is-size-4 is-capitalized has-text-weight-bold"><slot></slot></h1>
</template>
<script>
export default {
  props: [
    'id',
  ],
}
</script>
