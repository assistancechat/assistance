import { component$ } from "@builder.io/qwik";

import Chat from "~/components/widgets/Chat";
import Form from "~/components/widgets/Form";
import GptChat from "~/components/widgets/GptChat";

export default component$(() => {
  return (
    <section class={`bg-gradient-to-b md:bg-gradient-to-r from-white via-purple-50 to-sky-100 dark:bg-none mt-[-100px]`}>
      <div class="max-w-6xl mx-auto px-4 sm:px-6 md:flex md:h-screen 2xl:h-auto pt-[100px]">
        <div class="py-12 md:py-12 lg:py-16 block md:flex text-center md:text-left w-full">
          <div class="pb-12 md:pb-0 md:py-0 max-w-5xl mx-auto md:pr-16 flex items-center basis-[56%]">
            <div>
              <h1 class="text-5xl md:text-[3.48rem] font-bold leading-tighter tracking-tighter mb-4 font-heading px-4 md:px-0">
                Student Assistance Chat
              </h1>
            </div>
          </div>
          <div class="block md:flex items-center flex-1">
            <div class="relative m-auto w-full">
              <Chat
                disabled={true}
                conversation={[{"message": "Testing"}]}
                fieldsToWaitFor={[]}>
              </Chat>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
});
