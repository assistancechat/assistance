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
      "Discover God's Purpose for your <u>Life</u>"
    ],
    typeSpeed: 10,
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
    "We will help you find the right course and connect you to your purpose",
  ],
  typeSpeed: 20,
  backDelay: 1350,
  startDelay: 9200,
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
        className='absolute opacity-30 -z-10 w-screen h-screen md:hidden'
        src={props.portraitPicture}
        alt={props.alt}
      />
      <img
        className='absolute opacity-30 -z-10 w-screen h-screen hidden md:block'
        src={props.landscapePicture}
        alt={props.alt}
      />
      <div className='grid grid-rows-6 w-screen h-screen'>
       <div className="row-span-1 lg:row-span-2"></div>
        <div className='space-y-6 w-screen'>
          <div className='row-span-4 relative w-screen space-y-4 '>
            <hr className="border-orange-400 border-2 w-10/12 ml-10" />
            <h1
              className='text-5xl pl-10 tracking-normal leading-none'
              ref={element}
            />
            <h3 className='text-xl pl-10 pr-10 tracking-wide leading-tight font-light text-gray-800 w-screen' ref={element2} />
          </div>

          <StartChatWithQuestionButton
            question={props.ChatButtonText}
            buttonClassName='row-span-1 inset-10 relative bg-orange-400 inline-flex w-9/12 rounded-md py-1 px-4 shadow-sm hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 lg:w-1/3 lg:justify-self-end space-x-4'
            bubbleClassName='-ml-1 self-center text-white h-12 w-12'
            textClassName='text-sm font-medium text-white uppercase leading-none text-left place-self-center'
          />
        </div>

        <div className='w-screen'></div>
      </div>
    </div>
  )
}
