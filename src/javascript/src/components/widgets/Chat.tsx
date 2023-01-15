import {
  component$,
  useContext,
  useTask$,
  // QwikChangeEvent,
  // QwikKeyboardEvent,
  $, useStore } from '@builder.io/qwik';
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

type TextAreaState = {
  content: string
}


export const Chat = component$((props: {disabled: boolean, fieldsToWaitFor: FieldToWaitFor[], conversation: Message[]}) => {
  const formRecordIdState = useContext(FormRecordIdContext);
  const gptState = useContext(GptContext);

  const textAreaState = useStore<TextAreaState>({content: ""});

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

  // const resize$ = $((event: QwikChangeEvent<HTMLTextAreaElement> | QwikKeyboardEvent<HTMLTextAreaElement>) => {
  //   if (event.target == null) {
  //     return
  //   }

  //   const el = event.target as HTMLTextAreaElement

  //   el.style.height = '5px'
  //   el.style.height = `${(el.scrollHeight + 4)}px`
  // })

  const submitMessage$ = $(async () => {
    let message = textAreaState.content.trim()

    if (message == "") {
      return
    }

    textAreaState.content = ""

    const body = JSON.stringify({
      client_name: formRecordIdState["preferredName"],
      agent_name: gptState.agentName,
      client_text: message,
    })

    props.conversation.push({message})

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

    props.conversation.push({message})
  })

  return (
    <div class="items-center">
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
              // style="overflow-y: hidden"
              rows={2}
              class="block w-full h-32 bg-gray-200 text-gray-700 border border-gray-200 py-5 pl-5 pr-14 rounded-xl mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
              disabled={props.conversation.length % 2 == 0}
              placeholder="Type your message here..."
              value={textAreaState.content}
              // onKeyUp$={resize$}
              onChange$={(event) => {textAreaState.content = event.target.value}}
            />
            <button
              class="absolute px-4 py-4 my-12 rounded-xl text-gray-500 bottom-1.5 right-10 hover:bg-gray-100 dark:hover:text-gray-400 dark:hover:bg-gray-900 disabled:hover:bg-transparent dark:disabled:hover:bg-transparent"
              disabled={props.conversation.length % 2 == 0}
              onClick$={submitMessage$}
            >
              <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 20 20" class="h-8 w-8 rotate-90" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"></path></svg>
            </button>
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
      <Chat
        disabled={false}
        conversation={gptState.conversation}
        // conversation={[{message:'Test'}, {message:'Test'}]}
        fieldsToWaitFor={[]}>
      </Chat>
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
