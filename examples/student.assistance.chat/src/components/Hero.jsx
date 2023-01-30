import React from "react";
import { ArrowDownCircleIcon } from "@heroicons/react/24/solid";
import { ChatBubbleOvalLeftEllipsisIcon } from "@heroicons/react/24/outline";

const courseResources = {
  videoBackground: {
    link: "https://www.youtube.com/embed/e6Gueu7UoFY?controls=0&loop=1",
    videoTitle: "Counselling Video",
  },
  courseTitle: "COURSE RESOURCES",
  headLine: "Discover God’s Purpose for you in Counselling",
  subHeading:
    "Talk with our customer exerience officer to find the right course for you",
  LearnButton: {
    text: "Study Christian Counselling",
    link: "https://www.ac.edu.au/healthbrochure",
  },
  ChatButton: {
    text: "How can you help me align counselling with my faith?",
    link: "#Chat",
  },
};

//currently video is hidden, remove hidden to play video
export default function Hero() {
  return (
    <div className="w-screen h-screen">
      <iframe
        lazy
        className="absolute opacity-30 -z-10 w-screen h-screen"
        src={courseResources.videoBackground.link}
        title={courseResources.videoBackground.videoTitle}
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; web-share"
      />
      <div className="grid grid-rows-6 w-screen h-screen">
        <button
          type="button"
          className="row-span-2 left-10 top-20 h-12 w-3/4 relative inline-flex items-center rounded-md border border-transparent px-4 py-2 shadow-sm hover:bg-white focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 lg:w-1/4"
        >
          <a
            href={courseResources.LearnButton.link}
            rel="noreferrer"
            target="_blank"
            className="inline-flex h-max w-max space-x-2"
          >
            <ArrowDownCircleIcon className="h-10 w-10 self-center text-orange-600" />
            <h3 className="text-lg self-center text-left text-black leading-none uppercase ">
              {courseResources.LearnButton.text}
            </h3>
          </a>
        </button>
        <div>
          <div className="row-span-4 relative left-10 w-4/5 space-y-4 ">
            <h1 className="pt-4 text-5xl tracking-normalleading-none border-orange-400 border-t-4 border-orange-500">
              {courseResources.headLine}{" "}
            </h1>
            <h3 className="text-xl w-4/5 tracking-wide leading-tight font-light text-gray-800">
              {courseResources.subHeading}
            </h3>
          </div>

          <button
            type="button"
            className="row-span-1 relative inset-10 inline-flex h-12 w-5/6 inline-flex items-center rounded-md border border-transparent px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-white focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 lg:w-1/3 lg:justify-self-end lf:mt-10"
          >
            <a
              href={courseResources.ChatButton.link}
              className="inline-flex h-max w-max space-x-2"
            >
              <ChatBubbleOvalLeftEllipsisIcon className="-ml-1 self-center text-orange-600 h-12 w-12" />
              <h3 className="text-md text-black text-left self-center leading-none uppercase">
                {courseResources.ChatButton.text}
              </h3>
            </a>
          </button>
        </div>

        <div></div>
      </div>
    </div>
  );
}
