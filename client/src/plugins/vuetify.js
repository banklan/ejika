import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import colors from 'vuetify/lib/util/colors'

Vue.use(Vuetify)

const opts = {
    theme:{
         themes: {
            light: {
                primary: '#003B63',
                pry_light: '#0063ab',
                secondary: '#002E4F',
                accent: colors.red.accent3,
                error: '#b71c1c',
                lightbg: '#fff',
            },
        },
    }
}

export default new Vuetify(opts)

// #003B63 - blue
// #002E4F - dark blue
// #FF6433 - orange
// colors.red.accent3