import { Container } from '@/components/Container'


//AppDemo on the side of the screen
function App() {
  return (

    <div className="m-auto p-10 border-gray-200 space-y-4 rounded-xl shadow-2xl">
      <div className="ml-10 rounded-lg bg-cyan-500 py-1 p-3 text-right text-sm text-white leading-snug">
        Congratulations Caroline! We{"'"}ve just enrolled you into the Bachelor of Ministry.
      </div>

      <div className="mr-14 rounded-lg bg-green-500 py-1 p-3 text-left text-sm text-white leading-snug">
        😌{"   "}{"   "}Thank you! That was so easy.
      </div>

      <div className="ml-12 rounded-lg bg-cyan-500 py-1 p-3 text-right text-sm text-white leading-snug">
        No worries. So happy we got you enrolled. {" "} 🥳🥳🥳
      </div>
    </div>
  )
}

//The main hero section
export function Hero() {
  return (
    <div className="overflow-hidden py-20 sm:py-32 lg:pb-32 xl:pb-36">
      <Container>
        <div className="lg:grid lg:grid-cols-12 lg:gap-x-8 lg:gap-y-20">
          <div className="relative z-10 mx-auto max-w-lg lg:max-w-xl lg:col-span-5  lg:pt-6 xl:col-span-6">
            <h1 className="text-4xl font-medium tracking-tight text-gray-900">
              Effortless answers to your Alphacrucis questions
            </h1>
            <p className="mt-6 text-lg text-gray-600">
              We understand that the enrolment process can be stressful. It{"'"}s
              why we are offering you a no stress enrolment service for free.
            </p>
          </div>
          <div className="m-auto mt-10 max-w-lg relative lg:col-span-7 lg:row-span-2 lg:mt-0 xl:col-span-6">
            <App />
          </div>
        </div>
      </Container>
    </div>
  )
}
