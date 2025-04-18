import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from "../views/LandingPage.vue";
import CustomerLogin from '@/views/CustomerLogin.vue';
import AdminLogin from '@/views/AdminLogin.vue';
import SecurityLogin from '@/views/SecurityLogin.vue';
import UserRegister from '@/views/UserRegister.vue';
import CustomerDashboard from '@/views/CustomerDashboard.vue';
import SecurityDashboard from '@/views/SecurityDashboard.vue';
import AdminDashboard from '@/views/AdminDashboard.vue';
import ChangePassword from '@/views/ChangePassword.vue';
import EnableMFA from '@/views/EnableMFA.vue'; // ✅ Correct Path
import UserNotifications from '@/views/UserNotifications.vue'; // ✅ Correct Path
import LoginHistory from '@/views/LoginHistory.vue'; // ✅ Correct Path
import AddUser from '@/views/AddUser.vue';  // ✅ Ensure this file exists
import DeleteUser from '@/views/DeleteUser.vue';  // ✅ Ensure this file exists
import SystemLogs from '@/views/SystemLogs.vue';  // ✅ Ensure this file exists
import FileUpload from '@/components/FileUpload.vue';
const routes = [
  
  { path: '/register', component: UserRegister },
  { path: '/', component: LandingPage },
  { path: '/admin-login', component: AdminLogin },
  { path: '/customer-login', component: CustomerLogin },
  { path: '/security-login', component: SecurityLogin },
  { path: '/customer-dashboard', component: CustomerDashboard },
  { path: '/security-dashboard', component: SecurityDashboard },
  { path: '/admin-dashboard', component: AdminDashboard },
  { path: '/change-password', component: ChangePassword },
  { path: '/enable-mfa', component: EnableMFA },
  { path: '/notifications', component: UserNotifications },
  { path: '/login-history', component: LoginHistory },
  { path: '/add-user', component: AddUser },  // ✅ Route for Add User
  { path: '/delete-user', component: DeleteUser },  // ✅ Route for Delete User
  { path: '/system-logs', component: SystemLogs },  // ✅ Route for System Logs
  { path: '/file-upload', component: FileUpload },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
