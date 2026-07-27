import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { FormulaDetailPage } from './pages/FormulaDetailPage'
import { SampleBookPage } from './pages/SampleBookPage'

const basename = import.meta.env.BASE_URL.replace(/\/$/, '')

export default function App() {
  return (
    <BrowserRouter basename={basename || undefined}>
      <Routes>
        <Route path="/" element={<SampleBookPage />} />
        <Route path="/formula/:id" element={<FormulaDetailPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
