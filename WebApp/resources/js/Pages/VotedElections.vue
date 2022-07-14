<script setup>
    import BreezeAuthenticatedLayout from '@/Layouts/Authenticated.vue'
    import BreezeButton from '@/Components/Button.vue'
    import { Head } from '@inertiajs/inertia-vue3'
</script>

<script>
    export default {
        props: ['voted_elections'],
        data() {
            return {
                list_of_elections: null
            }
        },
        methods: {
            copyToClipboard(value) {
                navigator.clipboard.writeText(value)
            }
        },
        mounted() {
            this.list_of_elections = JSON.parse(JSON.stringify(this.voted_elections)).original
        }
    }
</script>

<template>
    <Head title = "Results" />

    <BreezeAuthenticatedLayout>
        <template #header>
            <h2 class = "font-semibold text-xl text-gray-800 leading-tight">
                Voted Elections
            </h2>
        </template>

        <div class = "max-w-7xl mx-auto sm:px-6 lg:px-8 py-12">
            <div class = "bg-white overflow-auto shadow-sm sm:rounded-lg">
                <div class = "p-6 bg-white border-b border-gray-200">
                    <table class = 'min-w-full border'>
                        <thead class = 'border-b'>
                            <tr>
                                <th colspan = '2' class = 'border'>Election TXID</th>
                                <th colspan = '2' class = 'border'>Vote TXID</th>
                                <th class = 'border'>Vote Date</th>
                                <th class = 'border'>View Election</th>
                                <th class = 'border'>View Vote</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr v-for = '(value, key) in list_of_elections'>
                                <td class = 'border p-4'>
                                    {{ value['election_txid'].slice(0, 6) }}...{{ value['election_txid'].slice(value['election_txid'].length - 6) }}
                                </td>

                                <td class = 'border p-4'>
                                    <button @click = "copyToClipboard(value.election_txid)">
                                        <img class = 'inline max-h-5' src = '/icons/copy-to-clipboard.png'/>
                                        Copy
                                    </button>
                                </td>

                                <td class = 'border p-4'>
                                    {{ value['vote_txid'].slice(0, 6) }}...{{ value['vote_txid'].slice(value['vote_txid'].length - 6) }}
                                </td>

                                <td class = 'border p-4'>
                                    <button @click = "copyToClipboard(value.vote_txid)">
                                        <img class = 'inline max-h-5' src = '/icons/copy-to-clipboard.png'/>
                                        Copy
                                    </button>
                                </td>

                                <td class = 'border p-4'>
                                    {{ value['created_at'] }}
                                </td>

                                <td class = 'border text-center'>
                                    <a v-bind:href = "'/transaction_viewer?txid=' + value.vote_txid">
                                        <BreezeButton class = 'font-bold rounded-md text-white bg-indigo-600 hover:bg-indigo-800'>
                                            View Vote
                                        </BreezeButton>
                                    </a>
                                </td>

                                <td class = 'border text-center'>
                                    <a v-bind:href = "'/transaction_viewer?txid=' + value.election_txid">
                                        <BreezeButton class = 'font-bold rounded-md text-white bg-indigo-600 hover:bg-indigo-800'>
                                            View Election
                                        </BreezeButton>
                                    </a>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </BreezeAuthenticatedLayout>
</template>
