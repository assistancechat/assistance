import Image from "next/image";

import StartChatWithQuestionButton from "@/components/atoms/StartChatWithQuestionButton";

import ReviewsMediaObject from "./ReviewsMediaObject";
import CounsellingPhoto1 from "../images/counselling-photo-1.png";
import CounsellingProfile1 from "../images/counselling-profile-1.png";
import CounsellingProfile2 from "../images/counselling-profile-2.png";
import CounsellingProfile3 from "../images/counselling-profile-3.png";

const data = [
  {
    id: "1",
    src: CounsellingProfile1,
    title: "I ENROLLED FOR",
    headline: "Purpose Driven Study",
    quote:
      "The evidence based teaching at AC has really transformed the impacet of my ministry - Bradley Middleton, Senior Member of Churches of Christ, WA. Master of Counselling Student",
  },
  {
    id: "2",
    src: CounsellingProfile2,
    title: "I APPLIED FOR",
    headline: "Christ Centered Learning",
    quote:
      "I was studying the same degree at another university when the lecturer said that our worldview affects everything we do. At that moment, I realised I needed to find a new place to learn - Abigail Comafay, Bachelor of Applied Social Science Student",
  },
  {
    id: "3",
    src: CounsellingProfile3,
    title: "I GRADUATED WITH",
    headline: "Christ Centered Learning",
    quote:
      "Alphacrucis College helps you to empower others by instilling the kind of care for people as exemplified by Christ - Anne Luliano, Founder. Chaplaincy Australia",
  },
];

const DATA = {
  ChatButton: {
    href: "#chat",
    text: "What courses are on offer?",
  },
};

export default function Reviews(props) {
  return (
    <div
      id="Reviews"
      className="flex flex-wrap w-screen bg-white p-4 space-x-6"
    >
      <div className="flex flex-wrap justify-center items-center lg:w-1/3 space-y-6">
        <div className="flex justify-center">
          <Image
            src={CounsellingPhoto1}
            alt="counselling.png"
            className="w-1/2 h-1/2"
          />
        </div>

        <StartChatWithQuestionButton
          question={DATA.ChatButton.text}
          buttonClassName="inline-flex h-max w-max space-x-2 animate-pulse flex relative items-center rounded-md border border-transparent px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-orange-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
          bubbleClassName="-ml-1 self-center text-orange-600 h-10 w-10"
          textClassName="text-sm text-left text-black self-center leading-none uppercase"
        />
      </div>
      <div className="flex flex-wrap self-center space-y-8 mt-6 lg:w-7/12 lg:justify-evenly lg:place-items-stretch">
        {data.map((item) => (
          <ReviewsMediaObject
            key={item.id}
            src={item.src}
            title={item.title}
            headline={item.headline}
            quote={item.quote}
          />
        ))}{" "}
      </div>
    </div>
  );
}
