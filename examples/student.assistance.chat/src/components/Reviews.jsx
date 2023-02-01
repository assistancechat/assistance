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

const reviews = {
  featured: [
    {
      id: 1,
      content: `
        <p>The evidence based teaching at AC has really transformed the impact of my ministry
        </p>
      `,
      author: "Bradley M",
      action: "I Enrolled for",
      reason: "Purpose Driven Study",
      titlelocation: "- Senior Member of Churches of Christ, WA.",
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
      course: "- Bachelor of Applied Social Science",
      avatarSrc: "https://randomuser.me/api/portraits/women/65.jpg",
    },
    {
      id: 3,
      content: `
          <p>The evidence based teaching at AC has really transformed the impact of my ministry
          </p>
        `,
      author: "Anne L -",
      action: "I GRADUATED WITH",
      reason: "a meaningful career path",
      titlelocation: "Founder, ",
      course: " Chaplaincy Australia",
      avatarSrc: "https://randomuser.me/api/portraits/women/72.jpg",
    },
    // More reviews...
  ],
};

export default function Reviews() {
  return (
    <div className="bg-gray-800">
      <div className="mx-auto max-w-2xl py-16 px-4 justify-items-center sm:py-24 sm:px-6 lg:grid lg:max-w-7xl lg:grid-cols-12 lg:gap-x-8 lg:py-32 lg:px-8">
        <div className="lg:col-span-4">
          <div className="bg-orange-400 rounded-lg">
            <div className="mx-auto max-w-7xl py-10 px-6 border-2 rounded-lg sm:py-5 lg:px-4">
              <div className="mx-auto max-w-4xl text-center space-y-2">
                <h2 className="pt-4 text-5xl  text-gray-800 tracking-normal leading-none border-white text-left border-b-4 border-w-2/3">
                  Counselling Snapshot
                </h2>
                <p className="text-lg text-left font-light text-gray-800">
                  A Career Worth Pursuing at Alphacrucis
                </p>
              </div>
              <dl className="mt-10 text-center space-y-4">
                <div className="flex border-white border-2 flex-col">
                  <dt className=" order-2 mt-2 text-lg font-light leading-6 text-gray-800 ">
                    Starting Salary
                  </dt>
                  <dd className="order-1 text-5xl font-bold tracking-tight text-white">
                    $75,000 ↑
                  </dd>
                </div>
                <div className="mt-10 border-white border-2 flex flex-col sm:mt-0">
                  <dt className="order-2 mt-2 text-lg font-light leading-6 text-gray-800 ">
                    of all Australians will need help from a mental health
                    worker at some point in their life{" "}
                  </dt>
                  <dd className="order-1 text-5xl font-bold tracking-tight text-white">
                    40%
                  </dd>
                </div>
                <div className="mt-10 border-white border-2 flex flex-col sm:mt-0">
                  <dt className="order-2 mt-2 text-lg font-light leading-6 text-gray-800 ">
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
            <div className="flex flex-wrap items-center divide-gray-200 space-y-2">
              {reviews.featured.map((review) => (
                <div
                  key={review.id}
                  className="p-6 bg-gray-300 hover:bg-orange-200 shadow border-gray-400 rounded-md"
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
                    className="mt-4 space-y-2 text-sm tracking-wide leading-tight italic text-gray-500 "
                    dangerouslySetInnerHTML={{ __html: review.content }}
                  />
                  <div className="inline-flex place-items-start items-start flex-wrap space-x-1  self-end ">
                    <h4 className="text-xs font-light italic leading-tight text-gray-900">
                      {review.author}
                    </h4>
                    <h4 className="text-xs font-light italic leading-tight text-gray-900">
                      {review.titlelocation}
                    </h4>
                    <h4 className="text-xs italic font-light leading-tight text-gray-900">
                      {review.course}
                    </h4>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
