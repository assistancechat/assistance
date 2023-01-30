import React, { useState, useEffect } from 'react';
import {Dialog, Transition} from '@headlessui/react'
import { XIcon } from '@heroicons/react/outline'
import { DocumentMagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { ChevronLeftIcon } from '@heroicons/react/24/solid';
import GoogleEnrolmentForm from './GoogleEnrolmentForm';

export default function ChatHeader(props) {
    const [isOpen, setIsOpen] = useState(false)
    const [name, setName] = useState(props.name)
    const [profilepictureurl, setProfilePictureUrl] = useState(props.profilepictureurl)

    function closeModal() {
        setIsOpen(false)
    }

    function openModal() {
        setIsOpen(true)
    }

    return (
        <>
            <div className="flex items-center justify-between px-4 py-2 bg-white border-b border-gray-200">
                <div className="flex items-center">
                    <button className="p-2 mr-2 text-gray-600 rounded-full hover:bg-gray-100 focus:outline-none focus:bg-gray-100">
                    <ChevronLeftIcon className="w-5 h-5" />
                    </button>
                    <div className="flex flex-col">
                        <span className="font-semibold text-gray-700">{props.name}</span>
                    </div>
                </div>
                <div className="flex items-center">
                    <button className="p-2 mr-2 text-gray-600 rounded-full hover:bg-gray-100 focus:outline-none focus:bg-gray-100">
                     <DocumentMagnifyingGlassIcon className="w-5 h-5" />
                    </button>
                    <button className="p-2 text-gray-600 rounded-full hover:bg-gray-100 focus:outline-none focus:bg-gray-100">
                        <img className="w-8 h-8 rounded-full" src={props.profilepictureurl} alt="profilepictureurl" />
                    </button>
                </div>
            </div>
            <Transition appear show={isOpen} as={React.Fragment}>
                <Dialog
                    as="div"
                    className="fixed inset-0 z-10 overflow-y-auto"
                    onClose={closeModal}
                >
                    <div className="min-h-screen px-4 text-center">
                        <Transition.Child
                            as={React.Fragment}
                            enter="ease-out duration-300"
                            enterFrom="opacity-0"
                            enterTo="opacity-100"
                            leave="ease-in duration-200"
                            leaveFrom="opacity-100"
                            leaveTo="opacity-0"
                        >
                            <Dialog.Overlay className="fixed inset-0" />
                        </Transition.Child>

                        {/* This element is to trick the browser into centering the modal contents. */}
                        <span
                            className="inline-block h-screen align-middle"
                            aria-hidden="true"
                        >
                            &#8203;
                        </span>
                        <Transition.Child
                            as={React.Fragment}
                            enter="ease-out duration-300"
                            enterFrom="opacity-0 scale-95"
                            enterTo="opacity-100 scale-100"
                            leave="ease-in duration-200"
                            leaveFrom="opacity-100 scale-100"
                            leaveTo="opacity-0 scale-95"
                        >
                            <div className="inline-block w-full max-w-md p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl">
                                <Dialog.Title
                                    as="h3"
                                    className="text-lg font-medium leading-6 text-gray-900"
                                >
                                    {props.name}
                                </Dialog.Title>
                                <div className="mt-2">
                                    <GoogleEnrolmentForm />
                                </div>

                                <div className="mt-4">
                                    <button
                                        type="button"
                                        className="inline-flex justify-center w-full px-4 py-2 text-base font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-red-500"
                                        onClick={closeModal}
                                    >
                                        Close
                                    </button>
                                </div>
                            </div>
                        </Transition.Child>
                    </div>
                </Dialog>
            </Transition>
        </>
    )
    }