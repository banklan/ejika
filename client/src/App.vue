<template>
  <v-app>
    <template v-if="currentRoute === 'Home'" transition="scale-transition">
      <Navbar/>
    </template>
    <template v-else transition="scale-transition">
      <Navbar2/>
    </template>
    <v-content>
      <router-view></router-view>
    </v-content>
    <Footer/>
  </v-app>
</template>

<script>
import Navbar from './components/includes/Navbar'
import Navbar2 from './components/includes/Navbar2'
import Footer from './components/includes/Footer'

export default {
  name: 'App',

  components: {
    Navbar,
    Navbar2,
    Footer
  },

  computed: {
    currentRoute(){
      return this.$route.name
    }
  }
};
</script>
