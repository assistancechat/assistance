import StartChatWithQuestionButton from '@/components/atoms/StartChatWithQuestionButton'

import CounsellingProfile1 from '../images/counselling-profile-1.png'
import CounsellingProfile2 from '../images/counselling-profile-2.png'
import CounsellingProfile3 from '../images/counselling-profile-3.png'

export default function Reviews(props) {
  return (
    <div className='bg-gray-800' id="Reviews" key={props.id}>
      <div className='mx-auto max-w-2xl py-16 px-4 justify-items-center sm:py-24 sm:px-6 lg:grid lg:max-w-7xl lg:grid-cols-12 lg:gap-x-8 lg:py-32 lg:px-8'>
        <div className='lg:col-span-5 p-5'>
          <div className='bg-orange-400 rounded-lg'>
            <div className='mx-auto max-w-7xl py-10 px-6 border-2 rounded-lg sm:py-5 lg:px-4'>
              <div className='mx-auto max-w-4xl text-center space-y-2'>
                <h2 className='pt-4 pb-2 text-5xl  text-gray-800 tracking-normal leading-none border-white text-left border-b-4 border-w-2/3'>
                  {props.careerSnapshot}
                </h2>
                <p className='text-md text-left font-light uppercase text-gray-800'>
                  {props.careerSlogan}
                </p>
              </div>
              <dl className='mt-10 text-center space-y-4'>
                {props.sidePanel.map((panel) => (
                  <>
                    <div
                      key={panel.id}
                      className='flex border-white border-2 flex-col'
                    >
                      <dd className='order-1 text-5xl font-bold tracking-tight text-white'>
                        {panel.headline}
                      </dd>
                      <dt className=' order-2 mt-2 text-lg font-light leading-6 text-gray-800 '>
                        {panel.subheading}
                      </dt>
                    </div>
                  </>
                ))}
              </dl>
            </div>
          </div>
        </div>

        <div className='mt-16 lg:col-span-7 lg:col-start-6 lg:mt-0'>
          <h3 className='sr-only'>Student Reviews</h3>

          <div className='flow-root'>
            <div className='flex flex-wrap items-center divide-gray-200 space-y-2 p-4'>
              {props.featured.map((review) => (
                <div
                  key={review.id}
                  className='p-6 bg-gray-300 hover:bg-orange-200 shadow border-gray-400 rounded-md'
                >
                  <div className='flex items-center'>
                    <img
                      src={review.avatarSrc}
                      alt={`${review.author}.`}
                      className='h-14 w-14 rounded-full'
                    />
                    <div className='ml-4'>
                      <h4 className='text-lg font-light text-gray-800 leading-tight tracking-wide uppercase'>
                        {review.action}
                      </h4>
                      <h3 className='text-2xl font-bold tracking-wide leading-none text-gray-800 capitalize'>
                        {review.reason}
                      </h3>
                      <div className='mt-1 flex items-center'></div>
                    </div>
                  </div>
                  <div className='mt-2 space-y-2'>
                  <p className='text-xs p-2 font-light text-gray-700 '>{review.content}</p></div>
                  <div className='p-2 inline-flex place-items-start items-start flex-wrap space-x-1  self-end '>
                    <h4 className='text-xs leading-tight text-gray-800'>
                      {review.author}
                    </h4>
                    <h4 className='text-xs  leading-tight text-gray-800'>
                      {review.titlelocation}
                    </h4>
                    <h4 className='text-xs leading-tight text-gray-800'>
                      {review.course}
                    </h4>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
