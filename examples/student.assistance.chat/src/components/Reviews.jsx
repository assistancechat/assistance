import StartChatWithQuestionButton from "@/components/atoms/StartChatWithQuestionButton";

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

const reviews = {
  featured: [
    {
      id: 1,
      content: `
        <p>The evidence based teaching at AC has really transformed the impacet of my ministry
        </p>
      `,
      author: "Bradley M",
      action: "I Enrolled for",
      reason: "Purpose Driven Study",
      titlelocation: "Senior Member of Churches of Christ, WA.",
      course: " Master of Counselling",
      avatarSrc: "https://randomuser.me/api/portraits/men/75.jpg",
    },
    {
      id: 2,
      content: `
          <p>I was studying the same degree at another university and the lecturer said that our worldview affects everything we do. At that moment, I realised I needed to find a new place to learn
          </p>
        `,
      author: "Abigail C",
      action: "I Applied for",
      reason: "Christ Centered Learning",
      titlelocation: "",
      course: "Bachelor of Applied Social Science",
      avatarSrc: "https://randomuser.me/api/portraits/women/65.jpg",
    },
    {
      id: 3,
      content: `
          <p>The evidence based teaching at AC has really transformed the impact of my ministry
          </p>
        `,
      author: "Anne L",
      action: "I GRADUATED WITH",
      reason: "a meaningful career path",
      titlelocation: "Founder",
      course: " Chaplaincy Australia",
      avatarSrc: "https://randomuser.me/api/portraits/women/72.jpg",
    },
    // More reviews...
  ],
};

export default function Reviews2() {
  return (
    <div className="bg-gray-100">
      <div className="mx-auto max-w-2xl py-16 px-4 sm:py-24 sm:px-6 lg:grid lg:max-w-7xl lg:grid-cols-12 lg:gap-x-8 lg:py-32 lg:px-8">
        <div className="lg:col-span-4">
          <div className="bg-orange-400 rounded-lg">
            <div className="mx-auto max-w-7xl py-10 px-6 border-2 rounded-lg border-gray-400 sm:py-5 lg:px-4">
              <div className="mx-auto max-w-4xl text-center space-y-2">
                <h2 className="pt-4 text-5xl tracking-normal leading-none border-white text-left border-b-4 border-w-2/3 border-orange-500">
                  Counselling Snapshot
                </h2>
                <p className="text-lg text-left font-light text-gray-800">
                  A Career Worth Pursuing at Alphacrucis
                </p>
              </div>
              <dl className="mt-10 text-center space-y-4">
                <div className="flex border-white border-2 flex-col">
                  <dt className=" order-2 mt-2 text-lg font-medium leading-6 text-gray-800 ">
                    Starting Salary
                  </dt>
                  <dd className="order-1 text-5xl font-bold tracking-tight text-white">
                    $75,000 ↑
                  </dd>
                </div>
                <div className="mt-10 border-white border-2 flex flex-col sm:mt-0">
                  <dt className="order-2 mt-2 text-lg font-medium leading-6 text-gray-800 ">
                    of all Australians will need help from a mental health
                    worker at some point in their life{" "}
                  </dt>
                  <dd className="order-1 text-5xl font-bold tracking-tight text-white">
                    40%
                  </dd>
                </div>
                <div className="mt-10 border-white border-2 flex flex-col sm:mt-0">
                  <dt className="order-2 mt-2 text-lg font-medium leading-6 text-gray-800 ">
                    of all counsellors find their career meaningful and
                    rewarding
                  </dt>
                  <dd className="order-1 text-5xl font-bold tracking-tight text-white">
                    {">"} 85%
                  </dd>
                </div>
              </dl>
            </div>
          </div>
        </div>

        <div className="mt-16 lg:col-span-7 lg:col-start-6 lg:mt-0">
          <h3 className="sr-only">Student Reviews</h3>

          <div className="flow-root">
            <div className="-my-5 divide-y divide-gray-200 space-y-2">
              {reviews.featured.map((review) => (
                <div
                  key={review.id}
                  className="py-6 hover:bg-orange-200 rounded-md p-2"
                >
                  <div className="flex items-center">
                    <img
                      src={review.avatarSrc}
                      alt={`${review.author}.`}
                      className="h-12 w-12 rounded-full"
                    />
                    <div className="ml-4">
                      <h4 className="text-lg font-light text-gray-900 leading-tight tracking-wide uppercase">
                        {review.action}
                      </h4>
                      <h3 className="text-2xl font-bold tracking-wide leading-none text-gray-900 capitalize">
                        {review.reason}
                      </h3>
                      <div className="mt-1 flex items-center"></div>
                    </div>
                  </div>
                  <div
                    className="mt-4 space-y-2 text-base italic text-gray-800 "
                    dangerouslySetInnerHTML={{ __html: review.content }}
                  />
                  <div className="inline-flex space-x-2 self-end ">
                    <h4 className="text-xs font-bold text-gray-900">
                      {review.author}
                    </h4>
                    <h4 className="text-xs italic text-gray-900">
                      {review.titlelocation}
                    </h4>
                    <h4 className="text-xs italic font-bold text-gray-900">
                      {review.course}
                    </h4>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <StartChatWithQuestionButton
          question={DATA.ChatButton.text}
          buttonClassName="inline-flex h-max w-max space-x-2 animate-pulse flex relative items-center rounded-md border border-transparent px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-orange-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
          bubbleClassName="-ml-1 self-center text-orange-600 h-10 w-10"
          textClassName="text-sm text-left text-black self-center leading-none uppercase"
        />
      </div>
    </div>
  );
}
