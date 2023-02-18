import { useContext, useEffect } from "react";
import { Disclosure } from "@headlessui/react";
import { Bars3Icon, XMarkIcon } from "@heroicons/react/24/outline";
import { ChatBubbleOvalLeftEllipsisIcon } from "@heroicons/react/24/solid";
import { BriefcaseIcon, EnvelopeIcon } from "@heroicons/react/24/solid";

import { ChatContext } from "@/providers/chat";

import Logo2 from "@/images/Logo.gif";
import Image from "next/image";

export default function Navbar() {
  const { chatData, setChatData } = useContext(ChatContext);

  function openChatModal() {
    setChatData({ ...chatData, openModal: "chat" });
  }

  function openEnquireModal() {
    setChatData({ ...chatData, openModal: "enquire" });
  }


  return (
    <Disclosure as="nav" className="bg-white shadow w-screen fixed z-10">
      {({ open }) => (
        <>
          <div className="mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex h-16 justify-between">
              <div className="flex">
                <div className="-ml-2 mr-2 flex items-center md:hidden">
                  {/* Mobile menu button */}
                  <Disclosure.Button className="inline-flex items-center justify-center  p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-orange-500">
                    <span className="sr-only">Open main menu</span>
                    {open ? (
                      <XMarkIcon className="block h-6 w-6" aria-hidden="true" />
                    ) : (
                      <Bars3Icon className="block h-6 w-6" aria-hidden="true" />
                    )}
                  </Disclosure.Button>
                </div>
                <div className="flex flex-shrink-0 items-center">
                  <Image
                    className="block h-14 w-auto lg:hidden"
                    src={Logo2}
                    alt="Global Talent"
                  />
                  <Image
                    className="hidden h-12 w-auto lg:block"
                    src={Logo2}
                    alt="Global Talent"
                  />
                </div>
                <div className="hidden md:ml-6 md:flex md:space-x-8">
                  {/* Current: "border-orange-500 text-gray-800", Default: "border-transparent text-gray-500 hover:border-gray-300 hover:text-orange-300" */}
                  <a
                    href="#MoreInfo"
                    className="inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium text-gray-800 hover:text-orange-400 hover:border-orange-500"
                  >
                    More Info
                  </a>
                  <a
                    href="#Reviews"
                    className="inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium text-gray-800 hover:text-orange-400 hover:border-orange-500"
                  >
                    Reviews
                  </a>
                  <a
                    href="#StudentExperience"
                    className="inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium text-gray-800 hover:text-orange-400 hover:border-orange-500"
                  >
                    Student Experience
                  </a>
                </div>
              </div>
              <div className="flex items-center">
                <button
                  type="button"
                  onClick={openChatModal}
                  onLoad={openChatModal}
                  className="text-gray-800 flex-col text-md inline-flex items-center px-4 py-2 rounded-md shadow-sm hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2"
                >
                  <ChatBubbleOvalLeftEllipsisIcon
                    className="h-5 w-5 text-orange-600"
                    aria-hidden="true"
                  />
                  <span className="text-gray-800 text-xs">Talk To Us</span>
                </button>
                <button
                  type="button"
                  className="text-gray-800 flex-col text-md inline-flex items-center px-4 py-2 rounded-md shadow-sm hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2"
                  onClick={() =>
                    window.open("https://forms.gle/GEeMCX6Q95TeYzW37")
                  }
                >
                  <BriefcaseIcon
                    className="h-5 w-5 text-orange-600"
                    aria-hidden="true"
                  />
                  <span className="text-gray-800 text-xs">Apply</span>
                </button>
                <button
                  type="button"
                  onClick={openEnquireModal}
                  className="text-gray-800 flex-col text-md inline-flex items-center px-4 py-2 rounded-md shadow-sm hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2"
                >
                  <EnvelopeIcon
                    className="h-5 w-5 text-orange-600"
                    aria-hidden="true"
                  />
                  <span
                    className="text-gray-800 text-xs"
                    onClick={openEnquireModal}
                  >
                    Enquire
                  </span>
                </button>
              </div>
            </div>
          </div>

          <Disclosure.Panel className="md:hidden">
            <div className="space-y-1 pt-2 pb-3">
              <Disclosure.Button
                as="a"
                href="#MoreInfo"
                className="block border-l-4 border-orange-500 py-2 pl-3 pr-4 text-base font-medium text-orange-400 sm:pl-5 sm:pr-6"
              >
                More Info
              </Disclosure.Button>
              <Disclosure.Button
                as="a"
                href="#Reviews"
                className="block border-l-4 border-transparent py-2 pl-3 pr-4 text-base font-medium text-gray-500 hover:border-gray-300 hover:bg-gray-50 hover:text-orange-300 sm:pl-5 sm:pr-6"
              >
                Reviews
              </Disclosure.Button>
              <Disclosure.Button
                as="a"
                href="#StudentExperience"
                className="block border-l-4 border-transparent py-2 pl-3 pr-4 text-base font-medium text-gray-500 hover:border-gray-300 hover:bg-gray-50 hover:text-orange-300 sm:pl-5 sm:pr-6"
              >
                Student Experience
              </Disclosure.Button>
              <Disclosure.Button
                as="a"
                href="#blog"
                className="block border-l-4 border-transparent py-2 pl-3 pr-4 text-base font-medium text-gray-500 hover:border-gray-300 hover:bg-gray-50 hover:text-orange-300 sm:pl-5 sm:pr-6"
              >
                Blogs
              </Disclosure.Button>
            </div>
          </Disclosure.Panel>
        </>
      )}
    </Disclosure>
  );
}
