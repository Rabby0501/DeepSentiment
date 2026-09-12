import axios from 'axios'
import.meta.env.VITE_API_BASE_URL

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

function extractErrorMessage(error) {
  if (error.response && error.response.data && error.response.data.detail) {
    return error.response.data.detail
  }
  if (error.message) return error.message
  return 'An unexpected error occurred.'
}

export async function predictSentiment(text, model) {
  try {
    const { data } = await api.post('/sentiment/predict', { text, model })
    return data
  } catch (error) {
    throw new Error(extractErrorMessage(error))
  }
}

export async function compareSentiment(text) {
  try {
    const { data } = await api.post('/sentiment/compare', { text })
    return data
  } catch (error) {
    throw new Error(extractErrorMessage(error))
  }
}

export async function getSystemModels() {
  try {
    const { data } = await api.get('/system/models')
    return data
  } catch (error) {
    throw new Error(extractErrorMessage(error))
  }
}

export default api
