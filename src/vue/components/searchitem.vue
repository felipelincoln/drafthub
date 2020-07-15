<template>
<b-dropdown role="menu">
  <a href="javascript:void(0);" class="navbar-item" slot="trigger" role="button" aria-label="search">
    <b-tooltip label="Search"
      type="is-dark"
      position="is-right">
      <b-icon icon="magnify"></b-icon>
    </b-tooltip>
  </a>

  <b-dropdown-item custom paddingless :focusable="false" role="menuitem">
    <form
      :action="action"
      method="get"
      role="search">
      <div class="dropdown-box">
        <b-input
          :value="value"
          name="q"
          :placeholder="placeholder"
          type="search"
          :aria-label="placeholder">
        </b-input>
        <input v-if="where" type="hidden" name="where" :value="where">
        <input v-if="who" type="hidden" name="who" :value="who">
      </div>
    </form>
  </b-dropdown-item>
</b-dropdown>
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
<style scoped>
.dropdown-box {
  min-width:300px;
  padding: 0 0.5rem;
}
</style>
