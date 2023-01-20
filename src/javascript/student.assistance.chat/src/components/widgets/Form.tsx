import { component$, useContext, useTask$, useStore } from '@builder.io/qwik';
import { FormRecordIdContext, FormPromptIdContext, FormUpdateCounterContext } from "~/providers/FormContexts";
import { GptContext } from "~/providers/GptContext";


type Item = {
  recordId: string
  formText: string
}

type ButtonState = {
  disabled: boolean
}

export default component$((props: {items: Item[]}) => {
  const formRecordIdState = useContext(FormRecordIdContext);
  const formUpdateCounterState = useContext(FormUpdateCounterContext);
  const gptState = useContext(GptContext);

  const buttonState = useStore<ButtonState>({disabled: false});

  useTask$(() => {
    for (let i = 0; i < props.items.length; i++) {
      const item = props.items[i]

      const startingContent = ""

      formRecordIdState[item.recordId] = startingContent
    }
  })


  return (
    <div class="container mx-auto items-center">
      <div class="px-5 py-5 flex justify-between bg-white border-b-2 shadow-lg rounded-lg">
        <form class="w-full">
          {props.items.map(({recordId, formText}) => (
            <div class="flex flex-wrap -mx-3 mb-6">
              <div class="w-full px-3">
                <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-password">
                  {formText}
                </label>
                <input
                  id={recordId}
                  value={formRecordIdState[recordId]}
                  onChange$={async (event) => {
                    const value = event.target.value

                    const body = JSON.stringify({
                      content: `{"${recordId}": "${value}"}`,
                    })

                    await fetch("https://api.assistance.chat/save", {
                      method: 'POST',
                      body: body,
                      headers: {
                        'Content-Type': 'application/json;charset=UTF-8',
                        "Authorization": `Bearer ${gptState.accessToken}`,
                      }
                    });
                  }}
                  onInput$={(event) => {
                    if (event.target == null) {
                      return
                    }
                    const target: HTMLInputElement = event.target as HTMLInputElement
                    const value = target.value
                    formRecordIdState[recordId] = value
                    formUpdateCounterState.counter += 1
                  }}
                  type="text"
                  class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                />
              </div>
            </div>
          ))}
          <button
            class="block btn btn-primary sm:mb-0"
            type="button"
            disabled={buttonState.disabled}
            onClick$={async () => {
              buttonState.disabled = true
              console.log(gptState.initialPrompt)

              const body = JSON.stringify({
                client_name: formRecordIdState["name"],
              })

              console.log(body)

              const firstMessageResponse = await fetch("https://api.assistance.chat/chat/student/start", {
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

              const e = document.getElementById("gpt-assistance-chat");
              if (e !== null) {
                e.scrollIntoView();
              }
            }}
          >
            Begin Chat
          </button>
        </form>
      </div>
    </div>
  );
});
