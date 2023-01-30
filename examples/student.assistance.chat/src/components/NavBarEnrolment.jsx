import { Fragment } from 'react'
import { Menu, Transition } from '@headlessui/react'
import { ChevronDownIcon } from '@heroicons/react/20/solid'
import { GoogleEnrolmentForm } from './GoogleEnrolmentForm'

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function NavBarEnrolment() {
  return (
    <Menu.Items className='absolute w-screen h-screen right-0 z-10 mt-2 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none'>
<GoogleEnrolmentForm />
    </Menu.Items>
  )
}
