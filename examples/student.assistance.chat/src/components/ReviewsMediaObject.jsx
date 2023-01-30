import Image from 'next/image'

export default function ReviewsMediaObject(props) {
  return (
    <div className='flex'>
        <div className='flex flex-wrap space-x-3 items-center self-center mb-4 flex-shrink-0 sm:mb-0 sm:mr-4 lg:space-x-12'>
          <div className='rounded-md justify-center border-2 border-orange-200'>
            <Image src={props.src} alt='feedback.png' className="w-24 rounded-md lg:w-36"/>
          </div>
          <div className='w-2/5'>
            <h3 className='text-md italic self-center leading-none lg:text-md'>{props.title}</h3>
            <h4 className='text-xl font-bold lg:text-xl'>{props.headline}</h4>
            <p className='text-xs mt-1 w-7/12 lg:text-md lg:w-3/4'>{props.quote}</p>
          </div>
      </div>
    </div>
  )
}
