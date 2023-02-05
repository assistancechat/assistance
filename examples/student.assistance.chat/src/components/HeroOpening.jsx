import { React, useState, useEffect, useRef } from 'react'
import { ArrowDownCircleIcon } from '@heroicons/react/24/solid'
import StartChatWithQuestionButton from '@/components/atoms/StartChatWithQuestionButton'
import Typed from 'typed.js'

export default function HeroOpening(props) {

  var headline = {
    strings: [
      "Discover God's Purpose for you in <u>Ministry</u>",
      "Discover God's Purpose for you in <u>Counselling </u>",
      "Discover God's Purpose for you in <u>Education</u>",
      "Discover God's Purpose for you in <u>Business</u>",
      "Discover God's Purpose for your <u>Career</u>"
    ],
    typeSpeed: 50,
    backSpeed: 25,
    backDelay: 1200,
    loop: true,
    loopCount: 1,
    showCursor: false,
    bindInputFocusEvents: true,
  }

  const element = useRef(null)
  const [typed, setTyped] = useState(null)

  useEffect(() => {
    const typed = new Typed(element.current, headline)
    setTyped(typed)
    return () => {
      typed.destroy()
    }
  }, [])

var subHeading = {
  strings: [
    "Talk with our customer experience officer now to find the right course for you",
  ],
  typeSpeed: 20,
  backDelay: 1150,
  startDelay: 14000,
  loop: true,
  loopCount: 1,
  showCursor: false,
}

const element2 = useRef(null)
const [typed2, setTyped2] = useState(null)

useEffect(() => {
  const typed2 = new Typed(element2.current, subHeading)
  setTyped2(typed2)
  return () => {
    typed2.destroy()
  }
}, [])


  return (
    <div className='w-screen h-screen'>
      <img
        className='absolute opacity-30 -z-10 w-screen h-screen lg:hidden'
        src={props.portraitPicture}
        alt={props.alt}
      />
      <img
        className='absolute opacity-30 -z-10 w-screen h-screen hidden lg:block'
        src={props.landscapePicture}
        alt={props.alt}
      />
      <div className='grid grid-rows-6 w-screen h-screen'>
        <button
          type='button'
          className='row-span-2 left-10 top-40 bg-orange-400 md:top-30 h-12 w-3/4 relative inline-flex items-center rounded-md border border-transparent px-4 py-2 shadow-sm hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 lg:w-1/4'
        >
          <a
            href={props.learnButtonLink}
            rel='noreferrer'
            target='_blank'
            className='inline-flex h-max w-max space-x-2'
          >
            <ArrowDownCircleIcon className='h-10 w-10 self-center text-white' />
            <h3 className='text-base font-medium text-white leading-none uppercase place-self-center '>
              {props.learnButtonText}
            </h3>
          </a>
        </button>
        <div className='space-y-6'>
          <div className='row-span-4 relative left-5 sm:left-10 w-4/5 space-y-4 '>
            <h1
              className='pt-4 text-5xl tracking-normalleading-none border-orange-400 border-t-4'
              ref={element}
            />
            <h3 className='text-xl w-4/5 tracking-wide leading-tight font-light text-gray-800' ref={element2} />
          </div>

          <StartChatWithQuestionButton
            question={props.ChatButtonText}
            buttonClassName='row-span-1 relative bg-orange-400 inset-10 inline-flex w-5/6 rounded-md py-1 px-4 shadow-sm hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 lg:w-1/3 lg:justify-self-end lf:mt-10 space-x-4'
            bubbleClassName='-ml-1 self-center text-white h-12 w-12'
            textClassName='text-base font-medium text-white uppercase leading-none text-left place-self-center'
          />
        </div>

        <div></div>
      </div>
    </div>
  )
}
