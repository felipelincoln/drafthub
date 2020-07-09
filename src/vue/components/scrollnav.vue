<template>
  <nav class="scrollnav" role="navigation" aria-label="page navigation">
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
    <div class="scrollnav-list" :style="style()">
      <span class="scrollnav-span"><slot></slot></span>
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
      delta: 0,
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
      if(this.x < -this.delta) this.x = -this.delta
    },
    scrollLeft: function(){
      this.x += this.dx;
      if(this.x > 0) this.x = 0;
    },
    makeScroll: function(e) {
      this.x = 0;
      this.navWidth = this.$el.querySelector('.scrollnav-span').getBoundingClientRect().width
      this.containerWidth = this.$el.getBoundingClientRect().width
      this.dx = this.containerWidth*2/3
      this.delta = this.navWidth - this.containerWidth
    },
  },
  mounted: function(){
    this.makeScroll();
  },
  created: function() {
    window.addEventListener("resize", this.makeScroll);
  },
  destroyed: function() {
    window.removeEventListener("resize", this.makeScroll);
  },
}
</script>

<style scoped>
.scrollnav {
  position: relative;
  overflow: hidden;
  width: 100%;
}
.button {
  position: absolute;
  z-index: 1;
  top:0;
}
.btn-left {
  left:0;
}
.btn-right {
  right:0;
}
.scrollnav-list {
  position: relative;
  width: 100%;
  height: 40px;
  line-height: 40px;
  white-space: nowrap;
  transition: all 500ms cubic-bezier(.19,1,.22,1) 0s;
}
</style>
