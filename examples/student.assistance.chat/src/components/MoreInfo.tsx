// Copyright (C) 2023 Assistance.Chat contributors

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//     http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { EnvelopeOpenIcon } from "@heroicons/react/24/solid";

import StartChatWithQuestionButton from "@/components/atoms/StartChatWithQuestionButton";

type MoreInfoProps = {
  heading: string;
  subHeading: string;
  videoLink: string;
  videoTitle: string;
  chatButtonText: string;
  learnButtonLink: string;
  learnButtonText: string;
};

export default function MoreInfo(props: MoreInfoProps) {
  return (
    <div id="MoreInfo" className="relative bg-white">
      <div className="mx-auto max-w-full lg:grid lg:grid-cols-12 lg:gap-x-8 lg:px-8">
        <div className="relative flex justify-items-center lg:col-span-7 xl:inset-0">
          <iframe
            className="w-screen aspect-video mt-10 pl-2 pr-2 bg-gray-50 object-cover lg:p-6 lg:w-full"
            src={props.videoLink}
            title={props.videoTitle}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            allowFullScreen
          />
        </div>
        <div className="px-6 pt-10 pb-24 sm:pb-32 lg:col-span-5 lg:px-0 lg:pb-56 ">
          <div className="mx-auto space-y-12 max-w-2xl lg:mx-0">
            <h1 className="pt-4 mt-10 text-5xl capitalize tracking-normal leading-none border-orange-400 border-t-4">
              {props.heading}
            </h1>
            <h3 className="text-xl w-4/5 tracking-wide leading-tight font-light text-gray-800">
              {props.subHeading}
            </h3>
            <StartChatWithQuestionButton
              question={props.chatButtonText}
              buttonClassName="inline-flex items-center rounded-md border uppercase border-transparent bg-orange-400 px-4 py-2 text-white shadow-sm hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
              bubbleClassName="-ml-1 mr-3 h-8 w-8"
              textClassName="leading-none text-white text-sm text-left uppercase"
            />
            <div className="h-11">
              <button
                type="button"
                onClick={() => window.open(props.learnButtonLink)}
                className=" bg-orange-400 px-4 py-2 text-sm text-left leading-none text-white shadow-sm hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
              >
                <EnvelopeOpenIcon
                  className="-ml-1 mr-3 w-8 h-8 "
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
