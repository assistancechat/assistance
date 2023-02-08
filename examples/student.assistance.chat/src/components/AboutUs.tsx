import React, { useContext } from 'react'
import {
  NewspaperIcon,
  ChatBubbleLeftRightIcon,
  BriefcaseIcon
} from '@heroicons/react/24/outline'
import { ChatContext } from '@/providers/chat'
import Image from 'next/image';
import { Autour_One } from '@next/font/google';

const supportLinks = [
  {
    name: 'Student Course Application',
    href: '#',
    description:
      'We offer education agent services to connect you the education you need for the Australian job you are meant for. Helping you succeed.',
    icon: NewspaperIcon
  },
  {
    name: 'Career Counselling',
    href: '#',
    description:
      'We believe that everyone has Talents and Gifts that God has given them. We will speak to you, find your purpose and guide you into the right career.',
    icon: ChatBubbleLeftRightIcon
  },
  {
    name: 'Job Placement',
    href: '#',
    description:
      'Getting a job or work experience is difficult. We make it easy for you.',
    icon: BriefcaseIcon
  }
];

export default function AboutUs() {
const { chatData, setChatData } = useContext(ChatContext)

function openEnquireModal() {
  setChatData({ ...chatData, openModal: 'enquire' })}


  return (
    <div className='bg-white'>
      {/* Header */}
      <div className="relative bg-gray-800 pb-32">
        <div className="absolute inset-0">
          <img
            className="h-full w-full object-cover"
            src="https://images.unsplash.com/photo-1573496546038-82f9c39f6365?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1469&q=80"
            alt=""
          />
          <div className="absolute inset-0 bg-gray-700 mix-blend-multiply" aria-hidden="true" />
        </div>
        <div className="relative mx-auto max-w-7xl py-24 px-6 sm:py-32 lg:px-8">
          <h1 className="text-4xl font-bold tracking-tight text-orange-400 md:text-5xl lg:text-6xl">
            About Us
          </h1>
          <p className='mt-6 max-w-3xl text-xl text-gray-300'>
            Our team will help you find the right career in Australia. Our
            Christian values guide us and we are committed to finding meaningful
            and fufilling work for you.
          </p>
          <p className='mt-6 max-w-3xl text-xl text-gray-300'>
            If you are willing to begin your journey. We would love to support
            you and help you invest your talent wisely.
          </p>
        </div>
      </div>

      {/* Overlapping cards */}
      <section
        className='relative z-10 mx-auto -mt-32 max-w-7xl px-6 pb-32 lg:px-8'
        aria-labelledby='contact-heading'
      >
        <h2 className='sr-only' id='contact-heading'>
          Contact us
        </h2>
        <div className='grid grid-cols-1 gap-y-20 lg:grid-cols-3 lg:gap-y-0 lg:gap-x-8'>
          {supportLinks.map((link) => (
            <div
              key={link.name}
              className='flex flex-col rounded-2xl bg-white shadow-xl'
            >
              <div className='relative flex-1 px-6 pt-16 pb-8 md:px-8'>
                <div className='absolute top-0 inline-block -translate-y-1/2 transform rounded-xl bg-orange-400 p-5 shadow-lg'>
                  <link.icon
                    className='h-8 w-8 text-white'
                    aria-hidden='true'
                  />
                </div>
                <h3 className='text-xl font-medium text-gray-800'>
                  {link.name}
                </h3>
                <p className='mt-4 text-base text-gray-500'>
                  {link.description}
                </p>
              </div>
              <div className='rounded-bl-2xl rounded-br-2xl text-orange-400 bg-gray-50 p-6 md:px-8 hover:bg-gray-800 hover:text-white'>
                <p
                  onClick={openEnquireModal}
                  className='text-base font-medium'
                >
                  Contact us<span aria-hidden='true'> &rarr;</span>
                </p>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
