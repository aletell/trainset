import Vue from 'vue'
import VueRouter from 'vue-router'

// router components
import Index from '@/views/Index'
import Help from '@/views/Help'
import Labeler from '@/views/Labeler'
import License from '@/views/License'
import TimelineClone from '@/views/TimelineClone'
import Analytics from '@/views/Analytics'
import ProjectManagement from '@/views/ProjectManagement'
import Explore from '@/views/Explore'

Vue.use(VueRouter);

const routes = [
        { name: 'home', path: '/', component: Index, props: true },
        { name: 'help', path: '/help', component: Help },
        { name: 'license', path: '/license', component: License },
        { name: 'labeler', path: '/labeler', component: Labeler,
          props: route => ({
            ...route.params,
            ...route.query,
            useLocal: route.query.useLocal === '1' || route.query.useLocal === 'true',
            isValid: route.query.isValid ? route.query.isValid === 'true' : true
          }) },
        { name: 'timeline', path: '/timeline', component: TimelineClone },
        { name: 'analytics', path: '/analytics', component: Analytics },
        { name: 'project-management', path: '/project-management', component: ProjectManagement },
        { name: 'explore', path: '/explore', component: Explore }
];

export default new VueRouter({
	routes,
	mode: 'history'
});