import StartChatWithQuestionButton from "@/components/atoms/StartChatWithQuestionButton";

const DATA = {
  video: {
    link: "https://www.youtube.com/embed/3_AoWp1tFMA",
    title: "Student Experience",
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
      className="flex flex-wrap p-4 space-y-4 h-screen lg:space-x-4 lg:space-y-0 bg-gray-200"
    >
      <div className="flex flex-col self-start mt-10 w-full lg:w-5/12 lg:ml-10 space-y-8 lg:space-y-20">
        <h1 className="animate-pulse text-3xl tracking-wide border-t-4 border-orange-600 w-3/4">
          Student Experience
        </h1>

        <StartChatWithQuestionButton
          question={DATA.ChatButton.text}
          buttonClassName="inline-flex h-max w-max space-x-2 flex relative items-center rounded-md border border-transparent px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-orange-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 lg:w-1/2"
          bubbleClassName="-ml-1 self-center text-orange-600 h-10 w-10"
          textClassName="text-sm text-left text-black self-center leading-none uppercase"
        />
      </div>
      <iframe
        lazy="true"
        className="flex justify-center flex-wrap h-full w-full space-y-4 lg:w-1/2 lg:pt-10"
        src={DATA.video.link}
        title={DATA.video.title}
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; web-share"
      />
    </div>
  );
}
