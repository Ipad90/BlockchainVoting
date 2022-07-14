<script setup>
    import BreezeAuthenticatedLayout from '@/Layouts/Authenticated.vue'
    import BreezeButton from '@/Components/Button.vue'
    import BreezeInput from '@/Components/Input.vue'
    import BreezeLabel from '@/Components/Label.vue'
    import { Head, useForm } from '@inertiajs/inertia-vue3'
</script>

<script>
    export default {
        data() {
            return {
                election_list: [],
                active_elections: false
            }
        },
        props: ['elections'],
        methods: {
            async getElectionDetails(txids) {
                await txids.forEach((txid) => {
                    let message = {
                        'headers': {
                            'tx_hash': txid
                        },
                        'tx_details': {
                            'tx_type': 'view_tx'
                        }
                    }
                    axios.post('/api/get_tx', message)
                        .then((response) => {
                            if ('specified_tx_details' in response.data.tx_details) {
                                if (response.data.tx_details.specified_tx_details != {}) {
                                    this.election_list.push(JSON.parse(JSON.stringify(response.data.tx_details.specified_tx_details)))
                                }
                            }
                        }).catch((error) => {
                            console.log(error)
                        })
                })
            },
            convertUnixDateTimeToStandardDateTime(timestamp) {
                return new Date(timestamp).toLocaleString('sv-SE')
            },
            copyToClipboard(value) {
                navigator.clipboard.writeText(value)
            }
        },
        mounted() {
            let election_txids = JSON.parse(JSON.stringify(this.elections))
            election_txids = election_txids['tx_details']['election_txid_list']

            this.active_elections = (election_txids.length > 0) ? true : false
            this.getElectionDetails(election_txids)
        }
    }
</script>

<template>
    <Head title = 'Dashboard' />

    <BreezeAuthenticatedLayout>
        <template #header>
            <h2 class = 'font-semibold text-xl text-gray-800 leading-tight'>
                Dashboard
            </h2>
        </template>

        <div class = 'max-w-7xl mx-auto sm:px-6 lg:px-8 py-12'>
            <div :class = "{ 'hidden': active_elections }" class = 'p-8 bg-white overflow-hidden shadow-sm sm:rounded-lg mb-12 text-center'>
                <h2>No elections icri</h2>
            </div>

            <div :class = "{ 'hidden': !active_elections }" class = 'p-8 bg-white overflow-auto shadow-sm sm:rounded-lg mb-12 text-center'>
                <h2>Elections to vote</h2>
            </div>

            <div :class = "{ 'hidden': !active_elections }" class = 'p-8 bg-white overflow-auto shadow-sm sm:rounded-lg mb-12'>
                <table class = 'min-w-full border'>
                    <thead>
                        <tr>
                            <th class = 'border px-4'>Election Name</th>
                            <th colspan = '2' class = 'border px-4'>Election TXID</th>
                            <th class = 'border px-4'>Election Start Date</th>
                            <th class = 'border px-4'>Election End Date</th>
                            <th class = 'border px-4'>View Results</th>
                            <th class = 'border px-4'>Vote</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr v-for = '(value, key) in election_list'>
                            <td class = 'border p-4'>
                                {{ value['tx_details']['election_details']['election_name'] }}
                            </td>

                            <td class = 'border p-4'>
                                <a v-bind:href = "'/vote/' + value.headers.tx_hash">
                                    {{ value['headers']['tx_hash'].slice(0, 6) }}...{{ value['headers']['tx_hash'].slice(value['headers']['tx_hash'].length - 6) }}
                                </a>
                            </td>

                            <td class = 'border p-4'>
                                <button @click = "copyToClipboard(value.headers.tx_hash)">
                                    <img class = 'inline max-h-5' src = '/icons/copy-to-clipboard.png'/>
                                    Copy
                                </button>
                            </td>

                            <td class = 'border p-4'>
                                {{ convertUnixDateTimeToStandardDateTime(value['tx_details']['election_details']['start_timestamp']) }}
                            </td>

                            <td class = 'border p-4'>
                                {{ convertUnixDateTimeToStandardDateTime(value['tx_details']['election_details']['end_timestamp']) }}
                            </td>

                            <td class = 'border text-center'>
                                <a v-bind:href = "'/transaction_viewer?txid=' + value.headers.tx_hash">
                                    <BreezeButton class = 'font-bold rounded-md text-white bg-indigo-600 hover:bg-indigo-800'>
                                        View Results
                                    </BreezeButton>
                                </a>
                            </td>

                            <td class = 'border text-center'>
                                <a v-bind:href = "'/vote/' + value.headers.tx_hash">
                                    <BreezeButton class = 'font-bold rounded-md text-white bg-indigo-600 hover:bg-indigo-800'>
                                        Vote
                                    </BreezeButton>
                                </a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </BreezeAuthenticatedLayout>
</template>
