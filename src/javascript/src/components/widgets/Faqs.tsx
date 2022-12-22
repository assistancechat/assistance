import { component$ } from "@builder.io/qwik";
import { IconArrowDownRight } from "../icons/IconArrowDownRight";
import { RegisteredComponent } from "@builder.io/sdk-qwik";

type ColumnItem = {
  question: string,
  answer: string
}

const Faqs = component$((props: {leftColumn: ColumnItem[], rightColumn: ColumnItem[]}) => {
  const items = [
    props.leftColumn,
    props.rightColumn,
  ];

  return (
    <section class="border-t border-gray-200 dark:border-slate-800">
    <div class="px-4 py-16 mx-auto max-w-6xl lg:py-20">
      <div class="max-w-xl sm:mx-auto lg:max-w-2xl">
        <div class="max-w-xl mb-10 md:mx-auto sm:text-center lg:max-w-2xl md:mb-12">
        <p class="text-base text-primary-600 dark:text-purple-200 font-semibold tracking-wide uppercase">
            FAQs
          </p>
          <h2 class="max-w-lg mb-4 text-3xl font-bold leading-none tracking-tight sm:text-4xl md:mx-auto font-heading">
            Frequently Asked Questions
          </h2>
        </div>
      </div>
      <div class="max-w-screen-xl sm:mx-auto">
        <div class="grid grid-cols-1 gap-x-8 gap-y-8 lg:gap-x-16 md:grid-cols-2">
          {items.map((subitems) => (
            <div class="space-y-8">
              {subitems.map(({ question, answer }) => (
                <div>
                  <p class="mb-4 text-xl font-bold">
                    <IconArrowDownRight class="w-7 h-7 text-secondary-500 inline-block" />
                    {question}
                  </p>
                  {answer.split("\n\n").map((paragraph) => (
                    <p class="text-gray-700 dark:text-gray-400 mb-2">
                      {paragraph}
                    </p>
                  ))}
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
    </section>
  );
});


export const FaqsItem: RegisteredComponent=   {
  component: Faqs,
  name: 'Faqs',
  builtIn: true,
  inputs: [
    {
      name: 'leftColumn',
      type: 'list',
      subFields: [
        {
          name: "question",
          type: 'longText',
        },
        {
          name: "answer",
          type: 'longText'
        }
      ]
    },
    {
      name: 'rightColumn',
      type: 'list',
      subFields: [
        {
          name: "question",
          type: 'longText',
        },
        {
          name: "answer",
          type: 'longText'
        }
      ]
    }
  ],
}