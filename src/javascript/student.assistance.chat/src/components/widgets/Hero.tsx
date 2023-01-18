import { component$ } from "@builder.io/qwik";
import { RegisteredComponent } from "@builder.io/sdk-qwik";

const Hero = component$((props: {header: string, tagline: string, image: string, primaryButtonText: string, primaryButtonUrl: string}) => {
  return (
    <section class={`bg-gradient-to-b md:bg-gradient-to-r from-white via-purple-50 to-sky-100 dark:bg-none mt-[-100px]`}>
      <div class="max-w-6xl mx-auto px-4 sm:px-6 md:flex md:h-screen 2xl:h-auto pt-[100px]">
        <div class="py-12 md:py-12 lg:py-16 block md:flex text-center md:text-left">
          <div class="pb-12 md:pb-0 md:py-0 max-w-5xl mx-auto md:pr-16 flex items-center basis-[56%]">
            <div>
              <h1 class="text-5xl md:text-[3.48rem] font-bold leading-tighter tracking-tighter mb-4 font-heading px-4 md:px-0">
                {props.header}
              </h1>
              <div class="max-w-3xl mx-auto">
                <p class="text-xl text-gray-600 mb-8 dark:text-slate-400">
                  {props.tagline}
                </p>
                <div class="max-w-xs sm:max-w-md flex flex-nowrap flex-col sm:flex-row gap-4 m-auto md:m-0 justify-center md:justify-start">
                  <div class="flex w-full sm:w-auto">
                    <a
                      class="btn btn-primary sm:mb-0 w-full"
                      href={props.primaryButtonUrl}
                      target="_blank"
                      rel="noopener"
                    >
                      {props.primaryButtonText}
                    </a>
                  </div>
                  <div class="flex w-full sm:w-auto">
                    <button
                      class="btn w-full bg-gray-50 dark:bg-transparent"
                      onClick$={() => {
                          const e = document.getElementById("features");
                          if (e !== null) {
                            e.scrollIntoView();
                          }
                        }
                      }
                    >
                      Learn more
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="block md:flex items-center flex-1">
            <div class="relative m-auto max-w-4xl">
              <picture>
                <img
                  src={props.image}
                  width={1000}
                  height={1250}
                  class="mx-auto w-full rounded-md md:h-full drop-shadow-2xl bg-gray-400 dark:bg-slate-700"
                  alt="OpenSaMD"
                  loading="eager"
                  decoding="async"
                />
              </picture>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
});


export const HeroItem: RegisteredComponent = {
  component: Hero,
  name: 'Hero',
  builtIn: true,
  inputs: [
    {
      name: 'header',
      type: 'string'
    },
    {
      name: 'tagline',
      type: 'longText'
    },
    {
      name: 'image',
      type: 'file'
    },
    {
      name: 'primaryButtonText',
      type: "string"
    },
    {
      name: 'primaryButtonUrl',
      type: "string"
    }
  ],
}
