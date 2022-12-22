import { component$ } from "@builder.io/qwik";
import { RegisteredComponent } from "@builder.io/sdk-qwik";


const Chat = component$((props: {conversation: string[]}) => {
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
                    {message}
                  </div>
                </div>
              )
            })}
          </div>
          <div class="py-5">
            <input
              class="w-full bg-gray-300 py-5 px-5 rounded-xl"
              type="text"
              placeholder="Type your message here..."
            />
          </div>
        </div>
      </div>
    </div>
  );
});




export const ChatItem: RegisteredComponent = {
  component: Chat,
  name: 'Chat',
  builtIn: true,
  inputs: [
    {
      name: 'conversation',
      type: 'list',
      subFields: [
        {
          name: "message",
          type: 'string',
        },
      ]
    }
  ],
}