import {useContext} from 'react';
import { EnvelopeOpenIcon } from "@heroicons/react/24/solid";

import StartChatWithQuestionButton from "@/components/atoms/StartChatWithQuestionButton";

export default function MoreInfo(props) {
   


  return (
    <div id="MoreInfo" className="relative h-screen bg-white">
      <div className="mx-auto max-w-full lg:grid lg:grid-cols-12 lg:gap-x-8 lg:px-8">

      <div className="relative flex lg:col-span-7 xl:inset-0">
          <iframe
            className="w-screen aspect-video mt-10 pl-2 pr-2 bg-orange-50 object-cover lg:p-6 lg:w-full"
            src={props.videoLink}
            title={props.videoTitle}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            allowFullScreen
          />
        </div>
        <div className="px-6 pt-10 pb-24 sm:pb-32 justify-self-center lg:col-span-5 lg:px-0">
          <div className="mx-auto flex flex-col space-y-6 max-w-2xl lg:mx-0">
            <hr className="border-orange-400 border-2" />
            <h1 className="text-5xl capitalize tracking-normal leading-none">
              {props.heading}
            </h1>
            <h3 className="text-xl w-4/5 tracking-wide leading-tight font-light text-orange-400">
              {props.subHeading}
            </h3>
            <StartChatWithQuestionButton
              question={props.ChatButtonText}
              buttonClassName="bg-gray-800 px-4 py-2 text-sm text-left leading-none text-white shadow-sm hover:bg-orange-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 w-5/12"
              bubbleClassName="-ml-1 mr-3 h-7 w-7"
              textClassName="leading-none text-white text-sm text-left uppercase"
            />
            <div className="h-11">
              <button
                type="button"
                href={props.learnButtonLink}
                className=" bg-gray-800 px-4 py-2 text-sm text-left leading-none text-white shadow-sm hover:bg-orange-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
              >
                <EnvelopeOpenIcon
                  className="-ml-1 mr-3 w-7 h-7 "
                  aria-hidden="true"
                />
                {props.learnButtonText}
              </button>
            </div>
          </div>
        </div>


      </div>
    </div>
  );
}
