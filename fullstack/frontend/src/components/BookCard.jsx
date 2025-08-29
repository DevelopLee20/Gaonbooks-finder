import React from 'react'

const BookCard = ({ book }) => {
  const getTitleImg = (title) => {
    return '/assets/mas.png'
  }

  const getLocationText = (location) => {
    if (location === -1) {
      return '품절'
    }
    return `위치: ${location}`
  }

  const getLocationClass = (location) => {
    if (location === -1) {
      return 'book-location soldout'
    }
    return 'book-location available'
  }

  return (
    <div className="book">
      <img 
        src={getTitleImg(book.도서명)} 
        alt="표지 이미지"
        className="book-cover"
        onError={(e) => {
          e.target.style.display = 'none'
        }}
      />
      <div className="book-info">
        <div className="book-title">{book.도서명}</div>
        <div className="book-publisher">{book.출판사}</div>
        <div className={getLocationClass(book.위치)}>
          {getLocationText(book.위치)}
        </div>
        {book.주문경과일 && (
          <div className="book-order-date">{book.주문경과일}</div>
        )}
      </div>
    </div>
  )
}

export default BookCard
