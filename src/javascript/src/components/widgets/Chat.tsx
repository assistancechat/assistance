import { component$, useContext, useTask$ } from '@builder.io/qwik';
import { RegisteredComponent } from "@builder.io/sdk-qwik";
import { FormContext, PromptContext } from "~/providers/form";


type Message = {
  message: string
}

// TODO: Make this DRY
type FieldToWaitFor = {
  recordId: string
}


export const Chat = component$((props: {disabled: boolean, fieldsToWaitFor: FieldToWaitFor[], conversation: Message[]}) => {
  const formState = useContext(FormContext);
  const promptState = useContext(PromptContext);

  if (props.conversation == null || props.conversation.length == 0) {
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
        <div class="w-full px-5 flex flex-col justify-between">
          <div class="mt-5">
            {props.conversation.map(({message}, index) => {
              return (
                <div class={`flex ${index % 2 == 0 ? "justify-start" : "justify-end"} mb-4`}>
                  <div
                    class={`ml-2 py-3 px-4 text-white ${index % 2 == 0 ? "bg-gray-400 ml-2 rounded-br-3xl rounded-tr-3xl rounded-tl-xl" : "bg-blue-400 mr-2 rounded-bl-3xl rounded-tl-3xl rounded-tr-xl"}`}
                    style={{order: "2"}}
                  >
                    {message.replaceAll("{clientName}", formState['preferredName']).replaceAll("{agentName}", promptState.agentName)}
                  </div>
                </div>
              )
            })}
          </div>
          <div class="py-5" style={{display: `${props.disabled ? "none" : "block"}`}}>
            <input
              class="w-full bg-gray-300 py-5 px-5 rounded-xl"
              type="text"
              disabled={props.disabled}
              placeholder={props.disabled ? "Use the link within your email before you can type a message." : "Type your message here..."}
            />
          </div>
        </div>
      </div>
    </div>
  );
});

const GPTChat = component$((props: {agentName: string, prompt: string}) => {
  const formState = useContext(FormContext);
  const promptState = useContext(PromptContext);

  useTask$(() => {
    promptState.template = props.prompt
    promptState.agentName = props.agentName
  })

  const preferredName = formState['preferredName']
  const email = formState['email']

  if (preferredName == null || preferredName == "" || email == null || email == "") {
    return <></>
  }

  return (
    <Chat disabled={false} conversation={[]} fieldsToWaitFor={[]}></Chat>
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