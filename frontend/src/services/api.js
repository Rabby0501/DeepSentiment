import axios from 'axios'

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

function extractErrorMessage(error) {
  if (error.response?.data?.detail) {
    return error.response.data.detail
  }

  if (error.message) {
    return error.message
  }

  return 'An unexpected error occurred.'
}

export async function predictSentiment(text, model) {
  try {
    const { data } = await api.post('/sentiment/predict', {
      text,
      model
    })
    return data
  } catch (error) {
    throw new Error(extractErrorMessage(error))
  }
}

export async function compareSentiment(text) {
  try {
    const { data } = await api.post('/sentiment/compare', {
      text
    })
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