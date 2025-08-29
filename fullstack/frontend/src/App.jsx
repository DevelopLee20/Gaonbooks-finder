import { useState } from 'react'
import BookCard from './components/BookCard'
import './App.css'

function App() {
  const [searchQuery, setSearchQuery] = useState('')
  const [books, setBooks] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const searchBooks = async (query) => {
    if (!query.trim()) {
      setError('검색어를 입력하세요.')
      return
    }

    setIsLoading(true)
    setError('')
    
    try {
      const apiUrl = `/api/find/${encodeURIComponent(query)}/`
      const response = await fetch(apiUrl)
      
      if (!response.ok) {
        throw new Error('검색 중 오류가 발생했습니다.')
      }
      
      const booksData = await response.json()
      setBooks(booksData)
    } catch (err) {
      console.error('검색 오류:', err)
      setError('검색 중 오류가 발생했습니다.')
      setBooks([])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSearch = () => {
    searchBooks(searchQuery)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>가온북스 도서 검색</h1>
      </header>

      <div className="search-container">
        <div className="search-wrapper">
          <input
            type="text"
            className="search-input"
            placeholder="책 제목을 입력하세요"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button 
            className="search-button"
            onClick={handleSearch}
            disabled={isLoading}
          >
            {isLoading ? '검색 중...' : '검색'}
          </button>
        </div>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <div className="results">
        {isLoading ? (
          <p className="loading">검색 중...</p>
        ) : books.length === 0 && !error ? (
          <p className="no-results">검색 결과가 없습니다.</p>
        ) : (
          <div className="books-grid">
            {books.map((book, index) => (
              <BookCard key={index} book={book} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default App
