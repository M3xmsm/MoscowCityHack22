import {createRouter, createWebHistory} from 'vue-router'
import CompanyProfile from '@/components/CompanyProfile'
import ProductsProfile from '@/components/ProductsProfile'
import NotFound from '@/components/NotFound'

const routes = [
    { path: "/company", component: CompanyProfile },
    { path: "/product", component: ProductsProfile },
    { path: "/:pathMatch(.*)*", component: NotFound }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router