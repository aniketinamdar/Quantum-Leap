import React, { useState } from 'react'
import axios from 'axios'

function App() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    setFile(selectedFile)
    setPreview(URL.createObjectURL(selectedFile))
    setPrediction(null)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) return
  
    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)
  
    try {
      const response = await axios.post('http://localhost:5000/predict', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      console.log('Response from server:', response.data)
      setPrediction(response.data)
    } catch (error) {
      console.error('Error predicting image:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      <div className="relative py-3 sm:max-w-xl sm:mx-auto">
        <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
          <div className="max-w-md mx-auto">
            <div className="divide-y divide-gray-200">
              <div className="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
                <h2 className="text-2xl font-bold mb-4">Image Classifier</h2>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Upload Image
                    </label>
                    <input
                      type="file"
                      onChange={handleFileChange}
                      accept="image/*"
                      className="mt-1 block w-full text-sm text-gray-500
                        file:mr-4 file:py-2 file:px-4
                        file:rounded-full file:border-0
                        file:text-sm file:font-semibold
                        file:bg-blue-50 file:text-blue-700
                        hover:file:bg-blue-100"
                    />
                  </div>
                  {preview && (
                    <img src={preview} alt="Preview" className="mt-4 max-w-full h-auto" />
                  )}
                  <button
                    type="submit"
                    disabled={!file || loading}
                    className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                  >
                    {loading ? 'Predicting...' : 'Predict'}
                  </button>
                </form>
              </div>
              {prediction && (
  <div className="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
    <h3 className="text-xl font-bold">Prediction Result:</h3>
    <p>Predicted Class: {prediction.predicted_class}</p>
    <p>Class Probabilities:</p>
    <ul>
      {prediction.class_probabilities.map((prob, index) => (
        <li key={index}>Class {index}: {(prob * 100).toFixed(2)}%</li>
      ))}
    </ul>
  </div>
)}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App