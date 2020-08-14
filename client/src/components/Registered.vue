<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8" offset-md="2" class="pa-3 mt-4">
        <v-alert type="success">
          Congratulations, Your registration was successfull.Please
          <router-link to="/login" class="primary--text font-weight-bold">&nbsp;login&nbsp;</router-link>with your credentials.
        </v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  computed: {
    authToken() {
      return this.$store.getters.getToken;
    }
  },
  beforeRouteEnter(to, from, next) {
    next(vm => {
      if (vm.authToken) {
        next("/");
      }
    });
  },
}
</script>

<style scoped>
.v-alert__wrapper .v-alert__content a {
  text-decoration: none;
  transition: all 0.4s;
}
.v-alert__wrapper .v-alert__content a:hover {
  color: #ff1744 !important;
}
</style>