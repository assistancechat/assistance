import { component$ } from "@builder.io/qwik";
import { RegisteredComponent } from "@builder.io/sdk-qwik";

const CallToAction = component$((props: {title: string, description: string, buttonText: string, buttonUrl: string}) => {
  return (
    <section class="relative">
      <div class="max-w-6xl mx-auto px-4 sm:px-6">
        <div class="py-12 md:py-20">
          <div class="max-w-3xl mx-auto text-center p-6 rounded-md shadow-xl dark:shadow-none">
            <h2 class="text-4xl md:text-4xl font-bold leading-tighter tracking-tighter mb-4 font-heading">
              {props.title}
            </h2>
            <p class="text-xl text-gray-600 dark:text-slate-400">
              {props.description}
            </p>

            <div class="mt-6">
              <a
                class="btn btn-primary mb-4 sm:mb-0 w-full sm:w-auto"
                href={props.buttonUrl}
                target="_blank"
                rel="noopener"
              >
                {props.buttonText}
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
});

export const CallToActionItem: RegisteredComponent = {
  component: CallToAction,
  name: 'CallToAction',
  builtIn: true,
  inputs: [
    {
      name: 'title',
      type: 'string'
    },
    {
      name: 'description',
      type: 'longText'
    },
    {
      name: 'buttonText',
      type: "string"
    },
    {
      name: 'buttonUrl',
      type: "string"
    }
  ],
}
