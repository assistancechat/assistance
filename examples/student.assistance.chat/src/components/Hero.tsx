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

import React from "react";
import { ArrowDownCircleIcon } from "@heroicons/react/24/solid";

import StartChatWithQuestionButton from "@/components/atoms/StartChatWithQuestionButton";

type HeroProps = {
  portraitPicture: string;
  landscapePicture: string;
  alt: string;
  learnButtonLink: string;
  question: string;
  learnButtonText: string;
  headLine: string;
  subHeading: string;
  chatButtonText: string;
};

export default function Hero(props: HeroProps) {
  return (
    <div className="w-screen h-screen">
      <img
        className="absolute opacity-30 -z-10 w-screen h-screen lg:hidden"
        src={props.portraitPicture}
        alt={props.alt}
      />
      <img
        className="absolute opacity-30 -z-10 w-screen h-screen hidden lg:block"
        src={props.landscapePicture}
        alt={props.alt}
      />
      <div className="grid grid-rows-6 w-screen h-screen">
        <button
          type="button"
          className="row-span-2 left-10 top-40 bg-orange-400 md:top-30 h-12 w-3/4 relative inline-flex items-center rounded-md border border-transparent px-4 py-2 shadow-sm hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 lg:w-1/4"
        >
          <a
            href={props.learnButtonLink}
            rel="noreferrer"
            target="_blank"
            className="inline-flex h-max w-max space-x-2"
          >
            <ArrowDownCircleIcon className="h-10 w-10 self-center text-white" />
            <h3 className="text-base font-medium text-white leading-none uppercase place-self-center ">
              {props.learnButtonText}
            </h3>
          </a>
        </button>
        <div className="space-y-6">
          <div className="row-span-4 relative left-5 sm:left-10 w-4/5 space-y-4 ">
            <h1 className="pt-4 text-5xl tracking-normalleading-none border-orange-400 border-t-4 ">
              {props.headLine}
            </h1>
            <h3 className="text-xl w-4/5 tracking-wide leading-tight font-light text-gray-800">
              {props.subHeading}
            </h3>
          </div>

          <StartChatWithQuestionButton
            question={props.chatButtonText}
            buttonClassName="row-span-1 relative bg-orange-400 inset-10 inline-flex w-5/6 rounded-md py-1 px-4 shadow-sm hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 lg:w-1/3 lg:justify-self-end lf:mt-10 space-x-4"
            bubbleClassName="-ml-1 animate-pulse self-center text-white h-12 w-12"
            textClassName="text-base font-medium text-white uppercase leading-none text-left place-self-center"
          />
        </div>

        <div></div>
      </div>
    </div>
  );
}
