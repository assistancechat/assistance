import { component$ } from "@builder.io/qwik";

export default component$((props: {conversation: string[]}) => {




  return (
    <div class="fixed right-10 bottom-10 w-96 z-40 shadow-2xl rounded-lg bg-white">
        <div class="w-full px-5 flex flex-col justify-between">
            <div class="mt-5">
                {props.conversation.map((content, index) => {
                    return (
                        <div class={`flex ${index % 2 == 0 ? "justify-start" : "justify-end"} mb-4`}>
                            <img
                            src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
                            class="object-cover h-8 w-8 rounded-full"
                            style={{order: `${index % 2 == 0 ? "1" : "3"}`}}
                            alt=""
                            />
                            <div
                            class={`ml-2 py-3 px-4 text-white ${index % 2 == 0 ? "bg-gray-400 ml-2 rounded-br-3xl rounded-tr-3xl rounded-tl-xl" : "bg-blue-400 mr-2 rounded-bl-3xl rounded-tl-3xl rounded-tr-xl"}`}
                            style={{order: "2"}}
                            >
                                {content}
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
  );
});
