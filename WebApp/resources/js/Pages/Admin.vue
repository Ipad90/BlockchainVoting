<script setup>
    import BreezeAuthenticatedLayout from '@/Layouts/Authenticated.vue'
    import BreezeButton from '@/Components/Button.vue'
    import BreezeInput from '@/Components/Input.vue'
    import BreezeLabel from '@/Components/Label.vue'
    import { Head } from '@inertiajs/inertia-vue3'
</script>

<script>
    export default {
        data() {
            return {
                election_data: {
                    election_name: '',
                    candidates: [],
                    start_timestamp: '',
                    end_timestamp: ''
                },
                created_election: {
                    headers: {
                        tx_hash: '68319757087a0a9450a4cecbadb7398f8060c3dab018803d43ff2426f053d48c'
                    }
                },
                election_created: false
            }
        },
        methods: {
            submit() {
                this.election_data.start_timestamp = this.convertStandardDatetimeToUnixDateTime(this.election_data.start_timestamp)
                this.election_data.end_timestamp = this.convertStandardDatetimeToUnixDateTime(this.election_data.end_timestamp)

                if (this.checkInputs()) {
                    axios.post('/api/add_election', this.election_data)
                        .then((response) => {
                            if (response.data.tx_details.status == 'approved') {
                                this.election_created = true
                                this.created_election = response.data
                            }
                        }).catch((error) => {
                            console.log(error)
                        })
                }
            },
            checkInputs() {
                let input_conditions = [
                    this.election_data.election_name != '',
                    this.election_data.candidates.length > 1,
                    this.election_data.start_timestamp != '',
                    this.election_data.end_timestamp != ''
                ]

                return input_conditions.every(Boolean)
            },
            convertStandardDatetimeToUnixDateTime(timestamp) {
                return Date.parse(timestamp) / 1000
            },
            copyToClipboard(value) {
                navigator.clipboard.writeText(value)
            }
        }
    }
</script>

<template>
    <Head title = 'Admin' />

    <BreezeAuthenticatedLayout>
        <template #header>
            <h2 class = 'font-semibold text-xl text-gray-800 leading-tight'>
                Admin
            </h2>
        </template>

        <div :class = "{ 'hidden': election_created }" class = 'max-w-7xl mx-auto sm:px-6 lg:px-8 py-12'>
            <div class = 'bg-white overflow-hidden shadow-sm sm:rounded-lg'>
                <div class = 'mt-5 md:mt-0 md:col-span-2'>
                    <form class = 'w-full' @submit.prevent = 'submit'>
                        <div class = 'sm:rounded-md sm:overflow-hidden p-8'>
                            <div class = 'flex flex-wrap -mx-3 mb-6'>
                                <div class = 'w-full px-3'>
                                    <label class = 'block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2'>
                                        Election Name
                                    </label>
                                    <input 
                                        class = 'appearance-none block w-full bg-gray-100 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
                                        id = 'election_name' type = 'text' placeholder = 'ELECTION NAME' v-model = 'election_data.election_name'>
                                </div>
                            </div>

                            <div class = 'flex flex-wrap -mx-3 mb-6'>
                                <div class = 'w-full md:w-1/2 px-3 mb-6 md:mb-0'>
                                    <label class = 'block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2'>
                                        Candidate 1's name
                                    </label>
                                    <!-- Change border-gray-200 to border-red-500 for error -->
                                    <input 
                                        class = 'appearance-none block w-full bg-gray-100 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white' 
                                        id = 'candidate_1' type = 'text' placeholder = 'CANDIDATE 1' v-model = 'election_data.candidates[0]'>
                                    <!-- Error text -->
                                    <p class = 'hidden text-red-500 text-xs italic'>
                                        Please fill out this field.
                                    </p>
                                </div>

                                <div class = 'w-full md:w-1/2 px-3'>
                                    <label class = 'block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2'>
                                        Candidate 2's name
                                    </label>
                                    <input 
                                        class = 'appearance-none block w-full bg-gray-100 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500' 
                                        id = 'candidate_2' type = 'text' placeholder = 'CANDIDATE 2' v-model = 'election_data.candidates[1]'>
                                </div>
                            </div>

                            <div class = 'flex flex-wrap -mx-3 mb-6'>
                                <div class = 'w-full md:w-1/2 px-3 mb-6 md:mb-0'>
                                    <label class = 'block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2'>
                                        Start date
                                    </label>
                                    <input 
                                        class = 'appearance-none block w-full bg-gray-100 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
                                        id = 'start_timestamp' type = 'datetime-local' v-model = 'election_data.start_timestamp'>
                                </div>

                                <div class = 'w-full md:w-1/2 px-3'>
                                    <label class = 'block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2'>
                                        End date
                                    </label>
                                    <input 
                                        class = 'appearance-none block w-full bg-gray-100 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500' 
                                        id = 'end_timestamp' type = 'datetime-local' v-model = 'election_data.end_timestamp'>
                                </div>
                            </div>

                            <div class = 'sm:rounded-md sm:overflow-hidden text-center'>
                                <BreezeButton class = 'font-bold rounded-md text-white bg-indigo-600 hover:bg-indigo-800'>
                                    Create Election
                                </BreezeButton>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <div :class = "{ 'hidden': !election_created }" class = 'max-w-7xl mx-auto sm:px-6 lg:px-8 py-12'>
            <div class = 'bg-white overflow-hidden shadow-sm sm:rounded-lg'>
                <div class = 'px-6 text-center mt-6'>
                    <h2 class = 'font-semibold text-xl text-gray-800'>
                        Election successfully created
                    </h2>

                    <br/>

                    <label class = 'block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2'>
                        Election Details
                    </label>

                    <table class = 'min-w-full border text-left'>
                        <tbody>
                            <tr>
                                <td class = 'border p-4'>
                                    Election TXID
                                </td>

                                <td class = 'border p-4'>
                                    <a v-bind:href = "'/transaction_viewer?txid=' + created_election.headers.tx_hash">
                                        {{ created_election['headers']['tx_hash'] }}
                                    </a>
                                </td>

                                <td class = 'border p-4'>
                                    <button @click = "copyToClipboard(created_election.headers.tx_hash)">
                                        <img class = 'inline max-h-5' src = '/icons/copy-to-clipboard.png'/>
                                        Copy
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    <br/>

                    <a :v-bindhref = "'/vote/' + created_election.headers.tx_hash">
                        <BreezeButton class = 'font-bold rounded-md text-white bg-indigo-600 hover:bg-indigo-800 mb-6'>
                            Vote
                        </BreezeButton>
                    </a>
                </div>
            </div>
        </div>
    </BreezeAuthenticatedLayout>
</template>
