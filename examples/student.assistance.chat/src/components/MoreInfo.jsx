import { AcademicCapIcon, ArrowDownCircleIcon } from '@heroicons/react/24/solid'
import { ChatBubbleOvalLeftEllipsisIcon } from '@heroicons/react/24/outline'

const moreInfoData = {
  blurb1:'It’s time to align your faith with your future.',
  blurb2:'The courses at Alphacrucis are designed to provide you with an unique Christian experience. ',
  blurb3: 'We offer a range of courses that will help you to grow in your faith and develop your skills.',
  video: {
    link: 'https://www.youtube.com/embed/wds7y_0rix4?',
    title: 'Thank you'
  },
  LearnButton: {
    text: 'Alphacrucis counselling at a glance',
    link: 'https://www.ac.edu.au/healthbrochure'
  },
  ChatButton1: {
    text: 'Do I qualify for FEE-HELP?',
    link: '#Chat'
  },
  ChatButton2: {
    text: "What's the best course for me?",
    link: '#Chat'
}
}

export default function MoreInfo() {
  return (
    <>
      <div
        id='MoreInfo'
        className='relative w-screen bg-gray-200 pt-20 lg:h-screen lg:justify-center '
      >
        <div className='flex flex-wrap place-items-evenly h-full lg:items-center lg:justify-items-end'>
          <div className='grid grid-rows-6 w-full h-1/2 lg:w-1/2 lg:h-full lg:place-self-start space-y-4 '>
            <div className='w-8/12 row-span-3 space-y-4 place-self-center lg:w-8/12 lg:space-y-8'>
              <h3 className='text-xl tracking-wide lg:text-2xl lg:tracking-wider'>
                {moreInfoData.blurb1}
              </h3>
              <h3 className='text-xl tracking-wide lg:text-2xl lg:tracking-wider'>
                {moreInfoData.blurb2}
              </h3>
              <h3 className='text-xl tracking-wide lg:text-2xl lg:tracking-wider'>
                {moreInfoData.blurb3}
              </h3>
            </div>
            <button
              type='button'
              className='animate-pulse relative h-4/6 w-4/6 place-self-center place-content-evenly self-end items-center rounded-md border border-transparent shadow-sm hover:bg-white focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 lg:justify-self-center lg:h-1/2'
            >
              <a
                href={moreInfoData.ChatButton1.link}
                rel='noreferrer'
                target='_blank'
                className='inline-flex h-max w-max space-x-2'
              >
                <ChatBubbleOvalLeftEllipsisIcon className='w-10 h-10 self-center text-orange-600' />
                <h3 className='self-center leading-none text-black text-sm uppercase'>
                 {moreInfoData.ChatButton1.text}
                </h3>
              </a>
            </button>
          </div>
          <div className='grid grid-rows-6 mb-20 -mt-30 w-full lg:w-1/2 lg:h-full lg:mt-0 lg:mb-0'>
            <iframe
              className='w-full row-span-4 h-full p-6'
              src={moreInfoData.video.link}
              title={moreInfoData.video.title}
              frameBorder='0'
              allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share'
              allowFullScreen
            ></iframe>

            <div className='row-span-1 relative'>
              <div className='grid grid-rows-2 space-y-2'>
                <h2 className='row-span-1 text-3xl w-4/5 p-2 ml-5 self-center border-orange-600'>
                  More Information
                </h2>
                <div className='animate-pulse row-span-1 place-content-around flex justify-self-center space-x-1'>
                  <button
                    type='button'
                    className='relative inline-flex items-center rounded-md border border-transparent w-5/12 px-4 shadow-sm hover:bg-white focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2'
                  >
                    <a
                      href={moreInfoData.ChatButton2.link}
                      rel='noreferrer'
                      target='_blank'
                      className='inline-flex space-x-2'
                    >
                      <ChatBubbleOvalLeftEllipsisIcon className='h-10 self-center text-orange-600' />
                      <h3 className='self-center text-left leading-none text-black text-sm uppercase'>
                        {moreInfoData.ChatButton2.text}
                      </h3>
                    </a>
                  </button>
                  <button
                    type='button'
                    className='relative inline-flex items-center rounded-md border border-transparent w-5/12 px-4 shadow-sm hover:bg-white focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2'
                  >
                    {' '}
                    <a
                      href={moreInfoData.LearnButton.link}
                      rel='noreferrer'
                      target='_blank'
                      className='inline-flex space-x-2'
                    >
                      <AcademicCapIcon className='w-10 h-10 self-center text-orange-600' />
                      <h3 className='self-center text-left leading-none text-black text-sm uppercase'>
                        {moreInfoData.LearnButton.text}
                      </h3>
                    </a>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
