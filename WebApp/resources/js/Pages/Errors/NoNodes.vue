<script setup>
    import BreezeAuthenticatedLayout from '@/Layouts/Authenticated.vue'
    import BreezeButton from '@/Components/Button.vue'
    import BreezeInput from '@/Components/Input.vue'
    import BreezeLabel from '@/Components/Label.vue'
    import { Head, useForm } from '@inertiajs/inertia-vue3'
</script>

<script>
</script>

<template>
    <Head title = 'No Nodes' />

    <BreezeAuthenticatedLayout>
        <template #header>
            <h2 class = 'font-semibold text-xl text-gray-800 leading-tight'>
                No Nodes
            </h2>
        </template>
    </BreezeAuthenticatedLayout>
</template>
