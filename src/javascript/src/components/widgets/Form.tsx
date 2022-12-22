import { component$, useContext, useTask$, useStore, useServerMount$ } from '@builder.io/qwik';
import { RegisteredComponent } from "@builder.io/sdk-qwik";
import { FormContext, PromptContext } from "~/providers/form";


type Item = {
  recordId: string
  formText: string
  promptId: string
  startingContent: string
}

type FieldToWaitFor = {
  recordId: string
}

type PromptString = {
  prompt: string
}


const Form = component$((props: {hasButton: boolean, buttonText: string, fieldsToWaitFor: FieldToWaitFor[], items: Item[]}) => {
  const formState = useContext(FormContext);
  const promptState = useContext(PromptContext);
  const rawPromptState = useStore<PromptString>({prompt: ""})

  useTask$(() => {
    for (let i = 0; i < props.items.length; i++) {
      const item = props.items[i]

      const startingContent = item.startingContent ? item.startingContent : ""

      formState[item.recordId] = startingContent
      promptState.formContents[item.promptId] = startingContent
    }
  })

  useTask$(({ track }) => {
    track(() => formState['preferredName']);
    track(() => promptState);
    track(() => promptState.formContents);

    rawPromptState.prompt = promptState.template
      .replaceAll("{clientName}", formState['preferredName'])
      .replaceAll("{agentName}", promptState.agentName)
      .replaceAll("{formContents}", JSON.stringify(promptState.formContents, null, 2))
  })

  if (props.items === undefined || props.items.length === 0) {
    return <></>
  }

  if (props.fieldsToWaitFor != null) {
    for (let i = 0; i < props.fieldsToWaitFor.length; i++) {
      const item = formState[props.fieldsToWaitFor[i].recordId]
      if (item == null || item == "") {
        return <></>
      }
    }
  }

  return (
    <div class="container mx-auto items-center">
      <div class="px-5 py-5 flex justify-between bg-white border-b-2 shadow-lg rounded-lg">
        <form class="w-full">
          {props.items.map(({recordId, promptId, formText}) => (
            <div class="flex flex-wrap -mx-3 mb-6">
              <div class="w-full px-3">
                <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-password">
                  {formText}
                </label>
                <input
                  id={recordId}
                  value={formState[recordId]}
                  onChange$={(event) => {
                    const value = event.target.value
                    console.log(value)
                    formState[recordId] = value
                    promptState.formContents[promptId] = value
                  }}
                  type="text"
                  class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                />
              </div>
            </div>
          ))}
          <button
            style={{display: `${props.hasButton ? "block" : "none"}`}}
            class="btn btn-primary sm:mb-0"
            type="button"
            onClick$={() => {
              console.log(rawPromptState.prompt)
            }}
          >
            {props.buttonText}
          </button>
        </form>
      </div>
    </div>
  );
});


export const FormItem: RegisteredComponent = {
  component: Form,
  name: 'Form',
  builtIn: true,
  inputs: [
    {
      name: 'hasButton',
      type: "boolean"
    },
    {
      name: 'buttonText',
      type: "text"
    },
    {
      name: 'fieldsToWaitFor',
      type: "list",
      subFields: [
        {
          name: "recordId",
          type: 'string',
        }
      ]
    },
    {
      name: 'items',
      type: 'list',
      subFields: [
        {
          name: "recordId",
          type: 'string',
        },
        {
          name: "formText",
          type: 'string'
        },
        {
          name: "promptId",
          type: "string"
        },
        {
          name: "startingContent",
          type: "string",
        }
      ]
    }
  ],
}