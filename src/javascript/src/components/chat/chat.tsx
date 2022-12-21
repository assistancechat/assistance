import { component$ } from "@builder.io/qwik";

export default component$(() => {
  return (
    <div class="fixed right-10 bottom-10 w-96 z-40 shadow-2xl rounded-lg bg-white">
        <div class="w-full px-5 flex flex-col justify-between">
            <div class="mt-5">
                <div class="flex justify-end mb-4">
                    <div
                    class="mr-2 py-3 px-4 bg-blue-400 rounded-bl-3xl rounded-tl-3xl rounded-tr-xl text-white"
                    >
                    Welcome to group everyone !
                    </div>
                    <img
                    src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
                    class="object-cover h-8 w-8 rounded-full"
                    alt=""
                    />
                </div>
                <div class="flex justify-start mb-4">
                    <img
                    src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
                    class="object-cover h-8 w-8 rounded-full"
                    alt=""
                    />
                    <div
                    class="ml-2 py-3 px-4 bg-gray-400 rounded-br-3xl rounded-tr-3xl rounded-tl-xl text-white"
                    >
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Quaerat
                    at praesentium, aut ullam delectus odio error sit rem. Architecto
                    nulla doloribus laborum illo rem enim dolor odio saepe,
                    consequatur quas?
                    </div>
                </div>
                <div class="flex justify-end mb-4">
                    <div>
                    <div
                        class="mr-2 py-3 px-4 bg-blue-400 rounded-bl-3xl rounded-tl-3xl rounded-tr-xl text-white"
                    >
                        Lorem ipsum dolor, sit amet consectetur adipisicing elit.
                        Magnam, repudiandae.
                    </div>

                    <div
                        class="mt-4 mr-2 py-3 px-4 bg-blue-400 rounded-bl-3xl rounded-tl-3xl rounded-tr-xl text-white"
                    >
                        Lorem ipsum dolor sit amet consectetur adipisicing elit.
                        Debitis, reiciendis!
                    </div>
                    </div>
                    <img
                    src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
                    class="object-cover h-8 w-8 rounded-full"
                    alt=""
                    />
                </div>
                <div class="flex justify-start mb-4">
                    <img
                    src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
                    class="object-cover h-8 w-8 rounded-full"
                    alt=""
                    />
                    <div
                    class="ml-2 py-3 px-4 bg-gray-400 rounded-br-3xl rounded-tr-3xl rounded-tl-xl text-white"
                    >
                    happy holiday guys!
                    </div>
                </div>
            </div>
            <div class="py-5">
            <input
                class="w-full bg-gray-300 py-5 px-3 rounded-xl"
                type="text"
                placeholder="type your message here..."
            />
            </div>
        </div>
    </div>
  );
});
