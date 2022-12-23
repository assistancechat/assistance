import { component$, useContext, useTask$, useStore } from '@builder.io/qwik';
import { RegisteredComponent } from "@builder.io/sdk-qwik";
import { FormRecordIdContext, FormPromptIdContext, FormUpdateCounterContext } from "~/providers/form";
import { GptContext } from "~/providers/gpt";


type Item = {
  recordId: string
  formText: string
  promptId: string
  startingContent: string
}

type FieldToWaitFor = {
  recordId: string
}

type ButtonState = {
  disabled: boolean
}

const Form = component$((props: {hasButton: boolean, buttonText: string, fieldsToWaitFor: FieldToWaitFor[], items: Item[]}) => {
  const formRecordIdState = useContext(FormRecordIdContext);
  const formPromptIdState = useContext(FormPromptIdContext);
  const formUpdateCounterState = useContext(FormUpdateCounterContext);
  const gptState = useContext(GptContext);

  const buttonState = useStore<ButtonState>({disabled: false});

  useTask$(() => {
    for (let i = 0; i < props.items.length; i++) {
      const item = props.items[i]

      const startingContent = item.startingContent ? item.startingContent : ""

      formRecordIdState[item.recordId] = startingContent
      formPromptIdState[item.promptId] = startingContent
    }
  })

  if (props.items === undefined || props.items.length === 0) {
    return <></>
  }

  if (props.fieldsToWaitFor != null) {
    for (let i = 0; i < props.fieldsToWaitFor.length; i++) {
      const item = formRecordIdState[props.fieldsToWaitFor[i].recordId]
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
                  value={formRecordIdState[recordId]}
                  onInput$={(event) => {
                    if (event.target == null) {
                      return
                    }
                    const target: HTMLInputElement = event.target as HTMLInputElement
                    const value = target.value
                    formRecordIdState[recordId] = value
                    formPromptIdState[promptId] = value
                    formUpdateCounterState.counter += 1
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
            disabled={buttonState.disabled}
            onClick$={async () => {
              buttonState.disabled = true
              const e = document.getElementById("gpt-assistance-chat");
              if (e !== null) {
                e.scrollIntoView();
              }

              console.log(gptState.initialPrompt)

              const body = JSON.stringify({
                client_name: formRecordIdState["preferredName"],
                agent_name: gptState.agentName,
                prompt: gptState.initialPrompt,
              })

              const firstMessageResponse = await fetch("https://api.assistance.chat/chat/start", {
                method: 'POST',
                body: body,
                headers: {
                  'Content-Type': 'application/json;charset=UTF-8',
                  "Authorization": `Bearer ${gptState.accessToken}`,
                }
              });

              const firstMessageData = await firstMessageResponse.json()
              const message: string = firstMessageData["response"]

              gptState.conversation.push({message})
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
          type: 'text',
        }
      ]
    },
    {
      name: 'items',
      type: 'list',
      subFields: [
        {
          name: "recordId",
          type: 'text',
        },
        {
          name: "formText",
          type: 'text'
        },
        {
          name: "promptId",
          type: "text"
        },
        {
          name: "startingContent",
          type: "text",
        }
      ]
    }
  ],
}