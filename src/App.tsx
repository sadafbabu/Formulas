import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { FormulaDetailPage } from './pages/FormulaDetailPage'
import { SampleBookPage } from './pages/SampleBookPage'

export default function App() {
  return (
    <BrowserRouter basename="/Formulas">
      <Routes>
        <Route path="/" element={<SampleBookPage />} />
        <Route path="/formula/:id" element={<FormulaDetailPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
