import { useEffect, useMemo, useRef, useState } from 'react'
import clsx from 'clsx'
import {
  useInView
} from 'framer-motion'

import { Container } from '@/components/Container'

const reviews = [{
  title: 'Great service',
  body: 'The enrollment process was quick and easy, and the staff was incredibly friendly and helpful. I highly recommend this service to anyone looking to enroll in a Christian university.',
  author: 'Seng Yang',
  rating: 5
  },
  {
  title: 'Smooth process',
  body: 'I was impressed with how efficient and smooth the enrollment process was. The staff was very friendly and answered all of my questions. I would definitely use this service again.',
  author: 'Rohit',
  rating: 4
  },
  {
  title: 'Excellent help',
  body: 'I had a great experience with this enrollment service. The staff was extremely helpful and made the process quick and easy. I highly recommend it to anyone looking to enroll in a Christian university.',
  author: 'Mark Tyde',
  rating: 5
  },
  {
  title: 'Easy enrollment',
  body: 'The enrollment process was a breeze thanks to the helpful staff. They were able to answer all of my questions and get me enrolled in no time. I am very happy with this service.',
  author: 'Amy',
  rating: 4
  },
  {
  title: 'Friendly staff',
  body: 'I was very impressed with the friendly and helpful staff. They made the enrollment process quick and easy. I would definitely recommend this service to anyone looking to enroll in a Christian university.',
  author: 'Brian',
  rating: 5
  },
  {
  title: 'Great experience',
  body: 'I had a great experience with this enrollment service. The staff was very friendly and helpful, and the process was quick and efficient. I would definitely use this service again.',
  author: 'Emily Davis',
  rating: 4
  },
  {
  title: 'Efficient service',
  body: 'I was very pleased with how efficient and quick the enrollment process was. The staff was also very helpful and friendly. I would highly recommend this service to anyone looking to enroll in a Christian university.',
  author: 'Mike',
  rating: 5
  },
  {
  title: 'Helpful staff',
  body: 'The staff was incredibly helpful and made the enrollment process very easy. I am very happy with this service and would recommend it to anyone looking to enroll in a Christian university.',
  author: 'Jessica Garcia',
  rating: 4
  },
  {
  title: 'Quick and easy',
  body: 'The enrollment process was quick and easy thanks to the helpful staff. They were able to answer all of my questions and get me enrolled in no time. I would definitely use this service again.',
  author: 'Dave',
  rating: 5
  },
  {
  title: 'Highly recommend',
  body: 'I had a great experience with this enrollment service. The staff was friendly and helpful, and the process was quick and efficient. I highly recommend it to anyone looking to enroll in a Christian university.',
  author: 'Sam',
  rating: 4
  },

]

function StarIcon(props) {
  return (
    <svg viewBox="0 0 20 20" aria-hidden="true" {...props}>
      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
    </svg>
  )
}

function StarRating({ rating }) {
  return (
    <div className="flex">
      {[...Array(5).keys()].map((index) => (
        <StarIcon
          key={index}
          className={clsx(
            'h-5 w-5',
            rating > index ? 'fill-cyan-500' : 'fill-gray-300'
          )}
        />
      ))}
    </div>
  )
}

function Review({ title, body, author, rating, className, ...props }) {
  let animationDelay = useMemo(() => {
    let possibleAnimationDelays = ['0s', '0.1s', '0.2s', '0.3s', '0.4s', '0.5s']
    return possibleAnimationDelays[
      Math.floor(Math.random() * possibleAnimationDelays.length)
    ]
  }, [])

  return (
    <figure
      className={clsx(
        'animate-fade-in rounded-3xl bg-white p-6 opacity-0 shadow-md shadow-gray-900/5',
        className
      )}
      style={{ animationDelay }}
      {...props}
    >
      <blockquote className="text-gray-900">
        <StarRating rating={rating} />
        <p className="mt-4 text-lg font-semibold leading-6 before:content-['“'] after:content-['”']">
          {title}
        </p>
        <p className="mt-3 text-base leading-7">{body}</p>
      </blockquote>
      <figcaption className="mt-3 text-sm text-gray-600 before:content-['–_']">
        {author}
      </figcaption>
    </figure>
  )
}

function splitArray(array, numParts) {
  let result = []
  for (let i = 0; i < array.length; i++) {
    let index = i % numParts
    if (!result[index]) {
      result[index] = []
    }
    result[index].push(array[i])
  }
  return result
}

function ReviewColumn({
  className,
  reviews,
  reviewClassName = () => {},
  msPerPixel = 0,
}) {
  let columnRef = useRef()
  let [columnHeight, setColumnHeight] = useState(0)
  let duration = `${columnHeight * msPerPixel}ms`

  useEffect(() => {
    let resizeObserver = new window.ResizeObserver(() => {
      setColumnHeight(columnRef.current.offsetHeight)
    })

    resizeObserver.observe(columnRef.current)

    return () => {
      resizeObserver.disconnect()
    }
  }, [])

  return (
    <div
      ref={columnRef}
      className={clsx('animate-marquee space-y-8 py-4', className)}
      style={{ '--marquee-duration': duration }}
    >
      {reviews.concat(reviews).map((review, reviewIndex) => (
        <Review
          key={reviewIndex}
          aria-hidden={reviewIndex >= reviews.length}
          className={reviewClassName(reviewIndex % reviews.length)}
          {...review}
        />
      ))}
    </div>
  )
}

function ReviewGrid() {
  let containerRef = useRef()
  let isInView = useInView(containerRef, { once: true, amount: 0.4 })
  let columns = splitArray(reviews, 3)
  columns = [columns[0], columns[1], splitArray(columns[2], 2)]

  return (
    <div
      ref={containerRef}
      className="relative -mx-4 mt-16 grid h-[49rem] max-h-[150vh] grid-cols-1 items-start gap-8 overflow-hidden px-4 sm:mt-20 md:grid-cols-2 lg:grid-cols-3"
    >
      {isInView && (
        <>
          <ReviewColumn
            reviews={[...columns[0], ...columns[2].flat(), ...columns[1]]}
            reviewClassName={(reviewIndex) =>
              clsx(
                reviewIndex >= columns[0].length + columns[2][0].length &&
                  'md:hidden',
                reviewIndex >= columns[0].length && 'lg:hidden'
              )
            }
            msPerPixel={10}
          />
          <ReviewColumn
            reviews={[...columns[1], ...columns[2][1]]}
            className="hidden md:block"
            reviewClassName={(reviewIndex) =>
              reviewIndex >= columns[1].length && 'lg:hidden'
            }
            msPerPixel={15}
          />
          <ReviewColumn
            reviews={columns[2].flat()}
            className="hidden lg:block"
            msPerPixel={10}
          />
        </>
      )}
      <div className="pointer-events-none absolute inset-x-0 top-0 h-32 bg-gradient-to-b from-gray-50" />
      <div className="pointer-events-none absolute inset-x-0 bottom-0 h-32 bg-gradient-to-t from-gray-50" />
    </div>
  )
}

export function Reviews() {
  return (
    <section
      id="reviews"
      aria-labelledby="reviews-title"
      className="pt-20 pb-16 sm:pt-32 sm:pb-24"
    >
      <Container>
        <h2
          id="reviews-title"
          className="text-3xl font-medium tracking-tight text-gray-900 sm:text-center"
        >
          What People Are Saying
        </h2>
        <p className="mt-2 text-lg text-gray-600 sm:text-center">
        </p>
        <ReviewGrid />
      </Container>
    </section>
  )
}
