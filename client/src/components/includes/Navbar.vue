<template>
  <nav>
    <v-app-bar flat light color="lightbg" height="65">
      <span class="hidden-md-and-up">
        <v-app-bar-nav-icon class="secondary--text hidden-md-and-up" @click="sidebar = true"></v-app-bar-nav-icon>
      </span>
      <v-toolbar-title class="secondary--text pl-5 ml-n3">
        <router-link to="/" tag="span" style="cursor: pointer" exact>
          e<span class="ji">ji</span>ka
        </router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <span v-if="isLoggedIn" class="mr-5">Welcome {{ authUser.first_name | capFirstLetter }}</span>
      <v-toolbar-items class="hidden-sm-and-down menu_items">
        <router-link v-for="item in menuItems" :key="item.title" :to="item.path">{{ item.title }}</router-link>
        <template v-if="authToken">
          <router-link v-for="item in authMenuItems" :key="item.title" :to="item.path">{{ item.title }}</router-link>
          <button type="button" class="primary--text" @click="logout">Logout</button>
        </template>
        <template v-else>
          <router-link v-for="item in nonAuthMenuItems" :key="item.title" :to="item.path">{{ item.title }}</router-link>
        </template>
      </v-toolbar-items>
    </v-app-bar>
    <v-navigation-drawer absolute v-model="sidebar" color="primary white--text" class="hidden-md-and-up" disable-resize-watcher>
      <v-toolbar-title class="white--text ml-4 mt-3 pb-4">
        <router-link to="/" tag="span" style="cursor: pointer" exact>
          e<span class="ji">ji</span>ka
        </router-link>
      </v-toolbar-title>
      <v-divider></v-divider>
      <v-list class="ml-4">
          <v-list-item dark class="white--text" v-for="item in menuItems" :key="item.title" link :to="item.path">
              <v-list-item-content>
                  <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item-content>
          </v-list-item>
          <template v-if="isLoggedIn">
            <v-list-item dark class="white--text" v-for="item in authMenuItems" :key="item.title" link :to="item.path">
                <v-list-item-content>
                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                </v-list-item-content>
            </v-list-item>
            <v-list-item dark class="white--text">
              <button type="button" class="white--text" @click="logout">Logout</button>
            </v-list-item>
          </template>
          <template v-else>
            <v-list-item dark class="white--text" v-for="item in nonAuthMenuItems" :key="item.title" link :to="item.path">
                <v-list-item-content>
                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                </v-list-item-content>
            </v-list-item>
          </template>
      </v-list>
    </v-navigation-drawer>
    
    <v-snackbar v-model="loggedOut" :timeout="6000" top color="green darken-1 white--text">
      You have successfully logged out!
      <v-btn text color="white--text" @click="loggedOut = false">Close</v-btn>
    </v-snackbar>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      sidebar: false,
      menuItems: [
        { title: "About", path: "/about_us", icon: "mdi-view-dashboard" },
        { title: "Services", path: "/services", icon: "mdi-group" },
        { title: "Financing", path: "/appliances_financing", icon: "mdi-group" },
        { title: "Contact", path: "/contact_us", icon: "mdi-group" },
      ],
      authMenuItems: [
        { title: "Profile", path: "/profile", icon: "folder" }
      ],
      nonAuthMenuItems: [
        { title: "Login", path: "/login", icon: "folder" },
        { title: "Register", path: "/register", icon: "user" }
      ],
      loggedOut: false
    };
  },
  computed: {
    authToken() {
      return this.$store.getters.getToken;
    },
    authUser() {
      return this.$store.getters.getAuthUser;
    },
    isLoggedIn(){
      return this.$store.getters.isLoggedIn
    },
  },
  methods: {
    logout() {
      if (this.authToken) {
        this.$store.commit("logout");
        if (this.$route.path != "/") {
          this.$router.push("/");
        }
        this.loggedOut = true;
      }
    }
  }
};
</script>

<style lang="scss" scoped>
  nav{
    width: 100vw !important;
  }
  .v-app-bar {
    background-color: transparent !important;
    width: 100vw !important;
    margin: 0;
  }
  .v-toolbar__title {
    font-family: "Baloo 2", cursive;
    font-weight: 600;
    font-size: 28px !important;
    .ji {
      color: #ff1744;
    }
  }
  .v-toolbar__items a.v-btn--active {
    background: none !important;
  }

  .menu_items {
    width: 40%;
    display: flex;
    justify-content: space-around;
    align-items: center;

    button {
      text-transform: capitalize;
      font-size: inherit;
      padding-left: 15px !important;
      transition: all 0.6s !important;
      padding: 6px 12px !important;
      border-radius: 50px;

      &:hover {
        background: #003b63;
        color: #fff !important;
        text-transform: none;
        border-radius: 100px;
      }
    }

    a {
      padding-right: 10px;
      text-decoration: none;
      transition: all 0.6s;
      padding: 6px 12px;

      &:focus {
        outline: none;
      }
      &:hover,
      &.router-link-active,
      &.router-link-exact-active {
        background: #003b63;
        color: #fff;
        text-transform: none;
        border-radius: 100px;
      }
    }
  }
  .v-navigation-drawer{
  .v-divider{
    border-color: #144A6F !important;
  }
   button{
    text-transform: capitalize;
    font-size: inherit;
    transition: all 0.6s !important;
    margin-left: -10px;
    padding: 10px !important;
    border-radius: 100px;
    color: #fff;

    &:hover {
      background: #144A6F;
      color: #fff !important;
      text-transform: none;
      border-radius: 100px;
      padding: 10px 25px 10px 10px !important;
    }
   }
}
</style>
