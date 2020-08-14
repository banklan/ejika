<template>
  <v-container>
    <v-row class="justify-center mx-auto mt-5">
      <!-- <v-col md="5" class="hidden-sm">this should be hidden in small devices</v-col> -->
      <v-col cols="12" md="6">
        <v-card light shaped elevation="6" min-height="350">
          <v-card-title class="title primary white--text justify-center">Login</v-card-title>
          <v-card-text class="mt-5">
            <v-text-field label="Email" v-model="email" required v-validate="'required|email'" :error-messages="errors.collect('email')" name="email"></v-text-field>
            <v-text-field type="password" label="Password" v-model="password" required v-validate="'required'" :error-messages="errors.collect('password')" name="password"></v-text-field>
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn large class="primary white--text" @click.prevent="login" :loading="loading">Login</v-btn>
          </v-card-actions>
          <span class="register">
            <p class="body-2 text-center mt-3">
              <router-link to="/forgot_password">Forgot your password?</router-link> | Not yet a member?
              <router-link to="/register">Register Now</router-link>
            </p>
          </span>
          <span v-if="loginError" class="text-center">
            <div class="red lighten-3 red--text pa-2">{{ loginErrorMsg }}</div>
          </span>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: null,
      loginErrorMsg: null,
      loginError: false,
      loading: false
    };
  },
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
  methods: {
    login() {
      this.$validator.validateAll().then(isValid => {
        if (isValid) {
          this.loading = true;
          this.$axios
            .post("http://localhost:8000/api-token-auth/", {
              username: this.email,
              password: this.password
            })
            .then(res => {
              this.loading = false;
              localStorage.setItem("auth-token", res.data.token);
              this.$store.commit("store_token", res.data.token);
              this.$store.dispatch("getAuthUser");
              this.$router.push("/");
            })
            .catch(() => {
              this.loading = false;
              this.loginError = true;
              this.loginErrorMsg = "Login failed. Invalid login credentials";
            });
        }
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.v-card {
  .v-card__actions {
    .v-btn {
      width: 50% !important;
    }
  }
  .register p a {
    text-decoration: none;
  }
}
</style>
