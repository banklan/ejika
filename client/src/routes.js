import Home from './components/Home';
import ServicesByLoc from './components/ServicesByLoc';
import ServiceShow from './components/ServiceShow';
import Login from './components/Login';
import Register from './components/Register';
import Profile from './components/Profile';
// import CreateService from './components/Login';
import Registered from './components/Registered';
import Contact from './components/Contact';
import About from './components/About';
import PortFolioShow from './components/PortFolioShow';
import AllServices from './components/AllServices';
import ServicesByState from './components/ServicesByState';
import Testimonials from './components/Testimonials';
import HowItWorks from './components/HowItWorks';
import FreqAskedQstns from './components/FreqAskedQstns';
import AppliancesFinancing from './components/AppliancesFinancing';
import TermsAndConditions from './components/TermsAndConditions';
import ApplicationSubmitted from './components/ApplicationSubmitted';
import PrivacyPolicy from './components/PrivacyCookie';
import ForgotPassword from './components/ForgotPassword';
import PasswordReset from './components/PasswordReset';
import PasswordResetSuccess from './components/PasswordResetSuccess';


export default [{
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {path: '/register', name: 'Register', component: Register },
    {path: '/contact_us', name: 'Contact', component: Contact},
    {path: '/about_us', name: 'About', component: About},
    {path: '/services/:state/:categ', name: 'ServicesByLoc', component: ServicesByLoc, props: true},
    {path: '/service/:id/:slug', name: 'ServiceShow',component: ServiceShow},
    {path: '/profile', name: 'Profile', component: Profile},
    {path: '/registration_successfull', name: 'Registered', component: Registered},
    {path: '/porfolio/:id/:slug', name: 'PortFolioShow', component: PortFolioShow},
    {path: '/services', name: 'AllServices', component: AllServices, props: true },
    {path: '/testimonials', name: 'Testimonials', component: Testimonials },
    {path: '/how_it_works', name: 'HowItWorks',  component: HowItWorks},
    {path: '/faq', name: 'FreqAskedQstns',  component: FreqAskedQstns},
    {path: '/appliances_financing', name: 'AppliancesFinancing',  component: AppliancesFinancing},
    {path: '/terms_conditions', name: 'TermsAndConditions', component: TermsAndConditions },
    {path: '/application_submitted', name: 'ApplicationSubmitted', component: ApplicationSubmitted},
    {path: '/privacy_policy', name: 'PrivacyPolicy', component: PrivacyPolicy },
    {path: '/state/:id/:slug', name: 'ServicesByState', component: ServicesByState},
    {path: '/forgot_password', name: 'ForgotPassword', component: ForgotPassword},
    {path: '/password_reset/:email/:token', name: 'PasswordReset', component: PasswordReset},
    {path: '/password_reset_success', name: 'PasswordResetSuccess', component: PasswordResetSuccess},
]