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

import { useState, useEffect, useRef } from "react";

import StartChatWithQuestionButton from "@/components/atoms/StartChatWithQuestionButton";
import Typed from "typed.js";

type HeroOpeningProps = {
  portraitPicture: string;
  landscapePicture: string;
  alt: string;
  chatButtonText: string;
};

export default function HeroOpening(props: HeroOpeningProps) {
  const headlineConfig = {
    strings: [
      "<u>Ministry</u>",
      "<u>Counselling </u>",
      "<u>Education</u>",
      "<u>Business</u>",
      "<u>Life</u>",
    ],
    typeSpeed: 5,
    backSpeed: 25,
    backDelay: 1200,
    loop: true,
    loopCount: 1,
    showCursor: false,
    bindInputFocusEvents: true,
    fadeOut: true,
    fadeOutClass: 'typed-fade-out',
    fadeOutDelay: 500,
  };

  const subHeadingConfig = {
    strings: [
      "We will help you find the right course and connect you to your purpose",
      "Don't wait and waste your talent", 
      "ASK US TODAY."
    ],
    typeSpeed: 15,
    backSpeed: 10,
    backDelay: 1350,
    startDelay: 8000,
    loop: true,
    loopCount: 1,
    showCursor: false,
    fadeOut: false,
    fadeOutClass: 'typed-fade-out',
    fadeOutDelay: 500,
  };

  const headlineRef = useRef() as React.MutableRefObject<HTMLHeadingElement>;
  const [headline, setHeadline] = useState<Typed>();

  const subHeadingRef = useRef() as React.MutableRefObject<HTMLHeadingElement>;
  const [subHeading, setSubHeading] = useState<Typed>();

  const constTypedEffects = [
    {
      ref: headlineRef,
      set: setHeadline,
      config: headlineConfig,
    },
    {
      ref: subHeadingRef,
      set: setSubHeading,
      config: subHeadingConfig,
    },
  ];

  constTypedEffects.map((items) => {
    useEffect(() => {
      const typed = new Typed(items.ref.current, items.config);
      items.set(typed);
      return () => {
        typed.destroy();
      };
    }, []);
  });

  return (
    <div className="w-screen h-screen">
      <img
        className="absolute opacity-30 -z-10 w-screen h-screen md:hidden"
        src={props.portraitPicture}
        alt={props.alt}
      />
      <img
        className="absolute opacity-30 -z-10 w-screen h-screen hidden md:block"
        src={props.landscapePicture}
        alt={props.alt}
      />
      <div className="grid grid-rows-6 w-screen h-screen">
        <div className="row-span-1 lg:row-span-2"></div>
        <div className="space-y-6 w-screen">
          <div className="row-span-4 relative w-screen space-y-4 ">
            <hr className="border-orange-400 border-2 w-10/12 ml-10" />
            <h1 className = "text-5xl pl-10 tracking-normal leading-none"> Discover God's Purpose for you in </h1>
            <span
              className="text-5xl pl-10 tracking-normal leading-none"
              ref={headlineRef}
            />
            <h3
              className="text-xl pl-10 pr-10 tracking-wide leading-tight font-light text-gray-800 w-screen"
              ref={subHeadingRef}
            />
          </div>

          <StartChatWithQuestionButton
            question={props.chatButtonText}
            buttonClassName="row-span-1 inset-10 relative bg-gray-800 inline-flex w-9/12 rounded-md py-1 px-4 shadow-sm hover:bg-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 lg:w-1/3 lg:justify-self-end space-x-4"
            bubbleClassName="-ml-1 self-center text-white h-12 w-12"
            textClassName="text-sm font-medium text-white uppercase leading-none text-left place-self-center"
          />
        </div>

        <div className="w-screen"></div>
      </div>
    </div>
  );
}
