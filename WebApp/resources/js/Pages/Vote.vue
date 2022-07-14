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
                vote_data: {
                    election: '',
                    candidate: ''
                },
                vote_result: {
                    headers: {
                        timestamp: '',
                        tx_hash: ''
                    },
                    tx_details: {
                        candidate: ''
                    }
                },
                voted: false,
                selected_candidate: false
            }
        },
        props: ['election_data'],
        methods: {
            submit() {
                if (this.vote_data.candidate != '') {
                    axios.post('/api/add_vote', this.vote_data)
                        .then((response) => {
                            if (response.data.tx_details.status == 'approved') {
                                this.voted = true
                                this.vote_result = response.data
                            }
                        })
                        .catch((error) => {
                            console.log(error)
                        })
                }
            },
            convertUnixDateTimeToStandardDateTime(timestamp) {
                return new Date(timestamp).toLocaleString('sv-SE')
            },
            copyToClipboard(value) {
                navigator.clipboard.writeText(value)
            }
        },
        watch: {
            candidate: function(candidate) {
                if (this.vote_data.candidate != '') {
                    this.selected_candidate = true
                }
            }
        },
        mounted() {
            this.vote_data.election = this.election_data.tx_details.specified_tx_details.headers.tx_hash
        }
    }
</script>

<template>
    <Head title = 'Vote' />

    <BreezeAuthenticatedLayout>
        <template #header>
            <h2 class = 'font-semibold text-xl text-gray-800 leading-tight'>
                Vote - {{ election_data.tx_details.specified_tx_details.tx_details.election_details.election_name }}
            </h2>
        </template>

        <div :class = "{ 'hidden': voted }" class = 'max-w-7xl mx-auto sm:px-6 lg:px-8 py-12'>
            <div class = 'bg-white overflow-hidden shadow-sm sm:rounded-lg'>
                <div class = 'mt-5 md:mt-0 md:col-span-2'>
                    <form @submit.prevent = 'submit'>
                        <div class = 'sm:rounded-md sm:overflow-hidden p-8'>
                            <div class = 'grid grid-cols-2'>
                                <div class = 'mx-auto block p-6 max-w-sm bg-white rounded-lg border border-gray-200 shadow-md dark:bg-gray-800 dark:border-gray-700 w-2/4 text-center'>
                                    <img src = '/images/apu-apustaja-screaming.jpg' class = 'w-full'>
                                    <div class = 'px-6 py-4'>
                                        <input type = 'radio' id = 'candidate-one' :value = 'election_data.tx_details.specified_tx_details.tx_details.election_details.candidates[0]' v-model = 'vote_data.candidate'/>
                                        <label class = 'ml-2' for = 'candidate-one'>
                                            {{ election_data.tx_details.specified_tx_details.tx_details.election_details.candidates[0] }}
                                        </label>
                                    </div>
                                </div>

                                <div class = 'mx-auto block p-6 max-w-sm bg-white rounded-lg border border-gray-200 shadow-md dark:bg-gray-800 dark:border-gray-700 w-2/4 text-center'>
                                    <img src = '/images/kry-kat.jpg' class = 'w-full'>
                                    <div class = 'px-6 py-4'>
                                        <input type = 'radio' id = 'candidate-two' :value = 'election_data.tx_details.specified_tx_details.tx_details.election_details.candidates[1]' v-model = 'vote_data.candidate'/>
                                        <label class = 'ml-2' for = 'candidate-two'>
                                            {{ election_data.tx_details.specified_tx_details.tx_details.election_details.candidates[1] }}
                                        </label>
                                    </div>
                                </div>
                            </div>

                            <div class = 'py-4 text-center'>
                                <h2 :class = "{ 'hidden': !selected_candidate }" class = 'font-semibold text-xl text-gray-800'>
                                    Selected candidate: {{ vote_data.candidate }}
                                </h2>

                                <br/>

                                <BreezeButton class = 'py-2 px-4 font-bold rounded-md text-white bg-indigo-600 hover:bg-indigo-800'>
                                    Vote
                                </BreezeButton>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <div :class = "{ 'hidden': !voted }" class = 'max-w-7xl mx-auto sm:px-6 lg:px-8 py-12'>
            <div class = 'bg-white overflow-hidden shadow-sm sm:rounded-lg'>
                <div class = 'px-6 py-4 text-center'>
                    <br/>
                    <hr/>
                    <br/>

                    <h2 class = 'font-semibold text-xl text-gray-800'>
                        Thank you for your vote
                    </h2>

                    <br/>
                    <hr/>
                    <br/>

                    <p>
                        Your vote has been received, you voted for: {{ vote_result.tx_details.candidate }}.
                        <br/>
                        Your vote was received at: {{ convertUnixDateTimeToStandardDateTime(vote_result.headers.timestamp) }}
                        <br/><br/>
                        Your vote transaction ID is: 
                        <br/>
                        {{ vote_result.headers.tx_hash }}

                        <button @click = "copyToClipboard(vote_result.headers.tx_hash)">
                            <img class = 'inline max-h-5' src = '/icons/copy-to-clipboard.png'/>
                            Copy
                        </button> 

                        <br/><br/>

                        Click 
                        <a class = 'font-semibold text-indigo-800' v-bind:href = "'/transaction_viewer?txid=' + vote_result.headers.tx_hash">
                            here
                        </a>
                        to view your vote.
                    </p>

                    <br/>
                </div>
            </div>
        </div>
    </BreezeAuthenticatedLayout>
</template>
