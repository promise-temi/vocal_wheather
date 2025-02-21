<template>

      <Header/>
      <MeteoInfo/>

  
</template>

<script>
import Header from './components/BarreDeNavigation.vue'
import MeteoInfo from './components/MeteoInfo.vue'

export default{
  components: {
    Header,
    MeteoInfo
}
}
</script>

<style scoped>
*{
  margin:0px;
  padding: 0px;
  box-sizing: border-box;
  color: white;
}






</style>
