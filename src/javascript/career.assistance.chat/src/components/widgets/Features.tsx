import { component$ } from "@builder.io/qwik";
import { IconStar } from "~/components/icons/IconStar";
import { RegisteredComponent } from "@builder.io/sdk-qwik";

type ColumnItem = {
  title: string,
  description: string
}

const Features = component$((props: {title: string, description: string, leftColumn: ColumnItem[], rightColumn: ColumnItem[]}) => {
  const items = [
    props.leftColumn,
    props.rightColumn,
  ];

  return (
    <section class="scroll-mt-16" id="features">
      <div class="px-4 py-16 mx-auto max-w-6xl lg:px-8 lg:py-20">
        <div class="mb-10 md:mx-auto sm:text-center md:mb-12 max-w-3xl">
          <p class="text-base text-primary-600 dark:text-purple-200 font-semibold tracking-wide uppercase">
            Features
          </p>
          <h2 class="text-4xl md:text-5xl font-bold leading-tighter tracking-tighter mb-4 font-heading">
            {props.title}
          </h2>
          <p class="max-w-3xl mx-auto sm:text-center text-xl text-gray-600 dark:text-slate-400">
            {props.description}
          </p>
        </div>
        <div class="grid mx-auto space-y-6 md:grid-cols-2 md:space-y-0">
          {items.map((subitems) => (
            <div class="space-y-8 sm:px-8">
              {subitems.map(({ title, description }) => (
                <div class="flex flex-row max-w-md">
                  <div class="mb-4 mr-4">
                    <div class="text-white flex items-center justify-center w-12 h-12 rounded-full bg-secondary-500 dark:bg-secondary-700">
                      <IconStar />
                    </div>
                  </div>
                  <div>
                    <h3 class="mb-3 text-xl font-bold">{title}</h3>
                    <p class="text-gray-600 dark:text-slate-400">
                      {description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
});

export const FeaturesItem: RegisteredComponent=   {
  component: Features,
  name: 'Features',
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
      name: 'leftColumn',
      type: 'list',
      subFields: [
        {
          name: "title",
          type: 'string',
        },
        {
          name: "description",
          type: 'longText'
        }
      ]
    },
    {
      name: 'rightColumn',
      type: 'list',
      subFields: [
        {
          name: "title",
          type: 'string',
        },
        {
          name: "description",
          type: 'longText'
        }
      ]
    }
  ],
}
