<template>
  <nav class="navbar" role="navigation" aria-label="page navigation">
    <button
      v-if="x < 0"
      class="button btn-left"
      @click="scrollLeft()"
      aria-hidden="true"
      tabindex="-1">
      <b-icon icon="chevron-left"></b-icon>
    </button>
    <button
      v-if="x > containerWidth -navWidth"
      class="button btn-right"
      @click="scrollRight()"
      aria-hidden="true"
      tabindex="-1">
      <b-icon icon="chevron-right"></b-icon>
    </button>
    <div class="navbar-menu" :style="style()">
      <div class="navbar-start"><slot></slot></div>
    </div>
  </nav>
</template>

<script>
export default {
  data: function(){
    return {
      navWidth: 0,
      containerWidth: 0,
      x: 0,
      dx: 0,
    }
  },
  methods: {
    style: function(){
      return {
        transform: `translateX(${this.x}px)`
      }
    },
    scrollRight: function(){
      this.x -= this.dx;
    },
    scrollLeft: function(){
      this.x += this.dx;
    },
  },
  mounted: function(){
    this.navWidth = this.$el.querySelector('.navbar-start').getBoundingClientRect().width
    this.containerWidth = this.$el.getBoundingClientRect().width
    if(this.navWidth > this.containerWidth){
      this.dx = Math.min(this.containerWidth, this.navWidth - this.containerWidth)
    }
  },
}
</script>

<style scoped>
.navbar {
  position: relative;
  overflow: hidden;
  width: 100%;
}
.button {
  position: absolute;
  top:6px;
}
.btn-left {
  left:0;
}
.btn-right {
  right:0;
}
.navbar-menu {
  position: relative;
  z-index: -1;
  width: 100%;
  white-space: nowrap;
  transition: all 250ms ease-out 0s;
}
</style>
