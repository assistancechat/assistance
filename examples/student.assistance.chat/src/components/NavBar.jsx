import { useContext, useState, Fragment } from 'react'
import { Disclosure, Dialog, Transition, Switch } from '@headlessui/react'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'
import { ChatBubbleOvalLeftEllipsisIcon } from '@heroicons/react/24/solid'
import { AcademicCapIcon, EnvelopeIcon } from '@heroicons/react/24/solid'

import { ChatContext } from '@/providers/chat'
import { EmailForm } from '@/components/EmailForm'

import Logo2 from '@/images/Logo.gif'
import Image from 'next/image'

export default function Navbar() {
  const { chatData, setChatData } = useContext(ChatContext)
  const [isOpen, setIsOpen] = useState(false)

  function openModal() {
    setChatData({ ...chatData, open: true })
  }

  function openDialog() {
    setIsOpen(true)
  }

  function closeDialog() {
    setIsOpen(false)
  }

  const [agreed, setAgreed] = useState(false)

  function classNames(...classes) {
    return classes.filter(Boolean).join(' ')
  }

  return (
    <Disclosure as='nav' className='bg-white shadow w-screen fixed z-10'>
      {({ open }) => (
        <>
          <div className='mx-auto px-4 sm:px-6 lg:px-8'>
            <div className='flex h-16 justify-between'>
              <div className='flex'>
                <div className='-ml-2 mr-2 flex items-center md:hidden'>
                  {/* Mobile menu button */}
                  <Disclosure.Button className='inline-flex items-center justify-center  p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-orange-500'>
                    <span className='sr-only'>Open main menu</span>
                    {open ? (
                      <XMarkIcon className='block h-6 w-6' aria-hidden='true' />
                    ) : (
                      <Bars3Icon className='block h-6 w-6' aria-hidden='true' />
                    )}
                  </Disclosure.Button>
                </div>
                <div className='flex flex-shrink-0 items-center'>
                  <Image
                    className='block h-10 w-auto lg:hidden'
                    src={Logo2}
                    alt='Global Talent'
                  />
                  <Image
                    className='hidden h-10 w-auto lg:block'
                    src={Logo2}
                    alt='Global Talent'
                  />
                </div>
                <div className='hidden md:ml-6 md:flex md:space-x-8'>
                  {/* Current: "border-orange-500 text-orange-400", Default: "border-transparent text-gray-500 hover:border-gray-300 hover:text-orange-300" */}
                  <a
                    href='#MoreInfo'
                    className='inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium text-orange-400 hover:text-orange-700 hover:border-orange-500'
                  >
                    More Info
                  </a>
                  <a
                    href='#Reviews'
                    className='inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium text-orange-400 hover:text-orange-700 hover:border-orange-500'
                  >
                    Reviews
                  </a>
                  <a
                    href='#StudentExperience'
                    className='inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium text-orange-400 hover:text-orange-700 hover:border-orange-500'
                  >
                    Student Experience
                  </a>
                </div>
              </div>
              <div className='flex items-center'>
                <button
                  type='button'
                  onClick={openModal}
                  className='text-gray-600 text-md inline-flex items-center px-4 py-2 rounded-md shadow-sm hover:bg-orange-300 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2'
                >
                  <ChatBubbleOvalLeftEllipsisIcon
                    className='-ml-1 mr-2 h-5 w-5 text-orange-600'
                    aria-hidden='true'
                  />
                  <span className='text-gray-600 text-xs'>Chat</span>
                </button>
                <button
                  type='button'
                  className='text-gray-600 text-md inline-flex items-center px-4 py-2 rounded-md shadow-sm hover:bg-orange-300 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2'
                  onClick={() =>
                    window.open('https://forms.gle/bJohSSgcd2g61WKSA')
                  }
                  target='_blank'
                  rel='noreferrer'
                >
                  <AcademicCapIcon
                    className='-ml-1 mr-2 h-5 w-5 text-orange-600'
                    aria-hidden='true'
                  />
                  <span className='text-gray-600 text-xs'>Apply</span>
                </button>
                <button
                  type='button'
                  onClick={openDialog}
                  className='text-gray-600 text-md inline-flex items-center px-4 py-2 rounded-md shadow-sm hover:bg-orange-300 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2'
                >
                  <ChatBubbleOvalLeftEllipsisIcon
                    className='-ml-1 mr-2 h-5 w-5 text-orange-600'
                    aria-hidden='true'
                  />
                  <span className='text-gray-600 text-xs' onClick={openDialog}>
                    Enquire
                  </span>
                </button>
              </div>
            </div>
          </div>

          <Disclosure.Panel className='md:hidden'>
            <div className='space-y-1 pt-2 pb-3'>
              <Disclosure.Button
                as='a'
                href='#MoreInfo'
                className='block border-l-4 border-orange-500 bg-orange-50 py-2 pl-3 pr-4 text-base font-medium text-orange-700 sm:pl-5 sm:pr-6'
              >
                More Info
              </Disclosure.Button>
              <Disclosure.Button
                as='a'
                href='#Reviews'
                className='block border-l-4 border-transparent py-2 pl-3 pr-4 text-base font-medium text-gray-500 hover:border-gray-300 hover:bg-gray-50 hover:text-orange-300 sm:pl-5 sm:pr-6'
              >
                Reviews
              </Disclosure.Button>
              <Disclosure.Button
                as='a'
                href='#StudentExperience'
                className='block border-l-4 border-transparent py-2 pl-3 pr-4 text-base font-medium text-gray-500 hover:border-gray-300 hover:bg-gray-50 hover:text-orange-300 sm:pl-5 sm:pr-6'
              >
                Student Experience
              </Disclosure.Button>
              <Disclosure.Button
                as='a'
                href='#blog'
                className='block border-l-4 border-transparent py-2 pl-3 pr-4 text-base font-medium text-gray-500 hover:border-gray-300 hover:bg-gray-50 hover:text-orange-300 sm:pl-5 sm:pr-6'
              >
                Blogs
              </Disclosure.Button>
            </div>
          </Disclosure.Panel>

          <Transition appear show={isOpen} as={Fragment}>
            <Dialog as='div' className='relative z-10 ' onClose={closeDialog}>
              <Transition.Child
                as={Fragment}
                enter='ease-out duration-300'
                enterFrom='opacity-0'
                enterTo='opacity-100'
                leave='ease-in duration-200'
                leaveFrom='opacity-100'
                leaveTo='opacity-0'
              >
                <div className='fixed inset-0 bg-black bg-opacity-25' />
              </Transition.Child>

              <div className='fixed inset-0 overflow-y-auto'>
                <div className='flex min-h-full items-center justify-center p-4 text-center'>
                  <Transition.Child
                    as={Fragment}
                    enter='ease-out duration-300'
                    enterFrom='opacity-0 scale-95'
                    enterTo='opacity-100 scale-100'
                    leave='ease-in duration-200'
                    leaveFrom='opacity-100 scale-100'
                    leaveTo='opacity-0 scale-95'
                  >
                    <Dialog.Panel className='w-full max-w-md transform overflow-hidden rounded-2xl bg-gray-800 p-6 text-left align-middle shadow-xl transition-all'>
                      <Dialog.Title
                        as='h3'
                        className='text-3xl font-medium leading-none text-orange-400'
                      >
                        Contact Us
                      </Dialog.Title>
                      <div className='mt-5'>
                        <form
                          action='#'
                          method='POST'
                          className='grid grid-cols-1 gap-y-6 sm:grid-cols-2 sm:gap-x-8'
                        >
                          <div>
                            <label
                              htmlFor='first-name'
                              className='block text-sm font-medium text-orange-300'
                            >
                              First name
                            </label>
                            <div className='mt-1'>
                              <input
                                type='text'
                                name='first-name'
                                id='first-name'
                                autoComplete='given-name'
                                className='block w-full rounded-md border-gray-300 py-3 px-4 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
                              />
                            </div>
                          </div>
                          <div>
                            <label
                              htmlFor='last-name'
                              className='block text-sm font-medium text-orange-300'
                            >
                              Last name
                            </label>
                            <div className='mt-1'>
                              <input
                                type='text'
                                name='last-name'
                                id='last-name'
                                autoComplete='family-name'
                                className='block w-full rounded-md border-gray-300 py-3 px-4 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
                              />
                            </div>
                          </div>
                          <div className='sm:col-span-2'>
                            <label
                              htmlFor='email'
                              className='block text-sm font-medium text-orange-300'
                            >
                              Email
                            </label>
                            <div className='mt-1'>
                              <input
                                id='email'
                                name='email'
                                type='email'
                                autoComplete='email'
                                className='block w-full rounded-md border-gray-300 py-3 px-4 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
                              />
                            </div>
                          </div>
                          <div className='sm:col-span-2'>
                            <label
                              htmlFor='phone-number'
                              className='block text-sm font-medium text-orange-300'
                            >
                              Phone Number
                            </label>
                            <div className='relative mt-1 rounded-md shadow-sm'>
                              
                              <input
                                type='text'
                                name='phone-number'
                                id='phone-number'
                                autoComplete='tel'
                                className='block w-full rounded-md border-gray-300 py-3 px-4  focus:border-indigo-500 focus:ring-indigo-500'
                                placeholder='+61 1234 5678'
                              />
                            </div>
                          </div>
                          <div className='sm:col-span-2'>
                            <label
                              htmlFor='message'
                              className='block text-sm font-medium text-orange-300'
                            >
                              Message
                            </label>
                            <div className='mt-1'>
                              <textarea
                                id='message'
                                name='message'
                                rows={4}
                                className='block w-full rounded-md border-gray-300 py-3 px-4 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
                                defaultValue={''}
                              />
                            </div>
                          </div>
                          <div className='sm:col-span-2'>
                            <div className='flex items-start'>
                              <div className='flex-shrink-0'>
                                <Switch
                                  checked={agreed}
                                  onChange={setAgreed}
                                  className={classNames(
                                    agreed ? 'bg-indigo-600' : 'bg-gray-200',
                                    'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2'
                                  )}
                                >
                                  <span className='sr-only'>
                                    Agree to policies
                                  </span>
                                  <span
                                    aria-hidden='true'
                                    className={classNames(
                                      agreed
                                        ? 'translate-x-5'
                                        : 'translate-x-0',
                                      'inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out'
                                    )}
                                  />
                                </Switch>
                              </div>
                              <div className='ml-3'>
                                <p className='text-base text-gray-500'>
                                  By selecting this, you agree to the{' '}
                                  <a
                                    href='#'
                                    className='font-medium text-orange-300 underline'
                                  >
                                    Privacy Policy
                                  </a>{' '}
                                  and{' '}
                                  <a
                                    href='#'
                                    className='font-medium text-orange-300 underline'
                                  >
                                    Cookie Policy
                                  </a>
                                  .
                                </p>
                              </div>
                            </div>
                          </div>
                          <div className='sm:col-span-2'>
                            <button
                              type='submit'
                              className='inline-flex w-full items-center justify-center rounded-md border border-transparent bg-indigo-600 px-6 py-3 text-base font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2'
                            >
                              Let's talk
                            </button>
                          </div>
                        </form>
                      </div>
                    </Dialog.Panel>
                  </Transition.Child>
                </div>
              </div>
            </Dialog>
          </Transition>
        </>
      )}
    </Disclosure>
  )
}
