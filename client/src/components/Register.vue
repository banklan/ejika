<template>
  <v-container>
    <v-row class="justify-center mx-auto mt-12">
      <v-col cols="12" md="6">
        <div class="register_info">
          <h2
            class="headline font-weight-light primary--text darken-3"
          >Enlist your services, upload your portfolio, and position your business a notch above others..</h2>
          <h2 class="headline accent--text font-weight-thin">Register Free</h2>
          <p class="body-1 mt-5 py-4">
            Already a member?
            <router-link to="/login">Login Now</router-link>
          </p>
        </div>
      </v-col>
      <v-col cols="12" md="6">
        <v-card light shaped elevation="6" min-height="350">
          <v-card-title class="title primary white--text justify-center">Register</v-card-title>
          <v-card-text class="mt-5">
            <v-text-field label="First Name" v-model="f_name" required v-validate="'required'" :error-messages="errors.collect('f_name')" name="f_name" data-vv-as="first name"></v-text-field>
            <v-text-field label="Last Name" v-model="l_name" required v-validate="'required'" :error-messages="errors.collect('l_name')" name="l_name" data-vv-as="last name"></v-text-field>
            <v-text-field type="text" label="Email" v-model="email" required v-validate="'required|email'" :error-messages="errors.collect('email')" name="email"></v-text-field>
            <v-text-field type="password" label="Password" v-model="password" required v-validate="'required|min:6|max:20'" :error-messages="errors.collect('password')" name="password" ref="password"></v-text-field>
            <v-text-field type="password" label="confirm Password" v-model="conf_pswd" required v-validate="'required|confirmed:password'" :error-messages="errors.collect('conf_pswd')" name="conf_pswd" data-vv-as="confirm password"></v-text-field>
            <v-select :items="genderChoice" item-text="type" item-value="val" label="Gender" v-model="gender" persistent-hint required v-validate="'required'" :error-messages="errors.collect('gender')" name="gender"></v-select>
          </v-card-text>
          <v-card-actions class="justify-center py-4">
            <v-btn
              large
              class="primary white--text mb-4"
              @click.prevent="register"
              :loading="loading"
            >Register</v-btn>
          </v-card-actions>
          <div v-if="createError">
            <div class="pink lighten-1 red--text lighten-3 pa-4">
              <div v-for="(err, i) in createErrResponse" :key="i">
                <div v-for="(msg, j) in err" :key="j">{{ msg.field }} - {{ msg.message }}</div>
              </div>
            </div>
          </div>
        </v-card>
      </v-col>
      <v-snackbar v-model="createErrorSb" :timeout="5000" top color="red darken-1 white--text">
        User registeration failed.
        <v-btn text color="white--text" @click="createErrorSb = false">Close</v-btn>
      </v-snackbar>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      f_name: "",
      l_name: "",
      email: "",
      gender: '',
      password: "",
      conf_pswd: "",
      loading: false,
      createdMsg: null,
      createErrorSb: false,
      createError: false,
      createErrResponse: [],
      genderChoice: [
        {type: 'Male', val: 'M'},
        {type: 'Female', val: 'F'},
      ]
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
    register() {
      this.$validator.validateAll().then(isValid => {
        if (isValid) {
          this.loading = true;
          this.$axios
            .post("http://localhost:8000/api/user/register/", {
              first_name: this.f_name,
              last_name: this.l_name,
              email: this.email,
              gender: this.gender,
              password: this.password,
              c_password: this.conf_pswd
            })
            .then(res => {
              this.loading = false;
              console.log(res.data);
              this.createdMsg = res.message;
              this.$router.push("/registration_successfull");
            })
            .catch(err => {
              this.loading = false;
              this.createError = true;
              this.createErrorSb = true;
              this.createErrResponse = err.response.data;
              console.log(err.response.data);
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
.register_info {
  padding: 15px 45px;
  min-height: 25rem;
  display: flex;
  flex-direction: column;
  justify-content: center;

  h2:first-child {
    font-family: "Baloo Thambi 2", cursive;
    font-size: 30px !important;
    line-height: 1.55;
  }
  h2:last-child {
    margin-top: 25px;
    font-family: "Open Sans", sans-serif;
    font-size: 36px !important;
    font-weight: 300 !important;
  }
  p > a {
    text-decoration: none !important;
    transition: all 0.4s;

    &:hover {
      color: #ff1744;
    }
  }
}
</style>
