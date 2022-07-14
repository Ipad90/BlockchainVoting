<script setup>
    import BreezeAuthenticatedLayout from '@/Layouts/Authenticated.vue';
    import BreezeButton from '@/Components/Button.vue'
    import BreezeInput from '@/Components/Input.vue'
    import BreezeLabel from '@/Components/Label.vue'
    import { Head, useForm } from '@inertiajs/inertia-vue3'
</script>

<script>
    export default {
        data() {
            return {
                transaction_to_view: {
                    headers: {
                        tx_hash: ''
                    },
                    tx_details: {
                        tx_type: 'view_tx',
                        specified_tx_details: {}
                    }
                },
                transaction_not_found: true,
                transaction_validity: {
                    recalculated_hash: '',
                    validity: false
                },
                transaction_is_election: false,
                no_decrypted_data: true,
                election_results: {},
                decryption: {
                    to_decrypt: '',
                    decryption_key: '',
                    decrypted_data: {}
                }
            }
        },
        methods: {
            submit() {
                if (this.transaction_to_view.headers.tx_hash != '') {
                    axios.post('/api/get_tx', this.transaction_to_view)
                        .then((response) => {
                            if ('specified_tx_details' in response.data.tx_details) {
                                if (response.data.tx_details.specified_tx_details != {}) {
                                    this.transaction_to_view.headers.tx_hash = response.data.headers.tx_hash
                                    this.transaction_to_view.tx_details.specified_tx_details = response.data.tx_details.specified_tx_details
                                    this.transaction_to_view.tx_details.specified_tx_details = JSON.parse(JSON.stringify(this.transaction_to_view.tx_details.specified_tx_details))
                                    this.transaction_not_found = false

                                    if (response.data.tx_details.specified_tx_details.tx_details.tx_type == 'add_election') {
                                        this.transaction_is_election =  true
                                        this.getElectionResults()
                                    } else {
                                        this.transaction_is_election = false
                                    }
                                }
                            } else {
                                this.transaction_not_found = true
                            }
                        }).catch((error) => {
                            console.log(error)
                        })
                }
            },
            getElectionResults() {
                axios.post('/api/get_election_results', this.transaction_to_view)
                    .then((response) => {
                        if (response.data.tx_details.results != {}) {
                            this.election_results = response.data.tx_details.results
                            this.election_results = JSON.parse(JSON.stringify(this.election_results))
                        }
                    }).catch((error) => {
                        console.log(error)
                    })
            },
            setToViewTXHash(e) {
                this.transaction_to_view.headers.tx_hash = e.target.value
            },
            recalculateHash() {
                axios.post('/api/recalculate_hash', this.transaction_to_view.tx_details.specified_tx_details)
                    .then((response) => {
                        this.transaction_validity = response.data
                    }).catch((error) => {
                        console.log(error)
                    })
            },
            decryptData() {
                if (this.to_decrypt != '' && this.decryption_key != '') {
                    axios.post('/api/decryptor', this.decryption)
                        .then((response) => {
                            if (response.data.status == 'approved') {
                                this.decryption.decrypted_data = response.data.decrypted_data
                                this.no_decrypted_data = false
                            } else {
                                this.no_decrypted_data = true
                            }
                        })
                        .catch((error) => {
                            console.log(error)
                        })
                }
            }
        },
        mounted() {
            let uri = window.location.search.substring(1)
            this.transaction_to_view.headers.tx_hash = new URLSearchParams(uri).get('txid')
        }
    }
</script>

<template>
    <Head title = "Transaction Viewer" />

    <BreezeAuthenticatedLayout>
        <template #header>
            <h2 class = "font-semibold text-xl text-gray-800 leading-tight">
                Transaction Viewer
            </h2>
        </template>

        <div class = 'max-w-7xl mx-auto sm:px-6 lg:px-8 py-12'>
            <div class = 'bg-white overflow-hidden shadow-sm sm:rounded-lg mb-12'>
                <div class = 'mt-5 md:mt-0 md:col-span-2'>
                    <form @submit.prevent = 'submit'>
                        <div class = 'sm:rounded-md sm:overflow-hidden p-8 text-center'>
                            <label class = 'block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2'>
                                Transaction Hash
                            </label>

                            <input 
                                class = 'appearance-none block w-full bg-gray-100 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
                                type = 'text' id = 'tx-hash' v-bind:value = 'transaction_to_view.headers.tx_hash' v-on:input = 'setToViewTXHash($event)'/>

                            <BreezeButton class = 'py-2 px-4 font-bold rounded-md text-white bg-indigo-600 hover:bg-indigo-800'>
                                Get Details
                            </BreezeButton>
                        </div>
                    </form>
                </div>
            </div>

            <div :class = "{ 'hidden': transaction_not_found }" class = 'bg-white overflow-hidden shadow-sm sm:rounded-lg mb-12'>
                <div class = 'sm:rounded-md sm:overflow-scroll p-8 text-center'>
                    <label class = 'block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2'>
                        Transaction Headers
                    </label>

                    <table class = 'min-w-full border text-left'>
                        <thead>
                            <tr>
                                <th class = 'border px-4'>Candidate Name</th>
                                <th class = 'border px-4'>Votes</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr v-for = '(value, key) in transaction_to_view.tx_details.specified_tx_details.headers'>
                                <td class = 'border p-4'>
                                    {{ key }}
                                </td>
                                <td class = 'border p-4'>
                                    {{ value }}
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    <br/>

                    <label class = 'block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2'>
                        Transaction Details
                    </label>

                    <table class = 'min-w-full border text-left'>
                        <thead>
                            <tr>
                                <th class = 'border px-4'>Candidate Name</th>
                                <th class = 'border px-4'>Votes</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr v-for = '(value, key) in transaction_to_view.tx_details.specified_tx_details.tx_details'>
                                <td class = 'border p-4'>
                                    {{ key }}
                                </td>
                                <td class = 'border p-4'>
                                    {{ value }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div :class = "{ 'hidden': transaction_not_found }" class = 'bg-white overflow-hidden shadow-sm sm:rounded-lg mb-12'>
                <div class = 'mt-5 md:mt-0 md:col-span-2'>
                    <form class = 'w-full' @submit.prevent = 'recalculateHash'>
                        <div class = 'sm:rounded-md sm:overflow-hidden p-8 text-center'>
                            <label class = 'block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2'>
                                Verify transaction integrity and hash
                            </label>

                            <table class = 'min-w-full border text-left'>
                                <tbody>
                                    <tr>
                                        <td class = 'border p-4'>
                                            Original hash
                                        </td>
                                        <td class = 'border p-4'>
                                            {{ transaction_to_view.headers.tx_hash }}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class = 'border p-4'>
                                            Recalculated hash
                                        </td>
                                        <td class = 'border p-4'>
                                            {{ transaction_validity.recalculated_hash }}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>

                            <BreezeButton class = 'py-2 px-4 font-bold rounded-md text-white bg-indigo-600 hover:bg-indigo-800'>
                                Recalculate Hash
                            </BreezeButton>
                        </div>
                    </form>
                </div>
            </div>

            <div :class = "{ 'hidden': transaction_not_found }" class = 'bg-white overflow-hidden shadow-sm sm:rounded-lg mb-12'>
                <div :class = "{ 'hidden': !transaction_is_election }" class = 'mt-5 md:mt-0 md:col-span-2'>
                    <div class = 'sm:rounded-md sm:overflow-hidden p-8'>
                        <label class = 'block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2'>
                            Le results
                        </label>

                        <table class = 'min-w-full border text-left'>
                            <thead>
                                <tr>
                                    <th class = 'border px-4'>Candidate Name</th>
                                    <th class = 'border px-4'>Votes</th>
                                </tr>
                            </thead>

                            <tbody>
                                <tr v-for = '(value, key) in election_results'>
                                    <td class = 'border p-4'>
                                        {{ key }}
                                    </td>
                                    <td class = 'border p-4'>
                                        {{ value }}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div :class = "{ 'hidden': transaction_is_election }" class = 'mt-5 md:mt-0 md:col-span-2'>
                    <form class = 'w-full' @submit.prevent = 'decryptData'>
                        <div class = 'sm:rounded-md sm:overflow-hidden p-8'>
                            <div class = 'flex flex-wrap -mx-3'>
                                <div class = 'w-full md:w-1/2 px-3 md:mb-0'>
                                    <label class = 'block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2'>
                                        Encrypted data
                                    </label>

                                    <input 
                                        class = 'appearance-none block w-full bg-gray-100 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
                                        type = 'text' id = 'tx-hash' v-model = 'decryption.to_decrypt'/>
                                </div>
                                
                                <div class = 'w-full md:w-1/2 px-3'>
                                    <label class = 'block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2'>
                                        Decryption key
                                    </label>

                                    <input 
                                        class = 'appearance-none block w-full bg-gray-100 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
                                        type = 'text' id = 'tx-hash' v-model = 'decryption.decryption_key'/>
                                </div>
                            </div>

                            <div class = 'sm:rounded-md sm:overflow-hidden'>
                                <div class = 'text-center'>
                                    <BreezeButton class = 'font-bold rounded-md text-white bg-indigo-600 hover:bg-indigo-800'>
                                        Decrypt
                                    </BreezeButton>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>

            <div :class = "{ 'hidden': no_decrypted_data }" class = 'bg-white overflow-hidden shadow-sm sm:rounded-lg'>
                <div class = 'sm:rounded-md sm:overflow-scroll p-8'>
                    {{ decryption.decrypted_data }}
                </div>
            </div>
        </div>
    </BreezeAuthenticatedLayout>
</template>
