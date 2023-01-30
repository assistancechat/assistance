import { ChatBubbleOvalLeftEllipsisIcon } from "@heroicons/react/24/outline";

const studentExperienceData = {
  video: {
    link: "https://www.youtube.com/embed/3_AoWp1tFMA",
    title: 'Student Experience',
  },
  ChatButton: {
    href: "#Chat",
    text: "What is studying at Alphacrucis like?",
  },
};

export default function StudentExperience() {
  return (
    <div
      id="StudentExperience"
      className="flex flex-wrap w-screen h-screen p-4 space-y-4 lg:space-x-4 lg:space-y-0 bg-gray-200"
    >
      <div className='flex flex-col self-start mt-10 w-full lg:w-5/12 lg:ml-10 space-y-8 lg:space-y-20'>
        <h1 className='animate-pulse text-3xl tracking-wide border-t-4 border-orange-600 w-3/4'>
          Student Experience
        </h1>
        <button
          type="button"
          className="flex relative items-center rounded-md border border-transparent px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-orange-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 lg:w-1/2"
        >
          <a
            href={studentExperienceData.ChatButton.href}
            className="inline-flex h-max w-max space-x-2"
          >
            <ChatBubbleOvalLeftEllipsisIcon className="-ml-1 self-center text-orange-600 h-10 w-10" />
            <h3 className="text-sm text-left text-black self-center leading-none uppercase">
              {studentExperienceData.ChatButton.text}
            </h3>
          </a>
        </button>
      </div>
      <iframe
        lazy ='true'
        className='flex justify-center flex-wrap h-full w-full space-y-4 lg:w-1/2 lg:pt-10'
        src={studentExperienceData.video.link}
        title={studentExperienceData.video.title}
        allow=  'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; web-share'
      />
    </div>
  );
}
