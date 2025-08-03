import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

const endpoint: string = import.meta.env.VITE_API_ENDPOINT;

export const useExchangeStore = defineStore('exchange', () => {
  const cad_jpy = ref(0)
  const load = () => {
    axios.get(`${endpoint}/exchange`)
      .then((response) => {
        cad_jpy.value = response.data.ask
      })
      .catch((error) => {
        console.log(error);
      })
  }

  return { cad_jpy, load }
})
