<template>
  <div id="scrollContainer">
    <b-button id="btnLeft" v-if="x < 0" @click="scrollLeft()" aria-hidden="true">
      <b-icon icon="chevron-left"></b-icon>
    </b-button>
    <b-button id="btnRight" v-if="x > containerWidth -navWidth" @click="scrollRight()" aria-hidden="true">
      <b-icon icon="chevron-right"></b-icon>
    </b-button>
    <nav id="scrollNav" :style="style()">
      <span id="scrollSpan"><slot></slot></span>
    </nav>
  </div>
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
    this.navWidth = document.getElementById('scrollSpan').getBoundingClientRect().width
    this.containerWidth = document.getElementById('scrollContainer').getBoundingClientRect().width
    if(this.navWidth > this.containerWidth){
      this.dx = Math.min(this.containerWidth, this.navWidth - this.containerWidth)
    }
  },
}
</script>

<style scoped>
#scrollContainer {
  position: relative;
  overflow: hidden;
  width: 100%;
}
#btnLeft,
#btnRight {
  position: absolute;
  top:0;
}
#btnLeft {
  left:0;
}
#btnRight {
  right:0;
}
#scrollNav {
  position: relative;
  z-index: -1;
  width: 100%;
  height: 40px;
  line-height: 40px;
  white-space: nowrap;
  transition: all 250ms ease-out 0s;
}
</style>
