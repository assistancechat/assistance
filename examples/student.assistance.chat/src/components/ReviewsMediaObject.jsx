import Image from 'next/image'

export default function ReviewsMediaObject(props) {
  return (
    <div className='flex'>
        <div className='flex space-x-3 items-center self-center mb-2 flex-shrink-0 lg:space-x-12'>
          <div className='flex rounded-md justify-center border-2 border-orange-200 sm:w-1/6'>
            <Image src={props.src} alt='feedback.png' className="w-12 rounded-md lg:w-36"/>
          </div>
          <div className='flex flex-col max-w-xs'>
            <h4 className='text-sm italic self-start leading-none lg:text-md'>{props.title}</h4>
            <h3 className='text-lg font-bold lg:text-xl'>{props.headline}</h3>
            <p className='text-xs mt-1 max-w-xs lg:max-w-xl lg:text-md lg:w-3/4 lg:w-full '>{props.quote}</p>
          </div>
      </div>
    </div>
  )
}
