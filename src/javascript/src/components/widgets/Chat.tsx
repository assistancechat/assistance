import { component$, useContext, useTask$, QwikChangeEvent, QwikKeyboardEvent, $ } from '@builder.io/qwik';
import { RegisteredComponent } from "@builder.io/sdk-qwik";
import { FormRecordIdContext, FormPromptIdContext, FormUpdateCounterContext } from "~/providers/form";
import { GptContext } from "~/providers/gpt";


type Message = {
  message: string
}

// TODO: Make this DRY
type FieldToWaitFor = {
  recordId: string
}


export const Chat = component$((props: {disabled: boolean, fieldsToWaitFor: FieldToWaitFor[], conversation: Message[]}) => {
  const formRecordIdState = useContext(FormRecordIdContext);
  const gptState = useContext(GptContext);

  if (props.conversation == null || props.conversation.length == 0) {
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

  const resize$ = $((event: QwikChangeEvent<HTMLTextAreaElement> | QwikKeyboardEvent<HTMLTextAreaElement>) => {
    if (event.target == null) {
      return
    }

    const el = event.target as HTMLTextAreaElement

    el.style.height = '5px'
    el.style.height = `${(el.scrollHeight + 4)}px`
  })

  const submitMessage$ = $(async (event: QwikChangeEvent<HTMLTextAreaElement> | QwikKeyboardEvent<HTMLTextAreaElement>) => {
    if (event.target == null) {
      return
    }

    const target = event.target as HTMLTextAreaElement

    let message = target.value
    props.conversation.push({message})
    target.value = ""

    resize$(event)

    const body = JSON.stringify({
      client_name: formRecordIdState["preferredName"],
      agent_name: gptState.agentName,
      client_text: message,
    })

    const continuedMessageResponse = await fetch("https://api.assistance.chat/chat/continue", {
      method: 'POST',
      body: body,
      headers: {
        'Content-Type': 'application/json;charset=UTF-8',
        "Authorization": `Bearer ${gptState.accessToken}`,
      }
    });

    const continuedMessageData = await continuedMessageResponse.json()
    message = continuedMessageData["response"]

    gptState.conversation.push({message})
  })

  return (
    <div class="container mx-auto items-center">
      <div class="px-5 py-5 flex justify-between bg-white border-b-2 shadow-lg rounded-lg">
        <div class="w-full px-5 flex flex-col justify-between">
          <div class="mt-5">
            {props.conversation.map(({message}, index) => {
              return (
                <div class={`flex ${index % 2 == 0 ? "justify-start" : "justify-end"} mb-4`}>
                  <div
                    class={`ml-2 py-3 px-4 text-white ${index % 2 == 0 ? "bg-gray-400 ml-2 rounded-br-3xl rounded-tr-3xl rounded-tl-xl" : "bg-blue-400 mr-2 rounded-bl-3xl rounded-tl-3xl rounded-tr-xl"}`}
                    style={{order: "2", "overflow-wrap": "anywhere"}}
                  >
                    {message.replaceAll("{clientName}", formRecordIdState['preferredName']).replaceAll("{agentName}", gptState.agentName)}
                  </div>
                </div>
              )
            })}
          </div>
          <div class="py-5" style={{display: `${props.disabled ? "none" : "block"}`}}>
            <textarea
              style="overflow-y: hidden"
              class="appearance-none h-16 bg-gray-200 text-gray-700 border border-gray-200  w-full py-5 px-5 rounded-xl mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
              disabled={props.conversation.length % 2 == 0}
              placeholder="Type your message here..."
              onKeyDown$={async (event) => {
                resize$(event)

                if (event.key === "Enter") {
                  await submitMessage$(event)
                }
              }}
              onChange$={submitMessage$}
            />
          </div>
        </div>
      </div>
    </div>
  );
});

const GPTChat = component$((props: {agentName: string, prompt: string}) => {
  const formRecordIdState = useContext(FormRecordIdContext);
  const formPromptIdState = useContext(FormPromptIdContext);
  const formUpdateCounterState = useContext(FormUpdateCounterContext);
  const gptState = useContext(GptContext);

  useTask$(() => {
    gptState.promptTemplate = props.prompt
    gptState.agentName = props.agentName
  })

  useTask$(({track}) => {
    const template = track(() => gptState.promptTemplate);
    const clientName = track(() => formRecordIdState['preferredName']);
    const agentName = track(() => gptState.agentName);
    track(() => formUpdateCounterState.counter);

    gptState.initialPrompt = template
      .replaceAll("{clientName}", clientName)
      .replaceAll("{agentName}", agentName)
      .replaceAll("{formContents}", JSON.stringify(formPromptIdState, null, 2))
  })

  const preferredName = formRecordIdState['preferredName']
  const email = formRecordIdState['email']

  if (preferredName == null || preferredName == "" || email == null || email == "") {
    return <></>
  }

  return (
    <div>
      <Chat disabled={false} conversation={gptState.conversation} fieldsToWaitFor={[]}></Chat>
      <div id="gpt-assistance-chat"></div>
    </div>
  );
})

export const ChatItem: RegisteredComponent = {
  component: Chat,
  name: 'Chat',
  builtIn: true,
  inputs: [
    {
      name: 'disabled',
      type: "boolean",
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
      name: 'conversation',
      type: "list",
      subFields: [
        {
          name: "message",
          type: 'longText',
        }
      ]
    },
  ],
}

export const GPTChatItem: RegisteredComponent = {
  component: GPTChat,
  name: 'GPTChat',
  builtIn: true,
  inputs: [
    {
      name: "agentName",
      type: "text"
    },
    {
      name: 'prompt',
      type: 'longText'
    }
  ],
}