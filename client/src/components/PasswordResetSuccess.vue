<template>
    <v-container>
        <v-row justify="center">
            <v-col cols="12" md="10">
                <v-alert type="success" class="my-8">
                    Your password has been reset successfully. You can now  <router-link to="/login">login</router-link> with the new password. Thank you for using ejika.com.
                </v-alert>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    export default{
        beforeRouteEnter(to, from, next) {
            next(vm => {
                if (vm.authToken) {
                    next("/");
                }
            });
        },
    }

</script>